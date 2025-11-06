# Do Not Upload - Repository Structure Guide

**Purpose:** This document shows the complete folder structure of the Deep Research Pipeline project, marking files and folders that should **NOT** be uploaded to GitHub with a ❌ symbol.

**For Users:** When you clone this repository, the files marked with ❌ will not be present - they are either generated during installation/runtime or are user-specific configurations.

---

## Complete Project Structure

```
deepsearch/
├── README.md
├── setup.py
├── requirements.txt
├── env.example
├── .env ❌                                    # DO NOT UPLOAD - Contains API keys
├── .gitignore
├── __init__.py
│
├── cli.py                                      # Command-line interface
├── config.py                                   # Configuration management
├── llm_client.py                               # OpenRouter API client
├── research_agent.py                           # Core agentic research logic
├── search_tools.py                             # Search tool integrations
├── pipeline.py                                 # Main orchestrator (Phase 1-2)
├── pipeline_advanced.py                        # Advanced pipeline (Phase 3)
├── examples.py                                 # Usage examples
│
├── prompt_library.py                           # Phase 1: Structured prompts
├── few_shot_examples.py                        # Phase 1: Few-shot learning
│
├── test_phase1.py                              # Phase 1 test suite
├── test_phase2.py                              # Phase 2 test suite
├── test_phase3.py                              # Phase 3 test suite
│
├── isaac.md                                    # Project notes
├── orson.md                                    # Project notes
├── zargon2.md                                  # Project notes
│
├── agents/                                     # Phase 2: Multi-agent system
│   ├── __init__.py
│   ├── base_agent.py                          # Base agent class
│   ├── planner_agent.py                       # Planning specialist
│   ├── searcher_agent.py                      # Search specialist
│   ├── analyzer_agent.py                      # Analysis specialist
│   └── orchestrator.py                        # Agent coordinator
│
├── memory/                                     # Phase 2 & 3: Memory systems
│   ├── __init__.py
│   ├── research_memory.py                     # Phase 2: Short-term memory
│   └── semantic_memory.py                     # Phase 3: Semantic search
│
├── workflow/                                   # Phase 3: Dynamic workflow
│   ├── __init__.py
│   └── state_machine.py                       # Adaptive state machine
│
├── validation/                                 # Phase 3: Fact validation
│   ├── __init__.py
│   └── fact_checker.py                        # Fact-checking system
│
├── testing/                                    # Phase 3: A/B testing
│   ├── __init__.py
│   └── ab_testing.py                          # A/B test framework
│
├── docs/                                       # Documentation
│   ├── README.md                              # Main documentation
│   ├── QUICKSTART.md                          # Quick start guide
│   ├── ARCHITECTURE.md                        # System architecture
│   ├── IMPLEMENTATION_ROADMAP.md              # Implementation plan
│   │
│   ├── 007.md                                 # Consulting notes
│   │
│   ├── PHASE1_QUICK_WINS.md                   # Phase 1 guide
│   ├── PHASE1_IMPLEMENTATION_SUMMARY.md       # Phase 1 summary
│   │
│   ├── PHASE2_ARCHITECTURE.md                 # Phase 2 guide
│   ├── PHASE2_IMPLEMENTATION_SUMMARY.md       # Phase 2 summary
│   │
│   ├── PHASE3_ADVANCED.md                     # Phase 3 guide
│   ├── PHASE3_IMPLEMENTATION_SUMMARY.md       # Phase 3 summary
│   ├── PHASE3_BUGFIXES.md                     # Phase 3 bug fixes
│   │
│   └── do-not-upload.md                       # This file
│
├── ref/ ❌                                     # DO NOT UPLOAD - Reference materials
│
├── research_outputs/ ❌                        # DO NOT UPLOAD - Generated research results
│   ├── research_YYYYMMDD_HHMMSS.json ❌
│   └── report_YYYYMMDD_HHMMSS.md ❌
│
│
├── __pycache__/ ❌                             # DO NOT UPLOAD - Python bytecode cache
│   ├── *.pyc ❌
│   ├── *.pyo ❌
│   └── *.pyd ❌
│
├── venv/ ❌                                    # DO NOT UPLOAD - Virtual environment
├── env/ ❌                                     # DO NOT UPLOAD - Virtual environment
├── .venv/ ❌                                   # DO NOT UPLOAD - Virtual environment
├── ENV/ ❌                                     # DO NOT UPLOAD - Virtual environment
│
├── build/ ❌                                   # DO NOT UPLOAD - Build artifacts
├── dist/ ❌                                    # DO NOT UPLOAD - Distribution packages
├── *.egg-info/ ❌                              # DO NOT UPLOAD - Python package info
│
├── .vscode/ ❌                                 # DO NOT UPLOAD - VS Code settings
├── .idea/ ❌                                   # DO NOT UPLOAD - PyCharm settings
│
├── .DS_Store ❌                                # DO NOT UPLOAD - macOS file
├── Thumbs.db ❌                                # DO NOT UPLOAD - Windows file
│
└── *.log ❌                                    # DO NOT UPLOAD - Log files
```

