import logging
import websockets
import json
import asyncio
import sys
import os
from typing import Dict, Any

# Add the project root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.core.commands import MCPToolRequest, CommandResponse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BulletController:
    def __init__(self):
        try:
            self.simulator_uri = "ws://localhost:8765/ws"  # PyBullet simulator runs on port 8765
            self.websocket = None
            self.lock = asyncio.Lock()  # Add lock for WebSocket operations
            logger.info("Successfully initialized controller")
        except Exception as e:
            logger.error(f"Failed to initialize controller: {str(e)}")
            raise

    async def ensure_connection(self):
        """Ensure WebSocket connection is established"""
        if self.websocket is None:
            self.websocket = await websockets.connect(self.simulator_uri)
            logger.info("[WS] Connected to simulator")

    async def send_to_simulator(self, command: Dict[str, Any]) -> Dict[str, Any]:
        """Send command to simulator and wait for response"""
        try:
            await self.ensure_connection()
            async with self.lock:  # Use lock to prevent concurrent operations
                await self.websocket.send(json.dumps(command))
                response = await self.websocket.recv()
                response_data = json.loads(response)
                
                # Handle error response format
                if "error" in response_data:
                    return {
                        "success": False,
                        "message": response_data.get("error", "Unknown error")
                    }
                    
                return response_data
        except Exception as e:
            logger.error(f"Error communicating with simulator: {str(e)}")
            # Try to reconnect on error
            self.websocket = None
            return {
                "success": False,
                "message": f"Error: {str(e)}"
            }

    def validate_move_command(self, arguments: Dict[str, Any]) -> bool:
        """Validate move command arguments"""
        # Check for required arguments
        required_args = {"position"}
        if not all(arg in arguments for arg in required_args):
            return False
            
        # Check for extra arguments
        if len(arguments) > len(required_args):
            return False
            
        # Validate position argument
        if not isinstance(arguments["position"], list) or len(arguments["position"]) != 3:
            return False
        if not all(isinstance(x, (int, float)) for x in arguments["position"]):
            return False
            
        return True

    async def handle_mcp(self, mcp: MCPToolRequest) -> CommandResponse:
        """Handle MCP commands"""
        try:
            if mcp.name == "move":
                if not self.validate_move_command(mcp.arguments):
                    return CommandResponse(
                        success=False,
                        message="Invalid move command arguments"
                    )
                command = {
                    "type": "move",
                    "position": mcp.arguments["position"]
                }
                result = await self.send_to_simulator(command)
                return CommandResponse(**result)
            return CommandResponse(
                success=False,
                message="Unknown command"
            )
        except Exception as e:
            logger.error(f"Error handling MCP command: {str(e)}")
            return CommandResponse(
                success=False,
                message=f"Error: {str(e)}"
            ) 