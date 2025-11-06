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
      
      // Execute research with SSE
      apiService.executeResearch(
        query,
        personaId,
        // onEvent
        (event) => {
          switch (event.type) {
            case 'start':
              updateState(WorkflowState.PLANNING)
              break
              
            case 'progress':
              if (event.iteration && event.state) {
                updateProgress({
                  iteration: event.iteration,
                  state: event.state as WorkflowState,
                  confidence: event.confidence || 0,
                  coverage: event.coverage || 0,
                  contradictions: 0,
                  message: event.message || '',
                })
                updateState(event.state as WorkflowState)
              }
              break
              
            case 'state':
              // State transition event
              console.log('State transition:', event.message)
              break
              
            case 'metrics':
              if (progress && event.confidence !== undefined) {
                updateProgress({
                  ...progress,
                  confidence: event.confidence,
                  coverage: event.coverage || 0,
                })
              }
              break
            
            case 'result':
              // Result event with full research data
              if (event.data) {
                setResult(event.data as any)
              }
              break
              
            case 'log':
              // Log event
              console.log('Pipeline:', event.message)
              break
          }
        },
        // onError
        (err) => {
          const message = err.message || 'Unknown error'
          setError(message)
          showNotification('error', `Research failed: ${message}`)
        },
        // onComplete
        () => {
          showNotification('success', 'Research completed successfully!')
          // Note: Result should be fetched or included in completion event
        }
      )
      
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