---

## Files/Folders That Should NOT Be Uploaded (❌)

### 1. Environment & Secrets
- **`.env`** ❌ - Contains API keys and secrets (use `env.example` as template)

### 2. Python Build Artifacts
- **`__pycache__/`** ❌ - Python bytecode cache
- **`*.pyc`** ❌ - Compiled Python files
- **`*.pyo`** ❌ - Optimized Python files
- **`*.pyd`** ❌ - Python DLL files
- **`build/`** ❌ - Build directory
- **`dist/`** ❌ - Distribution packages
- **`*.egg-info/`** ❌ - Python package metadata
- **`.Python`** ❌ - Python symbolic link
- **`*.egg`** ❌ - Python egg files

### 3. Virtual Environments
- **`venv/`** ❌ - Virtual environment folder
- **`env/`** ❌ - Virtual environment folder
- **`.venv/`** ❌ - Virtual environment folder
- **`ENV/`** ❌ - Virtual environment folder

### 4. IDE Configuration
- **`.vscode/`** ❌ - Visual Studio Code settings
- **`.idea/`** ❌ - PyCharm/IntelliJ settings
- **`*.swp`** ❌ - Vim swap files
- **`*.swo`** ❌ - Vim swap files
- **`*~`** ❌ - Backup files

### 5. Operating System Files
- **`.DS_Store`** ❌ - macOS folder settings
- **`Thumbs.db`** ❌ - Windows thumbnail cache

### 6. Generated Outputs
- **`research_outputs/`** ❌ - Research results (generated at runtime)
  - `research_YYYYMMDD_HHMMSS.json` ❌
  - `report_YYYYMMDD_HHMMSS.md` ❌

### 7. Reference Materials
- **`ref/`** ❌ - Reference materials (user-specific)

### 8. Logs
- **`*.log`** ❌ - Log files

---

## Installation Checklist

When you clone this repository, verify you have:

### ✅ Core Files Present
- [ ] `requirements.txt` - Python dependencies
- [ ] `env.example` - Environment variable template
- [ ] `README.md` - Main documentation
- [ ] `setup.py` - Package setup file
- [ ] All `.py` source files in root directory
- [ ] All subdirectories: `agents/`, `memory/`, `workflow/`, `validation/`, `testing/`
- [ ] All documentation in `docs/`

### ✅ Dependencies Installed
```bash
pip install -r requirements.txt
```

**Required packages:**
- `requests>=2.31.0` - HTTP library for API calls
- `python-dotenv>=1.0.0` - Environment variable management
- `dataclasses-json>=0.6.0` - JSON serialization
- `openai>=1.0.0` - OpenAI embeddings (Phase 3)
- `numpy>=1.24.0` - Numerical computing (Phase 3)

### ✅ Environment Configuration
1. Copy environment template:
   ```bash
   cp env.example .env
   ```

2. Edit `.env` and add your API keys:
   ```bash
   OPENROUTER_API_KEY=your-openrouter-api-key-here
   OPENAI_API_KEY=your-openai-api-key-here  # Optional, for embeddings
   ```

