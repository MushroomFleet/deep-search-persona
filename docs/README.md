# Deep Research Agentic Pipeline

A Python-based autonomous research pipeline powered by OpenRouter.ai and Grok-4-fast:online (or any other LLM model). This system uses agentic AI to plan, execute, and synthesize comprehensive research on any topic.

## Features

- **Autonomous Research Planning**: AI agent creates multi-step research plans
- **Agentic Decision Making**: Agent decides next actions based on current findings
- **Multi-Tool Search**: Integrate web search, academic search, and custom data sources
- **Iterative Refinement**: Agent refines queries based on intermediate results
- **Intelligent Synthesis**: Comprehensive report generation from all findings
- **Flexible Configuration**: Customize models, search depth, and behavior
- **Progress Tracking**: Save intermediate results and monitor research progress

## Architecture

```
research_pipeline/
├── config.py           # Configuration management
├── llm_client.py       # OpenRouter API client
├── research_agent.py   # Core agentic research logic
├── search_tools.py     # Search tool integrations
├── pipeline.py         # Main orchestrator
├── examples.py         # Usage examples
└── requirements.txt    # Dependencies
```

## Installation

1. Clone or download the pipeline:
```bash
cd research_pipeline
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
```
Then edit the `.env` file and add your actual API key.

**Note:** The `.env` file is automatically loaded by the application. You can still use environment variables directly if preferred (e.g., `export OPENROUTER_API_KEY="your-key"`).

## Web Search & Grounding

This project uses **OpenRouter's native web search feature** via the `:online` suffix:
- Simply add `:online` to any model name (e.g., `x-ai/grok-4-fast:online`)
- No separate search API keys needed (Brave, Serper, etc.)
- All LLM requests automatically benefit from web search and grounding
- This feature is built into OpenRouter and works with any supported model

Example:
```python
# Enable web search by adding :online suffix
pipeline = ResearchPipeline(model="x-ai/grok-4-fast:online")
```

## Quick Start

### Basic Usage

```python
from pipeline import ResearchPipeline

# Initialize pipeline
pipeline = ResearchPipeline()

# Execute research
query = "What are the latest developments in quantum computing?"
results = pipeline.execute(query)

# Access results
print(results['results']['final_report'])
```

### Command Line Usage

```bash
python pipeline.py "Your research question here"
```

## Configuration

### Default Model

The pipeline uses `x-ai/grok-4-fast:online` by default. You can change this in `config.py`:

```python
DEFAULT_MODEL: str = "x-ai/grok-4-fast:online"  # Grok model
```

### Other Available Models on OpenRouter

```python
# Anthropic models
"anthropic/claude-3.5-sonnet"
"anthropic/claude-3-opus"

# OpenAI models
"openai/gpt-4-turbo"
"openai/gpt-4"

# Other models
"google/gemini-pro"
"meta-llama/llama-3-70b-instruct"
```

### Configuration Options

Edit `config.py` to customize:

```python
class Config:
    # Model settings
    DEFAULT_MODEL = "x-ai/grok-4-fast:online"
    MODEL_TEMPERATURE = 0.7
    MAX_TOKENS = 4000
    
    # Research settings
    MAX_RESEARCH_ITERATIONS = 10
    MAX_SEARCH_QUERIES = 5
    SEARCH_RESULTS_PER_QUERY = 5
    
    # Agent settings
    MIN_CONFIDENCE_THRESHOLD = 0.7
    
    # Output settings
    OUTPUT_DIR = "./research_outputs"
    SAVE_INTERMEDIATE_RESULTS = True
```

## Components

### 1. LLM Client (`llm_client.py`)

Handles all interactions with OpenRouter API:
- Chat completions
- System/user prompts
- Token management
- Error handling

```python
from llm_client import OpenRouterClient

llm = OpenRouterClient(model="x-ai/grok-4-fast:online")
response = llm.generate_with_system_prompt(
    system_prompt="You are a research assistant",
    user_prompt="Explain quantum entanglement"
)
```

### 2. Research Agent (`research_agent.py`)

