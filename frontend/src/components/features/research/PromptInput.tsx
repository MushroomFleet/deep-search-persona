import { useState } from 'react'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faMagnifyingGlass } from '@fortawesome/free-solid-svg-icons'
import Textarea from '@/components/common/Textarea'
import Button from '@/components/common/Button'

export interface PromptInputProps {
  onSubmit: (prompt: string) => void
  isLoading?: boolean
  defaultValue?: string
}

export default function PromptInput({ onSubmit, isLoading = false, defaultValue = '' }: PromptInputProps) {
  const [prompt, setPrompt] = useState(defaultValue)
  const [error, setError] = useState('')
  
  const handleSubmit = () => {
    if (!prompt.trim()) {
      setError('Please enter a research query')
      return
    }
    
    if (prompt.trim().length < 10) {
      setError('Research query should be at least 10 characters')
      return
    }
    
    setError('')
    onSubmit(prompt.trim())
  }
  
  return (
    <div className="space-y-4">
      <Textarea
        label="Research Query"
        placeholder="Enter your deep search query... (e.g., 'Explain quantum computing breakthroughs in 2024')"
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
        error={error}
        rows={4}
        disabled={isLoading}
      />
      
      <div className="flex justify-between items-center text-sm text-muted-foreground">
        <span>{prompt.length} characters</span>
        <span className="text-xs">Tip: Be specific and detailed for better results</span>
      </div>
      
      <Button
        variant="primary"
        size="lg"
        icon={faMagnifyingGlass}
        onClick={handleSubmit}
        isLoading={isLoading}
        fullWidth
      >
        Start Research
      </Button>
    </div>
  )
}
