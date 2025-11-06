# Phase 1: Foundation & Setup

## Overview
This phase establishes the foundation for the Deep Search Frontend application, including project initialization, build tooling, and NSL branding integration.

## Prerequisites
- Node.js 18+ and npm/yarn/pnpm installed
- Python 3.8+ (for backend bridge in later phases)
- Visual Studio Code or preferred IDE

---

## 1. Project Initialization

### 1.1 Create Vite + React + TypeScript Project

```bash
# Navigate to frontend directory
cd frontend

# Create Vite project with React + TypeScript template
npm create vite@latest . -- --template react-ts

# Install dependencies
npm install
```

### 1.2 Project Structure
```
frontend/
├── docs/                           # Phase documentation (current)
├── public/                         # Static assets
│   └── favicon.ico
├── src/
│   ├── assets/                     # Images, fonts, etc.
│   ├── components/                 # React components
│   │   ├── common/                 # Reusable components
│   │   ├── layout/                 # Layout components
│   │   └── features/               # Feature-specific components
│   ├── hooks/                      # Custom React hooks
│   ├── services/                   # API services
│   ├── types/                      # TypeScript type definitions
│   ├── utils/                      # Utility functions
│   ├── styles/                     # Global styles
│   │   └── globals.css             # NSL branding CSS
│   ├── App.tsx                     # Root component
│   ├── main.tsx                    # Entry point
│   └── vite-env.d.ts              # Vite type declarations
├── api/                            # Python backend bridge (Phase 3)
├── .env.example                    # Environment variables template
├── .gitignore
├── index.html                      # HTML entry point
├── package.json
├── tsconfig.json                   # TypeScript configuration
├── tsconfig.node.json
├── vite.config.ts                  # Vite configuration
└── tailwind.config.ts              # Tailwind CSS configuration
```

---

## 2. Install Core Dependencies

### 2.1 UI & Styling Dependencies

```bash
# Tailwind CSS and utilities
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p

# Tailwind CSS animations plugin
npm install tailwindcss-animate

# FontAwesome
npm install @fortawesome/fontawesome-svg-core \
            @fortawesome/free-solid-svg-icons \
            @fortawesome/free-regular-svg-icons \
            @fortawesome/react-fontawesome
```

### 2.2 Routing & State Management

```bash
# React Router for navigation
npm install react-router-dom

# Zustand for state management (lightweight alternative to Redux)
npm install zustand
```

### 2.3 Utilities & Features

```bash
# Markdown rendering
npm install react-markdown remark-gfm rehype-raw

# File upload
npm install react-dropzone

# Date formatting
npm install date-fns

# Class name utility
npm install clsx
```

### 2.4 TypeScript Type Definitions

```bash
npm install -D @types/node
```

---

## 3. Tailwind CSS Configuration

### 3.1 Create `tailwind.config.ts`

