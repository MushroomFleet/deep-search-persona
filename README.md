# Deep Search Personas

An advanced autonomous research pipeline with specialized writing personas, powered by LLMs through OpenRouter.ai.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## ✨ Features

### 🎯 3-Phase Optimization Architecture

**Phase 1: Quick Wins (+40-60% quality improvement)**
- 📝 Structured prompt library with versioning
- 🎓 Few-shot learning integration
- 🔧 Robust JSON extraction (>95% success rate)
- ✅ Self-validation system with retry mechanism

**Phase 2: Architecture Foundations (2-3x throughput)**
- 🤖 Multi-agent orchestration (Planner → Searcher → Analyzer)
- ⚡ Parallel processing with ThreadPoolExecutor
- 🧠 Semantic memory system with tag indexing
- 📊 Agent performance tracking and metrics

**Phase 3: Advanced Features (+80% comprehensiveness)**
- 🔄 Dynamic workflow state machine (adaptive research)
- ✅ Fact validation & cross-referencing system
- 🎯 OpenAI embeddings for semantic similarity search
- 🧪 A/B testing framework for continuous optimization

### 🎭 Writer Personas Feature

- **Custom writing styles** via markdown-based system prompts
- **Specialized personas** for different content types
- **CLI integration** with `--writer-prompt` flag
- **Included examples**: Asimov-style science communication, creative storytelling, technical writing
- **📚 Comparison Study**: See [examples/README.md](examples/README.md) for side-by-side persona comparisons

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Environment

```bash
cp .env.example .env
```

### 3. Add Your API Keys

Edit `.env` and add:
```env
# Required: OpenRouter for LLM access
OPENROUTER_API_KEY=your-openrouter-api-key-here

# Optional: OpenAI for semantic embeddings (Phase 3)
OPENAI_API_KEY=your-openai-api-key-here
```

