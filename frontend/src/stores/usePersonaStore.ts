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
