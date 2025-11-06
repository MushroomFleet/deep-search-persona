# Quick Start Guide - Deep Research Pipeline

Get up and running in 5 minutes!

## 🚀 Installation

```bash
# 1. Navigate to the directory
cd research_pipeline

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set up environment variables
cp .env.example .env
# Then edit .env and add your API key
```

Get your API key: https://openrouter.ai/keys

**Note:** Open the newly created `.env` file and replace `your-openrouter-api-key-here` with your actual API key.

## 💡 Basic Usage

### Method 1: Python Script

```python
from pipeline import ResearchPipeline

# Initialize
pipeline = ResearchPipeline()

# Research!
results = pipeline.execute("What is quantum computing?")

# View report
print(results['results']['final_report'])
```

### Method 2: Command Line

```bash
# Basic research
python cli.py "What is quantum computing?"

# With custom iterations
python cli.py "AI safety" --iterations 10

# With different model
python cli.py "Climate change" --model anthropic/claude-3.5-sonnet
```

### Method 3: Run Examples

```bash
python examples.py
```

## 🎯 Common Use Cases

### Academic Research
```python
query = "Recent advances in transformer architectures"
pipeline = ResearchPipeline()
results = pipeline.execute(query, max_iterations=10)
```

### Business Intelligence
```python
query = "Market trends in electric vehicles 2024"
pipeline = ResearchPipeline()
results = pipeline.execute(query)
```

### Technical Investigation
```python
query = "Best practices for microservices architecture"
pipeline = ResearchPipeline()
results = pipeline.execute(query)
```

## 🔧 Configuration

Create a `.env` file:
```bash
OPENROUTER_API_KEY=your-key-here
```

### Web Search & Grounding

This project uses **OpenRouter's native `:online` feature**:
- Simply add `:online` to any model name
- Example: `x-ai/grok-4-fast:online`
- No separate search API keys needed
- All requests automatically get web search and grounding

Modify `config.py` to change settings:
```python
class Config:
    DEFAULT_MODEL = "x-ai/grok-4-fast:online"  # Enable web search with :online
    MAX_RESEARCH_ITERATIONS = 10  # More thorough research
    SEARCH_RESULTS_PER_QUERY = 5  # Results per search
```

## 📊 Understanding Outputs

### JSON Output (`research_YYYYMMDD_HHMMSS.json`)
```json
{
  "query": "Your question",
  "final_report": "Comprehensive answer...",
  "research_steps": [...],
  "metadata": {
    "total_steps": 8,
    "avg_confidence": 0.82
  }
}
```

### Markdown Report (`report_YYYYMMDD_HHMMSS.md`)
Human-readable research report with all findings.

## 🎓 Learn More

- **Full Documentation**: See `README.md`
- **Architecture Details**: See `ARCHITECTURE.md`
- **More Examples**: See `examples.py`

## ⚡ Tips for Better Results

1. **Be Specific**: "Latest transformer architectures in NLP" > "AI"
2. **Start Small**: Use 5 iterations first, then scale up
3. **Check Confidence**: Review confidence scores in results
4. **Use Right Model**: Balance cost/speed vs quality
5. **Save Intermediate**: Enable for debugging

## 🐛 Troubleshooting

**No API Key Error**
- Make sure you've created a `.env` file from `.env.example`
- Add your OpenRouter API key to the `.env` file

**Import Errors**
```bash
pip install -r requirements.txt
```

**Web Search Not Working**
- Ensure your model name includes the `:online` suffix
- Example: `x-ai/grok-4-fast:online`
- This enables OpenRouter's native web search feature

## 📞 Support

- Check `README.md` for detailed docs
- Review `examples.py` for code samples
- Examine `config.py` for settings
- See `ARCHITECTURE.md` for system design

---

**Happy Researching!** 🔍✨
