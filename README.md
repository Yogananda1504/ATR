# AI Agent-based Deep Research System

This project implements a dual-agent AI research system that crawls websites using Tavily for online information gathering. The system consists of two specialized agents:

1. **Research Agent**: Focuses on data collection and web-based research
2. **Answer Drafter Agent**: Composes structured, comprehensive answers based on the research

The project uses LangGraph and LangChain frameworks to organize the information flow and manage the agent interactions.

## Features

- Web crawling and information gathering using Tavily API
- Dual-agent architecture for specialized tasks
- LangGraph workflow for organized information processing
- Structured answer composition with source attribution
- Research data persistence for future reference

## System Architecture

```
┌───────────────────┐     ┌─────────────────────┐
│                   │     │                     │
│   Research Agent  │────▶│   Answer Drafter    │
│                   │     │                     │
└───────────────────┘     └─────────────────────┘
         │                            │
         │                            │
         ▼                            ▼
┌───────────────────┐     ┌─────────────────────┐
│                   │     │                     │
│   Tavily Search   │     │  Structured Answer  │
│                   │     │                     │
└───────────────────┘     └─────────────────────┘
            │                        │
            └────────────┬───────────┘
                         │
                         ▼
                ┌─────────────────┐
                │                 │
                │  LangGraph      │
                │  Orchestrator   │
                │                 │
                └─────────────────┘
```

## Setup

### Prerequisites

- Python 3.9+
- Tavily API key
- GitHub AI API key

### Installation

1. Clone the repository
   ```bash
   git clone https://github.com/yourusername/ai-research-system.git
   cd ai-research-system
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root with your API keys:
   ```
   GITHUB_API_KEY=your_github_api_key_here
   TAVILY_API_KEY=your_tavily_api_key_here
   ```

### Environment Setup

#### Setting up a virtual environment (recommended)

It's recommended to use a virtual environment to avoid conflicts with other Python projects:

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### Getting API Keys

1. **Github API Key**:
   - Sign up at [Github.com](https://github.com/)
   - Navigate to API keys section and create a new key
   - Copy the key to your `.env` file

2. **Tavily API Key**:
   - Register at [Tavily](https://tavily.com/)
   - Get your API key from the dashboard
   - Add it to your `.env` file

## Usage

### Running the system

```bash
 python src/github_main.py -q "genetic sequencing"
```

### Examples

```bash
# Research a scientific topic
python src/main.py --query "What are the latest advancements in CRISPR gene editing?"

# Gather information on a historical event
python src/main.py --query "What were the economic impacts of the Industrial Revolution?"

# Research a technical concept
python src/main.py --query "Explain quantum computing and its potential applications"
```

### Running the demo

```bash
python src/demo.py
```

### Customizing Research Parameters

You can customize various research parameters by modifying the configuration in `src/config.py` or by passing additional arguments:

```bash
python src/main.py --query "Your query" --search_depth 3 --max_sources 5
```

## Project Structure

```
ai_research_system/
├── data/               # Storage for research results
├── docs/               # Documentation
├── src/
│   ├── research_agent.py      # Research agent implementation
│   ├── answer_drafter_agent.py # Answer drafting agent
│   ├── orchestrator.py        # LangGraph workflow orchestrator
│   ├── main.py               # Main entry point
│   └── demo.py               # Demo script
└── requirements.txt    # Project dependencies
```

## Advanced Usage

### Customizing Agent Behavior

The system allows for customization of agent behavior through configuration parameters. See the documentation in the `docs/` directory for more details.

### Integrating with Other Systems

The modular design allows for easy integration with other systems. The orchestrator can be modified to incorporate additional agents or data sources.

## Troubleshooting

Common issues and solutions:

- **API rate limiting**: If you encounter rate limiting, adjust the `--request_interval` parameter
- **Memory issues**: For large research tasks, use the `--chunk_size` parameter to process information in smaller batches
- **Missing dependencies**: Ensure all dependencies are installed with `pip install -r requirements.txt`

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT

## Author

[Your Name]

## Acknowledgements

- [LangChain](https://python.langchain.com/) for the agent framework
- [LangGraph](https://python.langchain.com/docs/langgraph) for workflow orchestration
- [Tavily](https://tavily.com/) for the search API
