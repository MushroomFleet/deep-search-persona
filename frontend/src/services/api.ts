/**
 * API Service for Deep Search Backend
 */

const API_BASE_URL = (import.meta as any).env?.VITE_API_BASE_URL || 'http://localhost:5000'

export interface ApiError {
  error: string
}

export interface PipelineEvent {
  type: 'start' | 'progress' | 'state' | 'metrics' | 'log' | 'result' | 'complete' | 'error'
  query?: string
  iteration?: number
  state?: string
  confidence?: number
  coverage?: number
  message?: string
  data?: any  // Result data for 'result' event type
}

export class ApiService {
  private baseUrl: string

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl
  }

  // Health check
  async healthCheck(): Promise<{ status: string; version: string; service: string }> {
    const response = await fetch(`${this.baseUrl}/api/health`)
    return response.json()
  }

  // Get API status
  async getStatus(): Promise<any> {
    const response = await fetch(`${this.baseUrl}/api/status`)
    return response.json()
  }

  // Execute research with SSE
  executeResearch(
    query: string,
    personaId?: string,
    onEvent?: (event: PipelineEvent) => void,
    onError?: (error: Error) => void,
    onComplete?: () => void
  ): EventSource {
    // Build URL with query parameters for EventSource (GET only)
    const params = new URLSearchParams({ query })
    if (personaId) {
      params.append('persona_id', personaId)
    }
    const url = `${this.baseUrl}/api/research/execute?${params.toString()}`

    // Create EventSource for SSE
    const eventSource = new EventSource(url)
    
    eventSource.onmessage = (event) => {
      try {
        const data: PipelineEvent = JSON.parse(event.data)
        
        if (data.type === 'complete') {
          onComplete?.()
          eventSource.close()
        } else if (data.type === 'error') {
          onError?.(new Error(data.message || 'Unknown error'))
          eventSource.close()
        } else {
          onEvent?.(data)
        }
      } catch (err) {
        console.error('Error parsing SSE data:', err)
      }
    }
    
    eventSource.onerror = (error) => {
      console.error('SSE error:', error)
      onError?.(new Error('Connection error'))
      eventSource.close()
    }
    
    return eventSource
  }

  // Upload persona
  async uploadPersona(file: File): Promise<any> {
    const formData = new FormData()
    formData.append('file', file)

    const response = await fetch(`${this.baseUrl}/api/persona/upload`, {
      method: 'POST',
      body: formData
    })

    if (!response.ok) {
      const error: ApiError = await response.json()
      throw new Error(error.error)
    }

    return response.json()
  }

  // List personas
  async listPersonas(): Promise<any[]> {
    const response = await fetch(`${this.baseUrl}/api/persona/list`)
    const data = await response.json()
    return data.personas || []
  }

  // Get persona by ID
  async getPersona(personaId: string): Promise<any> {
    const response = await fetch(`${this.baseUrl}/api/persona/${personaId}`)
    
    if (!response.ok) {
      const error: ApiError = await response.json()
      throw new Error(error.error)
    }
    
    return response.json()
  }

  // Delete persona
  async deletePersona(personaId: string): Promise<void> {
    const response = await fetch(`${this.baseUrl}/api/persona/${personaId}`, {
      method: 'DELETE'
    })
    
    if (!response.ok) {
      const error: ApiError = await response.json()
      throw new Error(error.error)
    }
  }

  // List jobs
  async listJobs(): Promise<any[]> {
    const response = await fetch(`${this.baseUrl}/api/research/jobs`)
    const data = await response.json()
    return data.jobs || []
  }

  // Get job by ID
  async getJob(jobId: string): Promise<any> {
    const response = await fetch(`${this.baseUrl}/api/research/jobs/${jobId}`)
    
    if (!response.ok) {
      const error: ApiError = await response.json()
      throw new Error(error.error)
    }
    
    return response.json()
  }

  // Get job result
  async getJobResult(jobId: string): Promise<any> {
    const response = await fetch(`${this.baseUrl}/api/research/jobs/${jobId}/result`)
    
    if (!response.ok) {
      const error: ApiError = await response.json()
      throw new Error(error.error)
    }
    
    return response.json()
  }
}

export const apiService = new ApiService()
