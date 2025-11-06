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
        set({
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
          currentState: WorkflowState.PLANNING,
        }, false, 'startResearch'),
      
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
