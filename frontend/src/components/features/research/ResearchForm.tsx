import { useState } from 'react'
import { Persona } from '@/types'
import Card from '@/components/common/Card'
import PromptInput from './PromptInput'
import PersonaUpload from './PersonaUpload'
import PersonaSelector from './PersonaSelector'

export interface ResearchFormProps {
  onSubmit: (query: string, persona?: Persona) => void
  isLoading?: boolean
}

export default function ResearchForm({ onSubmit, isLoading = false }: ResearchFormProps) {
  const [query, setQuery] = useState('')
  const [personas, setPersonas] = useState<Persona[]>([])
  const [selectedPersona, setSelectedPersona] = useState<Persona | undefined>()
  
  const handlePersonaUpload = (persona: Persona) => {
    setPersonas([...personas, persona])
    setSelectedPersona(persona)
  }
  
  const handleSubmit = (prompt: string) => {
    setQuery(prompt)
    onSubmit(prompt, selectedPersona)
  }
  
  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
      {/* Main prompt input */}
      <div className="lg:col-span-2">
        <Card>
          <h2 className="text-2xl font-semibold mb-6">Configure Research</h2>
          <PromptInput
            onSubmit={handleSubmit}
            isLoading={isLoading}
          />
        </Card>
      </div>
      
      {/* Persona selection sidebar */}
      <div className="space-y-6">
        <Card>
          <h3 className="text-lg font-semibold mb-4">Writer Settings</h3>
          <div className="space-y-6">
            <PersonaUpload onUpload={handlePersonaUpload} />
            <PersonaSelector
              personas={personas}
              selectedPersona={selectedPersona}
              onSelect={setSelectedPersona}
            />
          </div>
        </Card>
      </div>
    </div>
  )
}
