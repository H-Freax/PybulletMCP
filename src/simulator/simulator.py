import pybullet as p
import pybullet_data
import os
import logging
import asyncio
import websockets
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PyBulletSimulator:
    def __init__(self):
        try:
            # Connect to PyBullet with GUI
            self.physicsClient = p.connect(p.GUI)
            p.setAdditionalSearchPath(pybullet_data.getDataPath())
            p.setGravity(0, 0, -9.8)
            
            # Get the absolute path to assets directory
            current_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            assets_dir = os.path.join(current_dir, "assets")
            
            # Load workspace and UR5e
            workspace_path = os.path.join(assets_dir, "workspace", "workspace.urdf")
            ur5e_path = os.path.join(assets_dir, "ur5e", "ur5e.urdf")
            
            if not os.path.exists(workspace_path):
                raise FileNotFoundError(f"Workspace URDF not found at {workspace_path}")
            if not os.path.exists(ur5e_path):
                raise FileNotFoundError(f"UR5e URDF not found at {ur5e_path}")
                
            p.loadURDF(workspace_path, basePosition=[0, 0, 0])
            self.ur5 = p.loadURDF(ur5e_path, basePosition=[0, 0, 0], useFixedBase=True)
            logger.info("Successfully initialized PyBullet environment")
            
        except Exception as e:
            logger.error(f"Failed to initialize PyBullet environment: {str(e)}")
            raise

    def move_robot(self, position):
        """Move the robot to the specified position"""
        try:
            p.resetBasePositionAndOrientation(self.ur5, position, [0, 0, 0, 1])
            return {"success": True, "message": f"Moved to {position}"}
        except Exception as e:
            logger.error(f"Error moving robot: {str(e)}")
            return {"success": False, "message": f"Error: {str(e)}"}

    async def handle_command(self, websocket, path):
        """Handle incoming WebSocket commands"""
        try:
            async for message in websocket:
                try:
                    command = json.loads(message)
                    if command.get("type") == "move":
                        position = command.get("position", [0, 0, 0])
                        result = self.move_robot(position)
                        await websocket.send(json.dumps(result))
                    else:
                        await websocket.send(json.dumps({
                            "success": False,
                            "message": "Unknown command type"
                        }))
                except json.JSONDecodeError:
                    await websocket.send(json.dumps({
                        "success": False,
                        "message": "Invalid JSON format"
                    }))
        except websockets.exceptions.ConnectionClosed:
            logger.info("Client disconnected")
        except Exception as e:
            logger.error(f"Error handling command: {str(e)}")
            await websocket.send(json.dumps({
                "success": False,
                "message": f"Error: {str(e)}"
            }))

    async def run(self):
        """Run the simulation loop and WebSocket server"""
        try:
            # Start WebSocket server
            server = await websockets.serve(
                self.handle_command,
                "localhost",
                8765
            )
            logger.info("WebSocket server started on ws://localhost:8765")
            
            # Run simulation loop
            while True:
                p.stepSimulation()
                await asyncio.sleep(1.0 / 240.0)
                
        except KeyboardInterrupt:
            logger.info("Simulation stopped by user")
        finally:
            p.disconnect()

if __name__ == "__main__":
    simulator = PyBulletSimulator()
    asyncio.run(simulator.run()) 