```typescript
import type { Config } from "tailwindcss";

export default {
  darkMode: ["class"],
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        border: "hsl(var(--border))",
        input: "hsl(var(--input))",
        ring: "hsl(var(--ring))",
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        primary: {
          DEFAULT: "hsl(var(--primary))",
          foreground: "hsl(var(--primary-foreground))",
          glow: "hsl(var(--primary-glow))",
        },
        secondary: {
          DEFAULT: "hsl(var(--secondary))",
          foreground: "hsl(var(--secondary-foreground))",
        },
        destructive: {
          DEFAULT: "hsl(var(--destructive))",
          foreground: "hsl(var(--destructive-foreground))",
        },
        muted: {
          DEFAULT: "hsl(var(--muted))",
          foreground: "hsl(var(--muted-foreground))",
        },
        accent: {
          DEFAULT: "hsl(var(--accent))",
          foreground: "hsl(var(--accent-foreground))",
          glow: "hsl(var(--accent-glow))",
        },
        success: {
          DEFAULT: "hsl(var(--success))",
          foreground: "hsl(var(--success-foreground))",
        },
        popover: {
          DEFAULT: "hsl(var(--popover))",
          foreground: "hsl(var(--popover-foreground))",
        },
        card: {
          DEFAULT: "hsl(var(--card))",
          foreground: "hsl(var(--card-foreground))",
        },
      },
      borderRadius: {
        lg: "var(--radius)",
        md: "calc(var(--radius) - 2px)",
        sm: "calc(var(--radius) - 4px)",
      },
      keyframes: {
        "accordion-down": {
          from: { height: "0" },
          to: { height: "var(--radix-accordion-content-height)" },
        },
        "accordion-up": {
          from: { height: "var(--radix-accordion-content-height)" },
          to: { height: "0" },
        },
        glow: {
          "0%": { boxShadow: "0 0 20px hsl(263 70% 60% / 0.3)" },
          "100%": { boxShadow: "0 0 40px hsl(263 80% 70% / 0.5)" },
        },
        "slide-up": {
          "0%": { opacity: "0", transform: "translateY(20px)" },
          "100%": { opacity: "1", transform: "translateY(0)" },
        },
      },
      animation: {
        "accordion-down": "accordion-down 0.2s ease-out",
        "accordion-up": "accordion-up 0.2s ease-out",
        glow: "glow 2s ease-in-out infinite alternate",
        "slide-up": "slideUp 0.5s ease-out",
      },
    },
  },
  plugins: [require("tailwindcss-animate")],
} satisfies Config;
```

### 3.2 Create `src/styles/globals.css`

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  :root {
    /* NSL Branding - Dark Theme */
    --background: 250 24% 10%;
    --foreground: 250 10% 98%;
    
    --card: 250 20% 14%;
    --card-foreground: 250 10% 98%;
    
    --popover: 250 24% 12%;
    --popover-foreground: 250 10% 98%;
    
    --primary: 263 70% 60%;
    --primary-foreground: 250 10% 98%;
    --primary-glow: 263 80% 70%;
    
    --secondary: 250 15% 20%;
    --secondary-foreground: 250 10% 98%;
    
    --muted: 250 15% 18%;
    --muted-foreground: 250 10% 65%;
    
    --accent: 38 92% 50%;
    --accent-foreground: 250 24% 10%;
    --accent-glow: 38 100% 60%;
    
    --destructive: 0 72% 51%;
    --destructive-foreground: 250 10% 98%;
    
    --success: 142 71% 45%;
    --success-foreground: 250 10% 98%;
    
    --border: 250 15% 22%;
    --input: 250 15% 22%;
    --ring: 263 70% 60%;
    
    --radius: 0.75rem;
    
    /* Gradients */
    --gradient-primary: linear-gradient(135deg, hsl(263 70% 60%) 0%, hsl(263 80% 70%) 100%);
    --gradient-accent: linear-gradient(135deg, hsl(38 92% 50%) 0%, hsl(38 100% 60%) 100%);
    --gradient-subtle: linear-gradient(180deg, hsl(250 20% 14%) 0%, hsl(250 24% 10%) 100%);
    
    /* Shadows */
    --shadow-elegant: 0 10px 40px -10px hsl(263 70% 30% / 0.4);
    --shadow-glow: 0 0 40px hsl(263 80% 70% / 0.3);
    --shadow-accent: 0 4px 20px hsl(38 92% 50% / 0.3);
    
    /* Transitions */
    --transition-smooth: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  }
}

@layer base {
  * {
    @apply border-border;
  }

  body {
    @apply bg-background text-foreground;
    font-feature-settings: "rlig" 1, "calt" 1;
  }

  h1, h2, h3, h4, h5, h6 {
    @apply font-semibold tracking-tight;
  }
}

@layer utilities {
  .gradient-primary {
    background: var(--gradient-primary);
  }
  
  .gradient-accent {
    background: var(--gradient-accent);
  }
  
  .gradient-subtle {
    background: var(--gradient-subtle);
  }
  
  .shadow-elegant {
    box-shadow: var(--shadow-elegant);
  }
  
  .shadow-glow {
    box-shadow: var(--shadow-glow);
  }

  .shadow-accent {
    box-shadow: var(--shadow-accent);
  }
  
  .transition-smooth {
    transition: var(--transition-smooth);
  }

  .animate-glow {
    animation: glow 2s ease-in-out infinite alternate;
  }

  .animate-slide-up {
    animation: slide-up 0.5s ease-out;
  }
}

