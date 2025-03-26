# PyBullet Robot Control System (PyBulletMCP)
<div align="center">

### By Yaoyao(Freax) Qian

[![Website](https://img.shields.io/badge/Website-h--freax.github.io-blue?style=flat-square&logo=firefox)](https://h-freax.github.io)
[![GitHub](https://img.shields.io/badge/GitHub-H--Freax-black?style=flat-square&logo=github)](https://github.com/H-Freax)
[![Email](https://img.shields.io/badge/Email-limyoonaxi@gmail.com-red?style=flat-square&logo=gmail)](mailto:limyoonaxi@gmail.com)

</div>
A flexible and extensible robot control system using PyBullet for simulation and FastAPI for web interface. PyBulletMCP is designed to provide a microservice-based architecture for robot control, enabling seamless integration between simulation and real-world applications.

## Version

Current Version: v0.0.1 (Alpha)
![image](https://github.com/user-attachments/assets/4b1b546b-14b4-481a-8ce7-1b8667fdcda4)

### Changelog

#### v0.0.1 (2024-03-26)
- Initial alpha release
- Basic PyBulletMCP architecture implementation
- Core components:
  - PyBullet simulation environment
  - MCP (Microservice Control Platform) server
  - WebSocket-based communication
  - Natural language command interface
  - Web-based control panel

## About PyBulletMCP

PyBulletMCP is a microservice-based robot control system that separates the simulation environment from the control logic. This architecture provides several benefits:

- **Decoupled Components**: The simulation environment runs independently from the control server
- **Flexible Deployment**: Components can be deployed on different machines
- **Easy Integration**: Simple to integrate with other systems through WebSocket/REST APIs
- **Scalable Architecture**: Support for multiple robots and control interfaces

### Core Components

1. **Simulator Service**
   - PyBullet physics engine
   - Robot model visualization
   - Real-time simulation loop
   - WebSocket server on port 8765

2. **MCP Service**
   - Command processing
   - State management
   - WebSocket communication
   - Persistent WebSocket connections
   - Thread-safe command handling

3. **Web Interface**
   - User-friendly control panel
   - Real-time status updates
   - Command history

## Features

- Natural language command interface for robot control
- Real-time PyBullet simulation with visualization
- WebSocket-based communication between components
- Modular architecture for easy extension
- RESTful API endpoints for external integration
- Persistent WebSocket connections for improved performance
- Thread-safe command handling with connection management

## Project Structure

```
pybulletmcp/
├── src/
│   ├── core/           # Core functionality
│   │   ├── controller.py    # Robot controller
│   │   └── commands.py     # Command definitions
│   ├── web/            # Web interface
│   │   ├── server.py       # FastAPI server
│   │   └── templates/      # HTML templates
│   ├── simulator/      # PyBullet simulation
│   │   └── simulator.py    # PyBullet environment
│   └── utils/          # Utility functions
│       └── parser.py       # Command parsing
├── docs/               # Documentation
├── assets/            # Robot models and resources
│   ├── workspace/     # Workspace URDF
│   └── ur5e/         # UR5e robot URDF
├── requirements.txt   # Python dependencies
├── start.sh          # Start script
└── README.md         # This file
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/H-Freax/PybulletMCP.git
cd PybulletMCP
```

2. Create and activate a conda environment:
```bash
conda create -n pybulletmcp python=3.8
conda activate pybulletmcp
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
Create a `.env` file in the project root with the following variables:
```bash
OPENAI_API_KEY=your_openai_api_key_here
```

5. Start the simulator:
```bash
python src/simulator/simulator.py
```

6. Start the MCP server:
```bash
python src/web/server.py
```

The simulator will run on port 8765, and the MCP server will handle WebSocket connections to the simulator. The web interface will be available at http://localhost:8080.

## Usage

### Quick Start

Simply run the start script:
```bash
./start.sh
```

This will start both the PyBullet simulator and the web server. Then open your browser and navigate to:
```
http://localhost:8080
```

### Manual Start (Alternative)

If you need to start the components separately:

1. Start the PyBullet simulator:
```bash
python src/simulator/simulator.py
```

2. In a new terminal, start the web server:
```bash
python src/web/server.py
```

3. Open your browser and navigate to:
```
http://localhost:8080
```

## Available Commands

The system supports the following natural language commands:

- Direction-based movement:
  - "Move right 1 meter"
  - "Move forward 0.5 meters"
  - "Move up 0.3 meters"
  - "Move left 2 meters"
  - "Move backward 1 meter"
  - "Move down 0.5 meters"

- Coordinate-based movement:
  - "Move to position (1, 0, 0)"
  - "Move to coordinates (0.5, 1.0, 0.3)"

## API Documentation

### WebSocket Endpoint
```
ws://localhost:8080/ws
```

### REST Endpoints

#### POST /command
Send natural language commands to control the robot.

Request body:
```json
{
    "command": "Move right 1 meter"
}
```

Response:
```json
{
    "success": true,
    "message": "Moved to [1.0, 0.0, 0.0]"
}
```

## Development

### Adding New Commands

1. Add command definition in `src/core/commands.py`
2. Implement command handling in `src/core/controller.py`
3. Add natural language parsing in `src/utils/parser.py`

### Architecture Notes

- The simulator runs on port 8765 and handles WebSocket connections for robot control
- The MCP server maintains persistent WebSocket connections to the simulator
- All WebSocket operations are thread-safe using asyncio locks
- The system supports both natural language and JSON format commands

## TODO List

### High Priority
- [ ] Add joint control commands
- [ ] Implement collision detection
- [ ] Add robot state monitoring
- [ ] Improve error handling and recovery

### Medium Priority
- [ ] Add support for multiple robots
- [ ] Implement trajectory planning
- [ ] Add camera feed visualization
- [ ] Create configuration file system
- [ ] Add logging system

### Low Priority
- [ ] Add support for custom URDF models
- [ ] Implement robot calibration
- [ ] Add support for gripper control
- [ ] Create user authentication system
- [ ] Add support for recording and playback

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.



## Citation

If you use PyBulletMCP in your research or project, please cite it as:

```bibtex
@software{pybulletmcp2024,
  author = {Yaoyao, Qian},
  title = {PyBulletMCP: A Microservice-based Robot Control System},
  year = {2024},
  publisher = {GitHub},
  url = {https://github.com/H-Freax/PybulletMCP},
  version = {0.0.1}
}
```