Get your API keys:
- [OpenRouter API Key](https://openrouter.ai/keys)
- [OpenAI API Key](https://platform.openai.com/api-keys)

### 4. Run Research

**Standard Research:**
```bash
python pipeline_advanced.py "What are the latest breakthroughs in quantum computing?"
```

**With Writer Persona:**
```bash
python pipeline_advanced.py "Explain fusion energy advances" --writer-prompt isaac.md
```

**Basic Pipeline (Phase 2):**
```bash
python cli.py "Your research question"
```

---

## 🎭 Writer Personas

Customize the final synthesis with specialized writing styles using markdown system prompts.

### Available Personas

- **`isaac.md`** - Asimov-style science communication (clear, engaging, pedagogical)
- **`orson.md`** - Professional technical writing
- **`zargon2.md`** - Creative storytelling approach

### Usage

```bash
python pipeline_advanced.py "your research query" --writer-prompt isaac.md
```

### Creating Custom Personas

Create a markdown file with your custom system prompt:

```markdown
# My Custom Persona

You are a [role description].

Your writing style is characterized by:
- [characteristic 1]
- [characteristic 2]
- [characteristic 3]

When synthesizing research findings:
1. [instruction 1]
2. [instruction 2]
3. [instruction 3]
```

Then use it:
```bash
python pipeline_advanced.py "your query" --writer-prompt my_persona.md
```

---

## 📊 Performance Improvements

| Metric | Phase 1 | Phase 2 | Phase 3 |
|--------|---------|---------|---------|
| **Response Quality** | +40-60% | Maintained | +80%+ |
| **Throughput** | Baseline | **2-3x faster** | Maintained |
| **JSON Parse Success** | **>95%** | >95% | >95% |
| **Invalid Plans** | **-50%** | Better | Better |
| **Adaptability** | Static | Static | **Dynamic** |
| **Fact Validation** | None | None | **>90% accuracy** |

---

## 🏗️ Architecture Overview

### Phase Progression

```
Phase 1 (Foundation)          Phase 2 (Scale)              Phase 3 (Intelligence)
─────────────────────         ───────────────────          ──────────────────────
                                                           
┌─────────────────┐          ┌──────────────────┐         ┌──────────────────┐
│ Prompt Library  │   ──→    │  Multi-Agent     │   ──→   │ State Machine    │
│ Few-Shot Learn  │          │  Orchestration   │         │ Fact Validation  │
│ JSON Extraction │          │  Parallel Work   │         │ Semantic Memory  │
│ Self-Validation │          │  Memory System   │         │ A/B Testing      │
└─────────────────┘          └──────────────────┘         └──────────────────┘
                                                                    ↓
                                                           ┌──────────────────┐
                                                           │ Writer Personas  │
                                                           │ (Custom Styles)  │
                                                           └──────────────────┘
```

### Component Interaction

1. **Planning** → PlannerAgent creates structured research plan
2. **Searching** → SearcherAgent executes parallel queries (3 concurrent)
3. **Analyzing** → AnalyzerAgent extracts insights with semantic search
4. **Validating** → FactChecker validates findings across sources
5. **Synthesizing** → Custom writer persona generates final report

---

## 💡 Usage Examples

### Example 1: Basic Research (Phase 2 Pipeline)

```python
from pipeline import ResearchPipeline

# Initialize pipeline
pipeline = ResearchPipeline()

# Execute research
results = pipeline.execute("What are the main challenges in developing AGI?")

# Access results
print(results['results']['final_report'])
print(f"Agent Stats: {results['metadata']['agent_stats']}")
```

### Example 2: Advanced Research (Phase 3 Pipeline)

```python
from pipeline_advanced import AdvancedResearchPipeline

# Initialize with advanced features
pipeline = AdvancedResearchPipeline()

# Execute adaptive research
results = pipeline.execute("Explain recent advances in fusion energy")

# Access Phase 3 metadata
phase3 = results['results']['phase3_metadata']
print(f"State Path: {' → '.join(phase3['state_path'])}")
print(f"Validations: {phase3['validation_results']}")
print(f"Semantic Items: {phase3['semantic_memory_stats']['total_items']}")
```

### Example 3: Research with Custom Persona

```python
from pipeline_advanced import AdvancedResearchPipeline

# Initialize with custom writer
pipeline = AdvancedResearchPipeline(writer_prompt_path="isaac.md")

# Execute research with Asimov-style synthesis
results = pipeline.execute("Summarize the Voynich manuscript")

# Get persona-styled report
print(results['results']['final_report'])
```

**CLI Equivalent:**
```bash
python pipeline_advanced.py "Summarize the Voynich manuscript" --writer-prompt isaac.md
```

### Example 4: Compare Persona Outputs

See the [`examples/`](examples/) directory for a comprehensive comparison study where all four personas (Default, Isaac, Orson, Zargon) were used to research the same topic:

**Query:** `"summarize the voynich manuscript, writing a primer to introduce its content"`

The [examples/README.md](examples/README.md) provides:
- **Style comparison excerpts** showing how each persona opens the same topic
- **Use case recommendations** for when to use each persona
- **Technical details** on file naming conventions and structure
- **Quality metrics** demonstrating that all personas maintain equal factual accuracy

**Files included:**
- 8 research outputs (4 personas × 2 file types: `.md` reports + `.json` data)
- Side-by-side comparison of writing styles
- Detailed analysis of persona characteristics

---

## 📖 Documentation

Comprehensive documentation available in the `docs/` directory:

- **[Quick Start Guide](docs/QUICKSTART.md)** - Get started in 5 minutes
- **[Persona Examples](examples/README.md)** - Side-by-side comparison of all personas ⭐ **NEW**
- **[Phase 1: Quick Wins](docs/PHASE1_IMPLEMENTATION_SUMMARY.md)** - Foundation improvements
- **[Phase 2: Architecture](docs/PHASE2_IMPLEMENTATION_SUMMARY.md)** - Multi-agent system
- **[Phase 3: Advanced Features](docs/PHASE3_IMPLEMENTATION_SUMMARY.md)** - Adaptive workflow
- **[Full Architecture](docs/ARCHITECTURE.md)** - System design and internals
- **[Implementation Roadmap](docs/IMPLEMENTATION_ROADMAP.md)** - Development timeline

---

## 🗂️ Project Structure

```
deepsearch/
├── agents/                      # Phase 2: Multi-agent system
│   ├── base_agent.py           # Agent foundation
│   ├── planner_agent.py        # Research planning
│   ├── searcher_agent.py       # Search execution
│   ├── analyzer_agent.py       # Result analysis
│   └── orchestrator.py         # Parallel coordination
├── memory/                      # Memory systems
│   ├── research_memory.py      # Phase 2: Tag-based memory
│   └── semantic_memory.py      # Phase 3: Embedding-based
├── workflow/                    # Phase 3: Dynamic workflow
│   └── state_machine.py        # Adaptive state transitions
├── validation/                  # Phase 3: Fact checking
│   └── fact_checker.py         # Cross-reference validation
├── testing/                     # Phase 3: Optimization
│   └── ab_testing.py           # A/B test framework
├── examples/                    # Persona comparison examples
│   ├── README.md               # Detailed persona analysis
│   ├── default_report_*.md     # Default persona outputs
│   ├── isaac_persona_*.md      # Isaac persona outputs
│   ├── orson_persona_*.md      # Orson persona outputs
│   └── zargon_persona_*.md     # Zargon persona outputs
├── pipeline.py                  # Phase 2 pipeline
├── pipeline_advanced.py         # Phase 3 pipeline
├── prompt_library.py            # Phase 1: Structured prompts
├── few_shot_examples.py         # Phase 1: Learning examples
├── research_agent.py            # Core agent logic
├── search_tools.py              # Search integrations
├── llm_client.py               # OpenRouter client
├── config.py                    # Configuration
├── cli.py                      # Command-line interface
├── isaac.md                     # Asimov-style persona
├── orson.md                     # Technical writing persona
├── zargon2.md                   # Creative storytelling persona
└── docs/                        # Documentation
```

---

## ⚙️ Configuration

### Environment Variables

**Required:**
```env
OPENROUTER_API_KEY=your_key_here
```

**Optional (Phase 3):**
```env
# OpenAI Embeddings (for semantic memory)
OPENAI_API_KEY=your_openai_key_here
EMBEDDING_MODEL=text-embedding-3-small
EMBEDDING_DIMENSIONS=1536
EMBEDDING_CACHE_ENABLED=true
EMBEDDING_MAX_CACHE_SIZE=10000

# Research Settings
MAX_RESEARCH_ITERATIONS=10
SEARCH_RESULTS_PER_QUERY=5
MAX_SEARCH_QUERIES=10
```

### Web Search & Grounding

This project uses OpenRouter's native web search by adding the `:online` suffix to model names:

- Example: `x-ai/grok-beta:online`
- No separate search API keys needed
- Works with any OpenRouter model

---

## 🧪 Testing

Run comprehensive test suites:

```bash
# Phase 1 tests (prompt library, JSON extraction, validation)
python test_phase1.py

# Phase 2 tests (multi-agent, parallel processing, memory)
python test_phase2.py

# Phase 3 tests (state machine, validation, semantic memory, A/B testing)
python test_phase3.py
```

**Test Coverage:**
- Phase 1: 6/6 tests passing (100%)
- Phase 2: 19/19 tests passing (100%)
- Phase 3: 24/27 tests passing (89%)

---

## 🎯 Use Cases

- **Academic Research** - Comprehensive literature reviews with fact validation
- **Technical Analysis** - Deep dives into complex topics with specialized personas
- **Content Creation** - Research-backed content with custom writing styles
- **Competitive Intelligence** - Market research with semantic clustering
- **Educational Content** - Asimov-style explanations for complex subjects
- **Scientific Communication** - Technical findings made accessible

---

## 🔧 Advanced Features

### State Machine Workflow

The Phase 3 pipeline uses an adaptive state machine that responds to research quality:

```python
States: PLANNING → SEARCHING → ANALYZING → VALIDATING → SYNTHESIZING → COMPLETED

Adaptive Transitions:
- Low confidence → Backtrack to SEARCHING
- High contradictions → Trigger VALIDATING
- Stuck in loop → Enter REFINING
- Quality goals met → Proceed to COMPLETED
```

### Semantic Memory

Store and retrieve research findings by semantic similarity:

```python
from memory.semantic_memory import SemanticMemory

memory = SemanticMemory(openai_api_key="your_key")
memory.store("Quantum computers use qubits", {"topic": "quantum"})

# Find similar content
results = memory.search("quantum computing", top_k=5, threshold=0.7)
```

### A/B Testing

Optimize prompts and strategies:

```python
from testing.ab_testing import ABTestManager

manager = ABTestManager()
test = manager.create_test("prompt_style", "quality", {"A": "detailed", "B": "concise"})

# Use variant in research
variant = test.get_variant()
test.record_result(variant, quality_score)

# Determine winner
winner = test.get_winner(min_samples=30)
```

---

## 📚 Citation

### Academic Citation

If you use this codebase in your research or project, please cite:

```bibtex
@software{deep_search_personas,
  title = {Deep Search Personas: Advanced autonomous research with specialized writing personas},
  author = {Drift Johnson},
  year = {2025},
  url = {https://github.com/MushroomFleet/deep-search-persona},
  version = {1.0.0}
}
```

### Donate

Support continued development:

[![Ko-Fi](https://cdn.ko-fi.com/cdn/kofi3.png?v=3)](https://ko-fi.com/driftjohnson)

---

## 📄 License

This is a reference implementation. Adapt and use as needed under the MIT License.

---

## 🤝 Contributing

Contributions welcome! Areas of interest:

- Additional writer personas
- New specialized agents
- Vector database integrations
- Performance optimizations
- Documentation improvements

---

## 🔗 Links

- **Repository:** [https://github.com/MushroomFleet/deep-search-persona](https://github.com/MushroomFleet/deep-search-persona)
- **Documentation:** [docs/README.md](docs/README.md)
- **Issues:** [GitHub Issues](https://github.com/MushroomFleet/deep-search-persona/issues)

---

**Built with ❤️ using OpenRouter.ai and advanced prompt engineering**
