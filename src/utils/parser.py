import re
from typing import Dict, Any
from openai import OpenAI
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def parse_natural_language(command: str) -> Dict[str, Any]:
    """Parse natural language command into structured format using LLM"""
    try:
        # Prepare the prompt for the LLM
        prompt = f"""Parse the following command into a structured format.
Command: {command}

The output should be a JSON object with the following structure:
{{
    "name": "move",
    "arguments": {{
        "position": [x, y, z]  # List of three numbers representing the target position
    }}
}}

For directional movements:
- "right" -> [1, 0, 0]
- "left" -> [-1, 0, 0]
- "forward" -> [0, 1, 0]
- "backward" -> [0, -1, 0]
- "up" -> [0, 0, 1]
- "down" -> [0, 0, -1]

Multiply the direction vector by the distance value.
Only output the JSON object, nothing else."""

        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a command parser that converts natural language into structured JSON format."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1  # Low temperature for consistent output
        )

        # Extract and parse the JSON response
        content = response.choices[0].message.content
        if not isinstance(content, str):
            raise ValueError("Invalid response format")
        json_str = content.strip()
        parsed_command = json.loads(json_str)

        # Validate the parsed command
        if not isinstance(parsed_command, dict) or "name" not in parsed_command or "arguments" not in parsed_command:
            raise ValueError("Invalid command structure")
        
        if parsed_command["name"] != "move":
            raise ValueError("Only move commands are supported")
        
        if "position" not in parsed_command["arguments"]:
            raise ValueError("Missing position argument")
        
        position = parsed_command["arguments"]["position"]
        if not isinstance(position, list) or len(position) != 3:
            raise ValueError("Position must be a list of three numbers")
        
        if not all(isinstance(x, (int, float)) for x in position):
            raise ValueError("Position coordinates must be numbers")

        return parsed_command

    except Exception as e:
        raise ValueError(f"Command parsing error: {str(e)}") 