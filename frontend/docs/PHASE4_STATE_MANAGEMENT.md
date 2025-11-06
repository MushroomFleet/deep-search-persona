# Phase 4: State Management & Application Logic

## Overview
This phase implements centralized state management using Zustand, integrating all components and connecting the frontend to the backend API.

## Prerequisites
- Phases 1, 2, and 3 completed
- Backend API server running

---

## 1. State Management Architecture

### 1.1 Why Zustand?

- **Lightweight**: Minimal boilerplate compared to Redux
- **TypeScript-first**: Excellent TypeScript support
- **Simple API**: Easy to learn and use
- **No providers**: Direct store access
- **DevTools**: Redux DevTools compatible

### 1.2 Store Structure

```
src/stores/
├── useResearchStore.ts    # Research state and actions
├── usePersonaStore.ts     # Persona management
└── useUIStore.ts          # UI state (modals, notifications)
```

---

## 2. Research Store

### 2.1 Research Store (`src/stores/useResearchStore.ts`)

```typescript
import { create } from 'zustand'
import { devtools } from 'zustand/middleware'
import { ResearchJob, WorkflowState, ProgressUpdate, ResearchResult } from '@/types'

interface ResearchState {
  // State
  currentJob: ResearchJob | null
  currentState: WorkflowState
  progress: ProgressUpdate | null
  result: ResearchResult | null
  isRunning: boolean
  error: string | null
  
  // Actions
  startResearch: (query: string, personaId?: string) => void
  updateProgress: (progress: ProgressUpdate) => void
  updateState: (state: WorkflowState) => void
  setResult: (result: ResearchResult) => void
  setError: (error: string) => void
  reset: () => void
}

const initialState = {
  currentJob: null,
  currentState: WorkflowState.PLANNING,
  progress: null,
  result: null,
  isRunning: false,
  error: null,
}

export const useResearchStore = create<ResearchState>()(
  devtools(
    (set) => ({
      ...initialState,
      
      startResearch: (query: string, personaId?: string) => 
        set((state) => ({
          currentJob: {
            id: `job-${Date.now()}`,
            query,
            persona: personaId ? { id: personaId } as any : undefined,
            status: 'running' as any,
            createdAt: new Date(),
            startedAt: new Date(),
          },
          isRunning: true,
          error: null,
          result: null,
        }), false, 'startResearch'),
      
      updateProgress: (progress: ProgressUpdate) =>
        set({ progress }, false, 'updateProgress'),
      
      updateState: (currentState: WorkflowState) =>
        set({ currentState }, false, 'updateState'),
      
      setResult: (result: ResearchResult) =>
        set({
          result,
          isRunning: false,
          currentState: WorkflowState.COMPLETED,
        }, false, 'setResult'),
      
      setError: (error: string) =>
        set({
          error,
          isRunning: false,
          currentState: WorkflowState.FAILED,
        }, false, 'setError'),
      
      reset: () => set(initialState, false, 'reset'),
    }),
    { name: 'ResearchStore' }
  )
)
```

---

## 3. Persona Store

### 3.1 Persona Store (`src/stores/usePersonaStore.ts`)

```typescript
import { create } from 'zustand'
import { devtools, persist } from 'zustand/middleware'
import { Persona } from '@/types'

interface PersonaState {
  // State
  personas: Persona[]
  selectedPersona: Persona | null
  isUploading: boolean
  uploadError: string | null
  
  // Actions
  addPersona: (persona: Persona) => void
  removePersona: (personaId: string) => void
  selectPersona: (persona: Persona | null) => void
  setUploading: (isUploading: boolean) => void
  setUploadError: (error: string | null) => void
  clearPersonas: () => void
}

export const usePersonaStore = create<PersonaState>()(
  devtools(
    persist(
      (set) => ({
        personas: [],
        selectedPersona: null,
        isUploading: false,
        uploadError: null,
        
        addPersona: (persona: Persona) =>
          set((state) => ({
            personas: [...state.personas, persona],
            selectedPersona: persona,
            uploadError: null,
          }), false, 'addPersona'),
        
        removePersona: (personaId: string) =>
          set((state) => ({
            personas: state.personas.filter(p => p.id !== personaId),
            selectedPersona: state.selectedPersona?.id === personaId 
              ? null 
              : state.selectedPersona,
          }), false, 'removePersona'),
        
        selectPersona: (persona: Persona | null) =>
          set({ selectedPersona: persona }, false, 'selectPersona'),
        
        setUploading: (isUploading: boolean) =>
          set({ isUploading }, false, 'setUploading'),
        
        setUploadError: (error: string | null) =>
          set({ uploadError: error }, false, 'setUploadError'),
        
        clearPersonas: () =>
          set({ personas: [], selectedPersona: null }, false, 'clearPersonas'),
      }),
      {
        name: 'persona-storage',
        partialize: (state) => ({
          personas: state.personas,
          selectedPersona: state.selectedPersona,
        }),
      }
    ),
    { name: 'PersonaStore' }
  )
)
```