Core agentic component with autonomous capabilities:
- **Research Planning**: Creates structured research plans
- **Decision Making**: Decides next actions autonomously
- **Analysis**: Analyzes search results for insights
- **Synthesis**: Combines findings into coherent reports

```python
from research_agent import ResearchAgent

agent = ResearchAgent(llm)
plan = agent.plan_research("Your query")
decision = agent.decide_next_action(context)
analysis = agent.analyze_results(query, results)
report = agent.synthesize_findings(query)
```

### 3. Search Tools (`search_tools.py`)

Flexible search integrations:
- Web search (Brave, Serper)
- Academic search (Semantic Scholar, arXiv)
- Custom data sources

```python
from search_tools import SearchOrchestrator, WebSearchTool

search = SearchOrchestrator()
search.register_tool("web", WebSearchTool(api_key="your-key"))
results = search.search_and_combine("query")
```

### 4. Pipeline Orchestrator (`pipeline.py`)

Main coordinator that runs the full research process:
1. **Planning Phase**: Agent creates research plan
2. **Research Loop**: Iteratively search, analyze, decide
3. **Synthesis Phase**: Generate final comprehensive report
4. **Output Phase**: Save results in multiple formats

## Research Flow

```
┌─────────────────────────────────────────────────────┐
│ 1. PLANNING PHASE                                   │
│    - Agent analyzes query                           │
│    - Creates multi-step research plan               │
│    - Identifies key sub-questions                   │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│ 2. RESEARCH LOOP (Iterative)                        │
│    ┌─────────────────────────────────────────────┐  │
│    │ a) Agent Decides Next Action                │  │
│    │    - Search / Analyze / Refine / Complete   │  │
│    └─────────────────────────────────────────────┘  │
│                        ↓                             │
│    ┌─────────────────────────────────────────────┐  │
│    │ b) Execute Action                           │  │
│    │    - Perform search if needed               │  │
│    │    - Gather information                     │  │
│    └─────────────────────────────────────────────┘  │
│                        ↓                             │
│    ┌─────────────────────────────────────────────┐  │
│    │ c) Analyze Results                          │  │
│    │    - Extract key findings                   │  │
│    │    - Identify gaps                          │  │
│    │    - Assess confidence                      │  │
│    └─────────────────────────────────────────────┘  │
│                        ↓                             │
│    └──────────── Repeat until complete ─────────────┘
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│ 3. SYNTHESIS PHASE                                  │
│    - Combine all findings                           │
│    - Generate comprehensive report                  │
│    - Address original query                         │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│ 4. OUTPUT                                           │
│    - Save JSON results                              │
│    - Generate markdown report                       │
│    - Store intermediate steps                       │
└─────────────────────────────────────────────────────┘
```

## Output Format

The pipeline generates two main output files:

### 1. JSON Results (`research_YYYYMMDD_HHMMSS.json`)

```json
{
  "query": "Your research question",
  "model": "x-ai/grok-4-fast:online",
  "timestamp": "20250106_143022",
  "research_plan": [...],
  "research_steps": [
    {
      "step_number": 1,
      "phase": "searching",
      "query": "...",
      "confidence": 0.85,
      "results": {...}
    }
  ],
  "final_report": "...",
  "metadata": {
    "total_steps": 8,
    "avg_confidence": 0.82,
    "phases_completed": ["planning", "searching", "analyzing"]
  }
}
```

### 2. Markdown Report (`report_YYYYMMDD_HHMMSS.md`)

Human-readable research report with formatted findings.

## Advanced Usage

### Custom Research Plan

```python
from llm_client import OpenRouterClient
from research_agent import ResearchAgent

llm = OpenRouterClient()
agent = ResearchAgent(llm)

# Create custom plan
plan = agent.plan_research("Your complex query")

# Modify plan as needed
plan.append({
    "step": len(plan) + 1,
    "query": "Additional specific query",
    "reasoning": "Custom reasoning"
})

# Execute with custom plan
# (integrate into pipeline as needed)
```

### Integrating Custom Search Tools

```python
from search_tools import SearchTool, SearchOrchestrator

class CustomSearchTool(SearchTool):
    def search(self, query: str, num_results: int = 5):
        # Your custom search implementation
        return results

# Register in pipeline
search = SearchOrchestrator()
search.register_tool("custom", CustomSearchTool())
```

