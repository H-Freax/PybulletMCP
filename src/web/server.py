from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn
import json
import logging
import os
import sys
from typing import Dict

# Add the project root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.core.controller import BulletController
from src.core.commands import MCPToolRequest
from src.utils.parser import parse_natural_language
from pydantic import ValidationError

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI()

# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Mount static files
app.mount("/static", StaticFiles(directory=os.path.join(current_dir, "static")), name="static")

try:
    controller = BulletController()
    logger.info("Successfully initialized BulletController")
except Exception as e:
    logger.error(f"Failed to initialize BulletController: {str(e)}")
    raise

@app.get("/")
async def read_root():
    return FileResponse(os.path.join(current_dir, "templates", "index.html"))

@app.post("/command")
async def handle_command(command: Dict[str, str]):
    try:
        # Parse natural language command
        parsed_command = parse_natural_language(command["command"])
        
        # Convert to MCP format
        mcp_request = MCPToolRequest(**parsed_command)
        
        # Handle command
        result = await controller.handle_mcp(mcp_request)
        return result.dict()
    except ValueError as e:
        return {"success": False, "message": str(e)}
    except Exception as e:
        logger.error(f"Error handling command: {str(e)}")
        return {"success": False, "message": f"Error: {str(e)}"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    logger.info("[WS] Client connected")
    try:
        while True:
            data = await websocket.receive_text()
            logger.info(f"[WS] Received command: {data}")
            try:
                # Try to parse as JSON first
                try:
                    command_data = json.loads(data)
                    if isinstance(command_data, dict) and "type" in command_data:
                        # If it's a JSON command, convert it to natural language
                        if command_data["type"] == "move" and "position" in command_data:
                            position = command_data["position"]
                            # Convert position to natural language
                            if position == [1, 0, 0]:
                                data = "move right 1 meter"
                            elif position == [-1, 0, 0]:
                                data = "move left 1 meter"
                            elif position == [0, 1, 0]:
                                data = "move forward 1 meter"
                            elif position == [0, -1, 0]:
                                data = "move backward 1 meter"
                            elif position == [0, 0, 1]:
                                data = "move up 1 meter"
                            elif position == [0, 0, -1]:
                                data = "move down 1 meter"
                            else:
                                data = f"move to position ({position[0]}, {position[1]}, {position[2]})"
                except json.JSONDecodeError:
                    # If not JSON, treat as natural language
                    pass

                # Parse natural language command
                logger.info("[WS] Parsing command...")
                parsed_command = parse_natural_language(data)
                logger.info(f"[WS] Parsed command: {parsed_command}")
                
                # Convert to MCP format
                logger.info("[WS] Converting to MCP format...")
                mcp_request = MCPToolRequest(**parsed_command)
                logger.info(f"[WS] MCP request: {mcp_request}")
                
                # Handle command
                logger.info("[WS] Handling command...")
                result = await controller.handle_mcp(mcp_request)
                logger.info(f"[WS] Command result: {result}")
                
                # Send response back to client
                response = result.dict()
                await websocket.send_text(json.dumps(response))
                
            except ValueError as e:
                error_msg = {"error": "Invalid command format", "details": str(e)}
                logger.error(f"[WS] Validation error: {error_msg}")
                await websocket.send_text(json.dumps(error_msg))
            except Exception as e:
                error_msg = {"error": "Internal server error", "details": str(e)}
                logger.error(f"[WS] Unexpected error: {error_msg}")
                await websocket.send_text(json.dumps(error_msg))
    except WebSocketDisconnect:
        logger.info("[WS] Client disconnected")
    except Exception as e:
        logger.error(f"[WS] WebSocket error: {str(e)}")
        raise

if __name__ == "__main__":
    # Start the server
    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=8080,
        reload=True,
        log_level="info"
    ) 