3. **IMPORTANT:** Never commit the `.env` file to version control!

### ✅ Directory Structure Created
After running the pipeline for the first time, these directories will be created automatically:
- `research_outputs/` ❌ - Research results (do not upload)

---

## Quick Verification Script

Run this to verify your installation:

```bash
# Check Python version (3.8+ required)
python --version

# Check all dependencies installed
pip list | grep -E "requests|python-dotenv|dataclasses-json|openai|numpy"

# Verify .env exists (but don't show contents!)
test -f .env && echo "✅ .env file found" || echo "❌ .env file missing"

# Check directory structure
test -d agents && echo "✅ agents/ directory found" || echo "❌ agents/ missing"
test -d memory && echo "✅ memory/ directory found" || echo "❌ memory/ missing"
test -d workflow && echo "✅ workflow/ directory found" || echo "❌ workflow/ missing"
test -d validation && echo "✅ validation/ directory found" || echo "❌ validation/ missing"
test -d testing && echo "✅ testing/ directory found" || echo "❌ testing/ missing"
test -d docs && echo "✅ docs/ directory found" || echo "❌ docs/ missing"
```

---

## Requirements Validation

### Phase 1 Requirements ✅
- [x] `prompt_library.py` - Structured prompt templates
- [x] `few_shot_examples.py` - Few-shot learning examples
- [x] Updated `research_agent.py` - Robust JSON extraction
- [x] `test_phase1.py` - Test suite

### Phase 2 Requirements ✅
- [x] `agents/base_agent.py` - Agent foundation
- [x] `agents/planner_agent.py` - Planning specialist
- [x] `agents/searcher_agent.py` - Search specialist
- [x] `agents/analyzer_agent.py` - Analysis specialist
- [x] `agents/orchestrator.py` - Multi-agent coordinator
- [x] `memory/research_memory.py` - Memory system
- [x] `test_phase2.py` - Test suite

### Phase 3 Requirements ✅
- [x] `workflow/state_machine.py` - Dynamic workflow
- [x] `validation/fact_checker.py` - Fact validation
- [x] `memory/semantic_memory.py` - Semantic search
- [x] `testing/ab_testing.py` - A/B testing framework
- [x] `pipeline_advanced.py` - Advanced pipeline
- [x] `test_phase3.py` - Test suite

### Core Pipeline Requirements ✅
- [x] `llm_client.py` - OpenRouter API client
- [x] `research_agent.py` - Research agent logic
- [x] `search_tools.py` - Search integrations
- [x] `pipeline.py` - Main orchestrator
- [x] `config.py` - Configuration management
- [x] `cli.py` - Command-line interface

---

## What Gets Tracked in Git

**✅ DO UPLOAD (Tracked):**
- All `.py` source files
- `requirements.txt`
- `env.example` (template only)
- `README.md` and all documentation
- `.gitignore`
- `setup.py`

**❌ DO NOT UPLOAD (Gitignored):**
- `.env` (contains secrets)
- `__pycache__/` and `*.pyc` (build artifacts)
- `venv/`, `env/`, `.venv/` (virtual environments)
- `research_outputs/` (generated results)
- IDE settings (`.vscode/`, `.idea/`)
- OS files (`.DS_Store`, `Thumbs.db`)
- Log files (`*.log`)

---

## Notes for Contributors

1. **Never commit `.env`** - Use `env.example` as a template
2. **Test before committing** - Run test suites: `python test_phase1.py`, etc.
3. **Update requirements.txt** - If you add new dependencies
4. **Document changes** - Update relevant docs in `docs/`
5. **Clean build artifacts** - Run `find . -type d -name __pycache__ -exec rm -rf {} +` before committing

---

## Summary

This file serves as a reference to ensure:
- ✅ Users know exactly which files should be in the repository
- ✅ All required dependencies are documented
- ✅ Sensitive files (like `.env`) are never uploaded
- ✅ Build artifacts and generated files are excluded
- ✅ Installation can be verified step-by-step

**Remember:** Files marked with ❌ should NEVER be committed to version control!