/* Custom Scrollbar (Dark Theme) */
::-webkit-scrollbar {
  width: 10px;
  height: 10px;
}

::-webkit-scrollbar-track {
  background: hsl(250 24% 10%);
}

::-webkit-scrollbar-thumb {
  background: hsl(250 15% 22%);
  border-radius: 5px;
}

::-webkit-scrollbar-thumb:hover {
  background: hsl(263 70% 60%);
}
```

---

## 4. TypeScript Configuration

### 4.1 Update `tsconfig.json`

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,

    /* Bundler mode */
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",

    /* Linting */
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,

    /* Path aliases */
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"],
      "@/components/*": ["./src/components/*"],
      "@/hooks/*": ["./src/hooks/*"],
      "@/services/*": ["./src/services/*"],
      "@/types/*": ["./src/types/*"],
      "@/utils/*": ["./src/utils/*"]
    }
  },
  "include": ["src"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
```

### 4.2 Update `vite.config.ts` for Path Aliases

```typescript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
      '@/components': path.resolve(__dirname, './src/components'),
      '@/hooks': path.resolve(__dirname, './src/hooks'),
      '@/services': path.resolve(__dirname, './src/services'),
      '@/types': path.resolve(__dirname, './src/types'),
      '@/utils': path.resolve(__dirname, './src/utils'),
    },
  },
  server: {
    port: 3000,
    proxy: {
      // Proxy API requests to Python backend (Phase 3)
      '/api': {
        target: 'http://localhost:5000',
        changeOrigin: true,
      },
    },
  },
})
```

---

## 5. Type Definitions

### 5.1 Create `src/types/index.ts`

```typescript
/**
 * Core type definitions for Deep Search Frontend
 */

// Persona file representation
export interface Persona {
  id: string;
  name: string;
  filename: string;
  content: string;
  uploadedAt: Date;
}

// Research job configuration
export interface ResearchJob {
  id: string;
  query: string;
  persona?: Persona;
  status: JobStatus;
  createdAt: Date;
  startedAt?: Date;
  completedAt?: Date;
  error?: string;
}

// Job execution status
export enum JobStatus {
  PENDING = 'pending',
  RUNNING = 'running',
  COMPLETED = 'completed',
  FAILED = 'failed',
}

// Pipeline execution state (from workflow/state_machine.py)
export enum WorkflowState {
  PLANNING = 'planning',
  SEARCHING = 'searching',
  ANALYZING = 'analyzing',
  VALIDATING = 'validating',
  REFINING = 'refining',
  SYNTHESIZING = 'synthesizing',
  COMPLETED = 'completed',
  FAILED = 'failed',
}

// Real-time pipeline output message
export interface PipelineMessage {
  type: 'state' | 'progress' | 'result' | 'error';
  timestamp: Date;
  data: any;
}

// Progress update from pipeline
export interface ProgressUpdate {
  iteration: number;
  state: WorkflowState;
  confidence: number;
  coverage: number;
  contradictions: number;
  message: string;
}

// Final research results
export interface ResearchResult {
  query: string;
  final_report: string;
  research_history: ResearchStep[];
  phase3_metadata: Phase3Metadata;
  timestamp: string;
}

// Individual research step
export interface ResearchStep {
  step_number: number;
  query: string;
  confidence: number;
  results: {
    key_findings: Finding[];
    sources: Source[];
  };
}

// Research finding
export interface Finding {
  finding: string;
  source: string;
  confidence: number;
}

// Research source
export interface Source {
  title: string;
  url?: string;
  type: string;
}

// Phase 3 metadata
export interface Phase3Metadata {
  state_path: string[];
  total_transitions: number;
  validation_results: number;
  semantic_memory_stats: {
    total_items: number;
    cache_hits: number;
    cache_misses: number;
  };
  ab_test_results: Record<string, string>;
}
```

---

## 6. Environment Configuration