---

## 4. UI Store

### 4.1 UI Store (`src/stores/useUIStore.ts`)

```typescript
import { create } from 'zustand'
import { devtools } from 'zustand/middleware'

type NotificationType = 'success' | 'error' | 'info' | 'warning'

interface Notification {
  id: string
  type: NotificationType
  message: string
  duration?: number
}

interface UIState {
  // State
  notifications: Notification[]
  isResultsDrawerOpen: boolean
  isSettingsModalOpen: boolean
  
  // Actions
  showNotification: (type: NotificationType, message: string, duration?: number) => void
  removeNotification: (id: string) => void
  clearNotifications: () => void
  toggleResultsDrawer: () => void
  openSettingsModal: () => void
  closeSettingsModal: () => void
}

export const useUIStore = create<UIState>()(
  devtools(
    (set) => ({
      notifications: [],
      isResultsDrawerOpen: false,
      isSettingsModalOpen: false,
      
      showNotification: (type, message, duration = 5000) => {
        const id = `notification-${Date.now()}`
        
        set((state) => ({
          notifications: [...state.notifications, { id, type, message, duration }]
        }), false, 'showNotification')
        
        // Auto-remove notification
        if (duration > 0) {
          setTimeout(() => {
            set((state) => ({
              notifications: state.notifications.filter(n => n.id !== id)
            }))
          }, duration)
        }
      },
      
      removeNotification: (id: string) =>
        set((state) => ({
          notifications: state.notifications.filter(n => n.id !== id)
        }), false, 'removeNotification'),
      
      clearNotifications: () =>
        set({ notifications: [] }, false, 'clearNotifications'),
      
      toggleResultsDrawer: () =>
        set((state) => ({
          isResultsDrawerOpen: !state.isResultsDrawerOpen
        }), false, 'toggleResultsDrawer'),
      
      openSettingsModal: () =>
        set({ isSettingsModalOpen: true }, false, 'openSettingsModal'),
      
      closeSettingsModal: () =>
        set({ isSettingsModalOpen: false }, false, 'closeSettingsModal'),
    }),
    { name: 'UIStore' }
  )
)
```

---

## 5. Custom Hooks

### 5.1 Research Hook (`src/hooks/useResearch.ts`)

