# Deep Search Frontend

A modern React + TypeScript web interface for the Deep Search research pipeline, featuring real-time progress updates and persona-based synthesis.

## ⚠️ Prerequisites

This frontend is a **wrapper interface** for the Deep Search Python pipeline. You **must** have the main Deep Search project installed and working before using this frontend.

### Required Software

1. **Main Deep Search Project** - Fully installed and configured
   - Python 3.12+
   - All dependencies from main `requirements.txt`
   - Working `pipeline_advanced.py` script
   - Valid API keys configured (OpenAI, X.AI, etc.)

2. **Node.js & npm**
   - Node.js 20+ (LTS recommended)
   - npm 8+ (comes with Node.js)

3. **Python for Backend API**
   - Same Python environment as main project
   - Flask & dependencies (installed via `api/requirements.txt`)

## 🚀 Installation

### 1. Install Frontend Dependencies

From the `frontend/` directory:

```bash
npm install
```

### 2. Install Backend API Dependencies

The Flask API requires additional Python packages:

```bash
cd frontend/api
pip install -r requirements.txt
```

### 3. Configure Environment

Copy the example environment file:

```bash
cp .env.example .env
```

The default configuration should work for local development:
```env
VITE_API_BASE_URL=http://localhost:5000
VITE_WS_URL=http://localhost:5000
VITE_DEBUG=false
VITE_MAX_FILE_SIZE=1048576
VITE_PERSONA_EXTENSIONS=.md,.markdown,.txt
```

## 🎯 Running the Application

You need **TWO terminal windows** running simultaneously:

### Terminal 1: Flask API Server

```bash
cd frontend/api
python server.py
```

Expected output:
```
* Running on http://127.0.0.1:5000
* Debug mode: on
```

### Terminal 2: Vite Dev Server

```bash
cd frontend
npm run dev
```

Expected output:
```
VITE v7.x.x  ready in xxx ms

  ➜  Local:   http://localhost:3000/
  ➜  Network: use --host to expose
```

### Access the Application

Open your browser to: **http://localhost:3000**

## 📁 Project Structure

```
frontend/
├── api/                      # Flask backend API
│   ├── routes/              # API endpoints
│   │   ├── research.py      # Research pipeline routes
│   │   └── persona.py       # Persona management routes
│   ├── services/            # Business logic
│   │   ├── pipeline_service.py   # Pipeline execution
│   │   └── file_service.py       # File operations
│   ├── uploads/             # Uploaded persona files
│   └── server.py            # Flask app entry point
│
├── src/                     # React frontend
│   ├── components/          # UI components
│   │   ├── common/         # Reusable components
│   │   ├── features/       # Feature components
│   │   └── layout/         # Layout components
│   ├── hooks/              # Custom React hooks
│   ├── services/           # API client services
│   ├── stores/             # Zustand state management
│   ├── types/              # TypeScript definitions
│   └── styles/             # Global styles
│
└── docs/                    # Implementation documentation
    ├── PHASE1_FOUNDATION_SETUP.md
    ├── PHASE2_UI_COMPONENTS.md
    ├── PHASE3_BACKEND_INTEGRATION.md
    └── PHASE4_STATE_MANAGEMENT.md
```

## 🏗️ Architecture

### How It Works

```
React UI (localhost:3000)
    ↓ HTTP/SSE
Flask API (localhost:5000)
    ↓ subprocess.Popen()
pipeline_advanced.py (Main Project)
    ↓
Deep Search Pipeline (agents, workflow, memory, etc.)
```

**The frontend does NOT reimplement the pipeline** - it wraps the existing `pipeline_advanced.py` script via subprocess, streaming real-time output through Server-Sent Events (SSE).

### Technology Stack

**Frontend:**
- React 19.1 + TypeScript
- Vite (build tool)
- Tailwind CSS (styling)
- Zustand (state management)
- React Markdown (results rendering)
- FontAwesome (icons)

**Backend API:**
- Flask (Python web framework)
- Server-Sent Events (real-time streaming)
- Subprocess (pipeline execution)

## 🎨 Features

### ✅ Research Execution
- Enter research prompts
- Select/upload persona markdown files
- Run `pipeline_advanced.py` with persona support
- Real-time progress updates via SSE

### ✅ Live Progress Tracking
- Current workflow state (Planning → Searching → Analyzing → Validating → Synthesizing)
- Iteration counter
- Confidence & coverage metrics
- State transition logs

### ✅ Results Display
- Full markdown-rendered research reports
- Metadata badges (iterations, transitions, semantic items)
- Download reports as markdown files
- Syntax-highlighted code blocks

### ✅ Persona Management
- Upload custom writer personas (.md files)
- List available personas
- Select persona for synthesis
- Delete personas

## 🛠️ Development

### Build for Production

```bash
npm run build
```

Output will be in `dist/` directory.

### Linting

```bash
npm run lint
```

### Preview Production Build

```bash
npm run preview
```

## 🐛 Troubleshooting

### Issue: "Connection error" when submitting research

**Solution:** Ensure Flask API is running on port 5000:
```bash
cd frontend/api
python server.py
```

### Issue: "Pipeline failed: Unicode error"

**Solution:** This has been fixed in `pipeline_service.py`. Restart the Flask server:
- Stop Flask (Ctrl+C)
- Start again: `python server.py`

### Issue: Progress not updating in real-time

**Solution:** Restart Flask server. The fix for unbuffered Python output should now be active.

### Issue: "Module not found" errors

**Solution:** Install missing dependencies:
```bash
# Frontend
npm install

# Backend API
cd frontend/api
pip install -r requirements.txt
```

### Issue: Personas not uploading

**Solution:** Check that `frontend/api/uploads/` directory exists and is writable.

## 📝 Usage Example

1. Start both servers (Flask + Vite)
2. Open http://localhost:3000
3. Enter a research query: `"Explain quantum computing in 2025"`
4. (Optional) Upload a persona file like `isaac.md` from the main project
5. Click "Start Research"
6. Watch real-time progress as the pipeline executes
7. View the rendered markdown report
8. Download the report if needed

## 🔗 Related Documentation

- Main Project: `../README.md` (project root)
- Pipeline Documentation: `../docs/` 
- Implementation Phases: `./docs/PHASE*.md`
- NSL Branding Guide: `../ref/nsl-app-branding-guidance.md`

## 📄 License

Same as main Deep Search project.

## 🤝 Contributing

This frontend wraps the main Deep Search pipeline. For pipeline improvements, contribute to the main project.

For frontend-specific improvements:
1. Follow the NSL branding guidelines
2. Maintain TypeScript strict mode
3. Use Tailwind CSS for styling
4. Update relevant phase documentation in `docs/`

---

**Note:** This frontend requires a working Deep Search installation at the project root level. It does not function as a standalone application.