### 6.1 Create `.env.example`

```env
# Vite Environment Variables
# Copy this file to .env and update with your values

# API Base URL (Python backend)
VITE_API_BASE_URL=http://localhost:5000

# WebSocket/SSE URL
VITE_WS_URL=http://localhost:5000

# Enable debug mode
VITE_DEBUG=false

# Maximum file upload size (bytes)
VITE_MAX_FILE_SIZE=1048576

# Supported persona file extensions
VITE_PERSONA_EXTENSIONS=.md,.markdown,.txt
```

### 6.2 Create `.env`

```bash
cp .env.example .env
```

---

## 7. Entry Point Setup

### 7.1 Update `src/main.tsx`

```typescript
import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.tsx'
import './styles/globals.css'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
```

### 7.2 Update `index.html`

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/favicon.ico" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Deep Search - NSL Research Pipeline</title>
    <meta name="description" content="Advanced AI research pipeline with adaptive workflow and semantic memory" />
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
```

### 7.3 Create Basic `src/App.tsx`

```typescript
import { BrowserRouter } from 'react-router-dom'

function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-background text-foreground">
        <div className="container mx-auto px-4 py-8">
          <h1 className="text-4xl font-bold text-primary mb-4">
            Deep Search
          </h1>
          <p className="text-muted-foreground">
            NSL Research Pipeline - Phase 1 Foundation Complete
          </p>
        </div>
      </div>
    </BrowserRouter>
  )
}

export default App
```

---

## 8. Git Configuration

### 8.1 Update `.gitignore`

```gitignore
# Dependencies
node_modules/

# Build outputs
dist/
dist-ssr/

# Environment variables
.env
.env.local
.env.*.local

# Editor directories
.vscode/*
!.vscode/extensions.json
.idea/
*.swp
*.swo
*~

# OS files
.DS_Store
Thumbs.db

# Logs
*.log
npm-debug.log*
yarn-debug.log*
yarn-error.log*
pnpm-debug.log*

# Temp files
*.tmp
*.temp

# Uploaded persona files (temporary storage)
api/uploads/
api/temp/

# Python cache (for backend bridge)
__pycache__/
*.py[cod]
*$py.class
```

---

## 9. Package.json Scripts

### 9.1 Update `package.json` scripts

```json
{
  "name": "deepsearch-frontend",
  "version": "0.1.0",
  "private": true,
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview",
    "lint": "eslint . --ext ts,tsx --report-unused-disable-directives --max-warnings 0",
    "type-check": "tsc --noEmit"
  }
}
```

---

## 10. Verification Steps

### 10.1 Verify Installation

```bash
# Check Node.js version
node --version  # Should be 18+

# Check npm version
npm --version

# Verify dependencies
npm list --depth=0
```

### 10.2 Run Development Server

```bash
npm run dev
```

Visit `http://localhost:3000` - you should see the basic app with NSL branding.

### 10.3 Verify TypeScript

```bash
npm run type-check
```

Should complete with no errors.

### 10.4 Verify Tailwind CSS

The page should display with:
- Dark purple-blue background (`--background: 250 24% 10%`)
- Purple primary color for heading
- Muted foreground color for description text

---

## 11. Next Steps

With Phase 1 complete, you have:
- ✅ Vite + React + TypeScript project initialized
- ✅ Tailwind CSS configured with NSL branding
- ✅ FontAwesome installed
- ✅ Project structure established
- ✅ Type definitions created
- ✅ Build tooling configured

**Proceed to Phase 2:** UI Components & Design System

---

## Troubleshooting

### Issue: Path aliases not working
**Solution:** Ensure `tsconfig.json` and `vite.config.ts` both have matching path configurations.

### Issue: Tailwind classes not applying
**Solution:** 
1. Check that `globals.css` is imported in `main.tsx`
2. Verify `tailwind.config.ts` includes correct content paths
3. Restart dev server

### Issue: FontAwesome icons not showing
**Solution:** FontAwesome setup will be completed in Phase 2 with the icon library configuration.

---

**Phase 1 Complete!** 🎉