```typescript
import { useEffect } from 'react'
import { useResearchStore } from '@/stores/useResearchStore'
import { useUIStore } from '@/stores/useUIStore'
import { apiService } from '@/services/api'
import { WorkflowState } from '@/types'

export function useResearch() {
  const {
    currentJob,
    currentState,
    progress,
    result,
    isRunning,
    error,
    startResearch,
    updateProgress,
    updateState,
    setResult,
    setError,
    reset,
  } = useResearchStore()
  
  const { showNotification } = useUIStore()
  
  const executeResearch = async (query: string, personaId?: string) => {
    try {
      // Start research
      startResearch(query, personaId)
      showNotification('info', 'Research started...')
      
      // Create SSE connection
      const eventSource = apiService.executeResearch(query, personaId)
      
      eventSource.onmessage = (event) => {
        const data = JSON.parse(event.data)
        
        switch (data.type) {
          case 'start':
            updateState(WorkflowState.PLANNING)
            break
            
          case 'progress':
            updateProgress({
              iteration: data.iteration,
              state: data.state as WorkflowState,
              confidence: data.confidence || 0,
              coverage: data.coverage || 0,
              contradictions: data.contradictions || 0,
              message: data.message,
            })
            updateState(data.state as WorkflowState)
            break
            
          case 'state':
            // State transition event
            break
            
          case 'metrics':
            if (progress) {
              updateProgress({
                ...progress,
                confidence: data.confidence,
                coverage: data.coverage,
              })
            }
            break
            
          case 'complete':
            showNotification('success', 'Research completed successfully!')
            eventSource.close()
            
            // Fetch final result
            // Note: In production, the result should be included in the completion event
            break
            
          case 'error':
            setError(data.message)
            showNotification('error', `Research failed: ${data.message}`)
            eventSource.close()
            break
        }
      }
      
      eventSource.onerror = (error) => {
        console.error('SSE Error:', error)
        setError('Connection to server lost')
        showNotification('error', 'Connection to server lost')
        eventSource.close()
      }
      
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Unknown error'
      setError(message)
      showNotification('error', `Failed to start research: ${message}`)
    }
  }
  
  return {
    currentJob,
    currentState,
    progress,
    result,
    isRunning,
    error,
    executeResearch,
    reset,
  }
}
```

### 5.2 Persona Hook (`src/hooks/usePersonas.ts`)

```typescript
import { useCallback } from 'react'
import { usePersonaStore } from '@/stores/usePersonaStore'
import { useUIStore } from '@/stores/useUIStore'
import { apiService } from '@/services/api'
import { Persona } from '@/types'

export function usePersonas() {
  const {
    personas,
    selectedPersona,
    isUploading,
    uploadError,
    addPersona,
    removePersona,
    selectPersona,
    setUploading,
    setUploadError,
  } = usePersonaStore()
  
  const { showNotification } = useUIStore()
  
  const uploadPersona = useCallback(async (file: File) => {
    setUploading(true)
    setUploadError(null)
    
    try {
      const result = await apiService.uploadPersona(file)
      
      const persona: Persona = {
        id: result.id,
        name: result.name,
        filename: result.filename,
        content: '', // Content not needed in frontend
        uploadedAt: new Date(result.uploaded_at),
      }
      
      addPersona(persona)
      showNotification('success', `Persona "${persona.name}" uploaded successfully`)
      
      return persona
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Upload failed'
      setUploadError(message)
      showNotification('error', `Failed to upload persona: ${message}`)
      throw err
    } finally {
      setUploading(false)
    }
  }, [addPersona, setUploading, setUploadError, showNotification])
  
  const deletePersona = useCallback(async (personaId: string) => {
    try {
      await apiService.deletePersona(personaId)
      removePersona(personaId)
      showNotification('success', 'Persona deleted successfully')
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Delete failed'
      showNotification('error', `Failed to delete persona: ${message}`)
      throw err
    }
  }, [removePersona, showNotification])
  
  return {
    personas,
    selectedPersona,
    isUploading,
    uploadError,
    uploadPersona,
    deletePersona,
    selectPersona,
  }
}
```

---

## 6. Main Application Integration

### 6.1 Updated App Component (`src/App.tsx`)

```typescript
import { useEffect } from 'react'
import MainLayout from '@/components/layout/MainLayout'
import ResearchForm from '@/components/features/research/ResearchForm'
import ResearchProgress from '@/components/features/research/ResearchProgress'
import ResultsDisplay from '@/components/features/results/ResultsDisplay'
import { useResearch } from '@/hooks/useResearch'
import { usePersonas } from '@/hooks/usePersonas'
import { WorkflowState } from '@/types'

function App() {
  const {
    currentJob,
    currentState,
    progress,
    result,
    isRunning,
    error,
    executeResearch,
  } = useResearch()
  
  const { selectedPersona } = usePersonas()
  
  const handleSubmit = async (query: string) => {
    await executeResearch(query, selectedPersona?.id)
  }
  
  return (
    <MainLayout>
      <div className="space-y-6">
        {/* Research Form */}
        {!isRunning && !result && (
          <ResearchForm onSubmit={handleSubmit} isLoading={isRunning} />
        )}
        
        {/* Progress Indicator */}
        {isRunning && (
          <ResearchProgress
            currentState={currentState}
            progress={progress || undefined}
            isComplete={currentState === WorkflowState.COMPLETED}
            hasError={!!error}
          />
        )}
        
        {/* Results */}
        {result && (
          <ResultsDisplay result={result} />
        )}
        
        {/* Error State */}
        {error && !isRunning && (
          <div className="bg-destructive/10 border border-destructive rounded-lg p-6">
            <h3 className="text-lg font-semibold text-destructive mb-2">
              Research Failed
            </h3>
            <p className="text-destructive-foreground">{error}</p>
          </div>
        )}
      </div>
    </MainLayout>
  )
}

export default App
```

