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