### Monitoring Progress

```python
pipeline = ResearchPipeline()

# Enable verbose logging
import logging
logging.basicConfig(level=logging.INFO)

# Execute with progress tracking
results = pipeline.execute(query)

# Check intermediate steps
for step in pipeline.agent.research_history:
    print(f"Step {step.step_number}: {step.confidence:.2f} confidence")
```

## Alternative Search API Integration (Optional)

**Note:** This project primarily uses OpenRouter's `:online` feature for web search. The following search tools are available but optional.

### Brave Search (Optional)

```python
from search_tools import WebSearchTool

web_search = WebSearchTool(
    api_key="your-brave-api-key",
    provider="brave"
)
```

Get Brave Search API: https://brave.com/search/api/

### Serper (Google Search) (Optional)

```python
web_search = WebSearchTool(
    api_key="your-serper-api-key",
    provider="serper"
)
```

Get Serper API: https://serper.dev/

**Recommended:** Use OpenRouter's `:online` feature instead by adding `:online` to your model name (e.g., `x-ai/grok-4-fast:online`).

## Examples

See `examples.py` for detailed usage examples:

```bash
python examples.py
```

Examples include:
1. Basic research
2. Custom model configuration
3. Real search API integration
4. Custom configuration
5. Step-by-step control
6. Output processing

## Troubleshooting

### API Key Issues

```python
# Verify API key is set
import os
print(os.getenv("OPENROUTER_API_KEY"))

# Or set programmatically
pipeline = ResearchPipeline(api_key="your-key")
```

### Model Not Available

Check available models at: https://openrouter.ai/models

### Search Results Empty

- Using mock search (no API key set)
- Check search API key configuration
- Verify search API quota/limits

### JSON Parsing Errors

- Agent responses are cleaned automatically
- Check `Config.MODEL_TEMPERATURE` (lower = more consistent)
- Review agent prompts in `research_agent.py`

## Extending the Pipeline

### Add New Research Phases

```python
from research_agent import ResearchPhase
from enum import Enum

class ExtendedPhase(Enum):
    VALIDATION = "validation"
    PEER_REVIEW = "peer_review"
```

### Add Custom Analysis

```python
def custom_analyzer(results):
    # Your custom analysis logic
    return analysis

# Integrate into pipeline
pipeline.custom_analysis = custom_analyzer
```

### Add Output Formats

```python
def save_as_pdf(report, filename):
    # Convert to PDF
    pass

# Use after synthesis
pipeline._save_results()
save_as_pdf(pipeline.final_report, "report.pdf")
```

## Best Practices

1. **Start Small**: Begin with 5 iterations, then scale up
2. **Monitor Confidence**: Check confidence scores in intermediate steps
3. **Review Plans**: Examine agent's research plan before full execution
4. **Iterate Prompts**: Adjust system prompts in agent for better results
5. **Save Intermediate**: Enable `SAVE_INTERMEDIATE_RESULTS` for debugging
6. **Use Appropriate Models**: Balance cost/speed with quality needs

## Cost Considerations

OpenRouter pricing varies by model:
- Grok models: Check current pricing at openrouter.ai
- Monitor token usage via OpenRouter dashboard
- Estimate: ~10-50k tokens per research session

## Contributing

To extend this pipeline:
1. Add new search tools in `search_tools.py`
2. Enhance agent logic in `research_agent.py`
3. Add phases/strategies in `pipeline.py`
4. Update configuration options in `config.py`

## License

This is a reference implementation. Adapt and use as needed.

## Resources

- OpenRouter Documentation: https://openrouter.ai/docs
- OpenRouter Models: https://openrouter.ai/models
- Grok Information: https://x.ai/
- API Keys: https://openrouter.ai/keys

## Support

For issues or questions:
1. Check the examples in `examples.py`
2. Review configuration in `config.py`
3. Examine agent prompts in `research_agent.py`
4. Monitor API logs from OpenRouter

---

**Happy Researching! 🔍🤖**
