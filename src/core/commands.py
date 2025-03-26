from pydantic import BaseModel, Field, validator
from typing import List, Dict, Any

class MCPToolRequest(BaseModel):
    """MCP tool request model"""
    name: str
    arguments: Dict[str, Any] = Field(default_factory=dict)

    @validator('name')
    def validate_name(cls, v):
        valid_commands = ["move"]  # Add more valid commands here
        if v not in valid_commands:
            raise ValueError(f"Invalid command name. Must be one of: {valid_commands}")
        return v

class MoveCommand(BaseModel):
    """Move command model"""
    position: List[float]

class CommandResponse(BaseModel):
    """Command response model"""
    success: bool
    message: str 