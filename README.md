# 🎙️ LiveKit Voice Agent

A production-ready voice agent built with LiveKit Agents, featuring real-time speech processing, AI-powered responses, and seamless integration with LiveKit's real-time communication platform. This agent can handle voice interactions, process natural language, and integrate with various AI services.

## 🚀 Quick Start

### Prerequisites

- **Python 3.12+** - [Download Python](https://www.python.org/downloads/)
- **UV** (recommended) or pip - [Install UV](https://github.com/astral-sh/uv)
- **LiveKit Server** - [Get LiveKit Cloud](https://livekit.io/cloud) or [Self-host](https://docs.livekit.io/self-hosting/)
- **Mistral AI API Key** - [Get API Key](https://console.mistral.ai/api-keys/)
- **FFmpeg** - Required for audio processing ([Installation Guide](https://ffmpeg.org/download.html))

## 🛠️ Installation

1. **Clone and setup**
   ```bash
   # Clone the repository
   git clone https://github.com/yourusername/livekit-voice-agent.git
   cd livekit-voice-agent
   
   # Create and activate virtual environment (recommended)
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   
   # Install with UV (faster and more reliable)
   uv pip install -e .
   
   # Or with pip
   # pip install -e .
   ```

2. **Configure Environment**
   
   Copy the example environment file and update with your credentials:
   ```bash
   cp .env.example .env
   ```
   
   Edit the `.env` file with your configuration:
   ```env
   # Required: LiveKit Configuration
   LIVEKIT_URL=wss://your-instance.livekit.cloud
   LIVEKIT_API_KEY=your_api_key_here
   LIVEKIT_API_SECRET=your_api_secret_here
   
   # Required: Mistral AI Configuration
   MISTRAL_API_KEY=your_mistral_api_key_here
   
   # Optional: Voice Settings
   VOICE_MODEL=eleven-mono
   VOICE_SPEED=1.0
   
   # Optional: Logging
   LOG_LEVEL=INFO
   ```

## 📁 Project Structure

```
livekit-voice-agent/
├── agent.py           # Main agent implementation and entry point
├── prompt.py          # System prompts and conversation templates
├── tool.py            # Custom tools and utilities
├── pyproject.toml     # Project dependencies and configuration
├── .env.example       # Example environment configuration
└── README.md          # This file
```

## 🚀 Running the Agent

1. **Start the agent**
   ```bash
   # Basic usage
   python -m livekit_voice_agent.agent
   
   # With custom room and identity
   python -m livekit_voice_agent.agent --room my-room --identity assistant
   
   # With debug logging
   LOG_LEVEL=DEBUG python -m livekit_voice_agent.agent
   ```

2. **Connect to the Agent**
   
   **Option 1: LiveKit Test App**
   1. Go to [LiveKit Test App](https://meet.livekit.io/)
   2. Enter the same room name you started the agent with
   3. Start a voice call and interact with the agent
   
   **Option 2: Custom Client**
   Use any LiveKit client SDK to connect to the room where the agent is running.

## ⚙️ Configuration

### Agent Settings
Modify `agent.py` to customize:
- Voice model and parameters
- Audio processing settings
- Timeout and retry configurations

### System Prompt
Edit `prompt.py` to adjust:
- Agent personality and behavior
- Response style and formatting
- Context and memory settings

### Tools
Enhance `tool.py` to add:
- New functionality via custom tools
- API integrations
- Data processing utilities

### Environment Variables
| Variable | Required | Description |
|----------|----------|-------------|
| `LIVEKIT_URL` | Yes | WebSocket URL of your LiveKit server |
| `LIVEKIT_API_KEY` | Yes | API key for LiveKit server |
| `LIVEKIT_API_SECRET` | Yes | API secret for LiveKit server |
| `MISTRAL_API_KEY` | Yes | API key for Mistral AI |
| `VOICE_MODEL` | No | Voice model to use (default: eleven-mono) |
| `LOG_LEVEL` | No | Logging level (DEBUG, INFO, WARNING, ERROR) |

## Development

## 📦 Dependencies

### Core Dependencies
- `livekit-agents`: Core framework for building LiveKit agents
- `livekit-plugins-noise-cancellation`: Real-time noise cancellation
- `python-dotenv`: Environment variable management
- `pydantic`: Data validation and settings management
- `loguru`: Modern logging utility

### Development Dependencies
- `black`: Code formatting
- `mypy`: Static type checking
- `pytest`: Testing framework
- `pytest-asyncio`: Async test support

### Adding New Features

1. **Add new tools**:
   - Create a new function in `tool.py`
   - Register it with the `@tool()` decorator
   - Update the system prompt to inform the agent about the new tool

2. **Modify behavior**:
   - Adjust the system prompt in `prompt.py`
   - Modify the agent's logic in `agent.py`

## 🐛 Troubleshooting

### Common Issues

#### Connection Problems
```
❌ Failed to connect to LiveKit server
```
- Verify `LIVEKIT_URL` starts with `wss://`
- Check API key/secret permissions
- Ensure your LiveKit server is running and accessible

#### Audio Issues
```
❌ No audio detected
```
- Check microphone permissions
- Verify audio input/output devices
- Ensure FFmpeg is installed and in PATH

#### Dependency Conflicts
```bash
# Check for conflicts
uv pip check

# Resolve conflicts
uv pip install --upgrade-strategy=only-if-needed -e .
```

### Getting Help
- Check the [LiveKit Documentation](https://docs.livekit.io/)
- Search [LiveKit Community](https://github.com/livekit/livekit/discussions)
- [Open an Issue](https://github.com/yourusername/livekit-voice-agent/issues) for bugs or feature requests

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [LiveKit](https://livekit.io/) for the amazing real-time platform
- [Mistral AI](https://mistral.ai/) for powerful language models
- All contributors who help improve this project

---

by ~chaitanya ♥️
