import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faUser, faCheck } from '@fortawesome/free-solid-svg-icons'
import clsx from 'clsx'
import { Persona } from '@/types'
import { format } from 'date-fns'

export interface PersonaSelectorProps {
  personas: Persona[]
  selectedPersona?: Persona
  onSelect: (persona: Persona | undefined) => void
}

export default function PersonaSelector({ personas, selectedPersona, onSelect }: PersonaSelectorProps) {
  if (personas.length === 0) {
    return null
  }
  
  return (
    <div className="space-y-2">
      <label className="block text-sm font-medium text-foreground">
        Select Writer Persona
      </label>
      
      <div className="space-y-2">
        {/* None option */}
        <div
          onClick={() => onSelect(undefined)}
          className={clsx(
            'flex items-center gap-3 p-3 rounded-lg border cursor-pointer transition-smooth',
            !selectedPersona
              ? 'border-primary bg-primary/10'
              : 'border-border hover:border-primary/50'
          )}
        >
          <div className={clsx(
            'flex items-center justify-center w-5 h-5 rounded-full border-2',
            !selectedPersona ? 'border-primary bg-primary' : 'border-muted-foreground'
          )}>
            {!selectedPersona && (
              <FontAwesomeIcon icon={faCheck} className="h-3 w-3 text-primary-foreground" />
            )}
          </div>
          <div className="flex-1">
            <p className="font-medium text-foreground">Default (No Persona)</p>
            <p className="text-xs text-muted-foreground">Use standard synthesis</p>
          </div>
        </div>
        
        {/* Uploaded personas */}
        {personas.map((persona) => (
          <div
            key={persona.id}
            onClick={() => onSelect(persona)}
            className={clsx(
              'flex items-center gap-3 p-3 rounded-lg border cursor-pointer transition-smooth',
              selectedPersona?.id === persona.id
                ? 'border-primary bg-primary/10'
                : 'border-border hover:border-primary/50'
            )}
          >
            <div className={clsx(
              'flex items-center justify-center w-5 h-5 rounded-full border-2',
              selectedPersona?.id === persona.id ? 'border-primary bg-primary' : 'border-muted-foreground'
            )}>
              {selectedPersona?.id === persona.id && (
                <FontAwesomeIcon icon={faCheck} className="h-3 w-3 text-primary-foreground" />
              )}
            </div>
            <FontAwesomeIcon icon={faUser} className="h-4 w-4 text-accent" />
            <div className="flex-1">
              <p className="font-medium text-foreground">{persona.name}</p>
              <p className="text-xs text-muted-foreground">
                Uploaded {format(persona.uploadedAt, 'MMM d, yyyy')} · {(persona.content.length / 1024).toFixed(1)}KB
              </p>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