---

## 7. Notification System

### 7.1 Notifications Component (`src/components/common/Notifications.tsx`)

```typescript
import { useEffect } from 'react'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import {
  faCheckCircle,
  faExclamationCircle,
  faInfoCircle,
  faTriangleExclamation,
  faTimes
} from '@fortawesome/free-solid-svg-icons'
import { useUIStore } from '@/stores/useUIStore'
import clsx from 'clsx'

export default function Notifications() {
  const { notifications, removeNotification } = useUIStore()
  
  const icons = {
    success: faCheckCircle,
    error: faExclamationCircle,
    info: faInfoCircle,
    warning: faTriangleExclamation,
  }
  
  const colors = {
    success: 'bg-success/10 border-success text-success',
    error: 'bg-destructive/10 border-destructive text-destructive',
    info: 'bg-primary/10 border-primary text-primary',
    warning: 'bg-accent/10 border-accent text-accent',
  }
  
  return (
    <div className="fixed top-4 right-4 z-50 space-y-2 max-w-md">
      {notifications.map((notification) => (
        <div
          key={notification.id}
          className={clsx(
            'flex items-start gap-3 p-4 rounded-lg border shadow-elegant',
            'animate-slide-up',
            colors[notification.type]
          )}
        >
          <FontAwesomeIcon
            icon={icons[notification.type]}
            className="h-5 w-5 mt-0.5"
          />
          <p className="flex-1 text-sm font-medium">{notification.message}</p>
          <button
            onClick={() => removeNotification(notification.id)}
            className="text-current hover:opacity-70 transition-smooth"
          >
            <FontAwesomeIcon icon={faTimes} className="h-4 w-4" />
          </button>
        </div>
      ))}
    </div>
  )
}
```

### 7.2 Add to MainLayout

Update `src/components/layout/MainLayout.tsx`:

```typescript
import Notifications from '@/components/common/Notifications'

export default function MainLayout({ children }: MainLayoutProps) {
  return (
    <div className="min-h-screen bg-background text-foreground flex flex-col">
      <Header />
      <main className="flex-1 py-8">
        <Container>{children}</Container>
      </main>
      <Footer />
      <Notifications />
    </div>
  )
}
```

---

## 8. Testing State Management

### 8.1 Test Store Actions

```typescript
// Example test in browser console
import { useResearchStore } from '@/stores/useResearchStore'

const store = useResearchStore.getState()
store.startResearch('Test query')
console.log(store.currentJob)
```

### 8.2 Redux DevTools

1. Install Redux DevTools browser extension
2. Open DevTools
3. Navigate to Redux tab
4. Observe state changes in real-time

---

## 9. Next Steps

**Phase 4 Complete!** You now have:
- ✅ Centralized state management with Zustand
- ✅ Custom hooks for research and personas
- ✅ Notification system
- ✅ Full application integration

**Proceed to Phase 5:** Results Display & Final Polish

---

## Best Practices

### State Updates
- Use descriptive action names for DevTools
- Keep stores focused and single-purpose
- Avoid deeply nested state

### Performance
- Use `partialize` for localStorage persistence
- Avoid unnecessary re-renders with selectors
- Keep computed values minimal

### Debugging
- Enable DevTools in development
- Use action names for traceability
- Log errors to notification system

**Phase 4 Complete!** 🎉
