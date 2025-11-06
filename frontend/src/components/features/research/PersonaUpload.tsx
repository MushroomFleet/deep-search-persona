import { useCallback, useState } from 'react'
import { useDropzone } from 'react-dropzone'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faUpload, faFileAlt, faCheckCircle } from '@fortawesome/free-solid-svg-icons'
import clsx from 'clsx'
import { Persona } from '@/types'

export interface PersonaUploadProps {
  onUpload: (persona: Persona) => void
  maxSize?: number // bytes
  acceptedExtensions?: string[]
}

export default function PersonaUpload({
  onUpload,
  maxSize = 1048576, // 1MB
  acceptedExtensions = ['.md', '.markdown', '.txt']
}: PersonaUploadProps) {
  const [uploaded, setUploaded] = useState(false)
  const [error, setError] = useState('')
  
  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    setError('')
    setUploaded(false)
    
    if (acceptedFiles.length === 0) {
      setError('No file selected')
      return
    }
    
    const file = acceptedFiles[0]
    
    // Validate file size
    if (file.size > maxSize) {
      setError(`File too large. Maximum size: ${(maxSize / 1024 / 1024).toFixed(1)}MB`)
      return
    }
    
    // Validate extension
    const extension = '.' + file.name.split('.').pop()?.toLowerCase()
    if (!acceptedExtensions.includes(extension || '')) {
      setError(`Invalid file type. Accepted: ${acceptedExtensions.join(', ')}`)
      return
    }
    
    try {
      const content = await file.text()
      
      const persona: Persona = {
        id: `${Date.now()}-${file.name}`,
        name: file.name.replace(/\.(md|markdown|txt)$/i, ''),
        filename: file.name,
        content,
        uploadedAt: new Date()
      }
      
      onUpload(persona)
      setUploaded(true)
    } catch (err) {
      setError('Error reading file')
      console.error(err)
    }
  }, [maxSize, acceptedExtensions, onUpload])
  
  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'text/markdown': acceptedExtensions,
      'text/plain': acceptedExtensions
    },
    maxFiles: 1,
    multiple: false
  })
  
  return (
    <div className="space-y-2">
      <label className="block text-sm font-medium text-foreground">
        Writer Persona (Optional)
      </label>
      
      <div
        {...getRootProps()}
        className={clsx(
          'border-2 border-dashed rounded-lg p-8 text-center cursor-pointer',
          'transition-smooth hover:border-primary',
          isDragActive && 'border-primary bg-primary/5',
          uploaded && 'border-success bg-success/5',
          error && 'border-destructive bg-destructive/5',
          !isDragActive && !uploaded && !error && 'border-border'
        )}
      >
        <input {...getInputProps()} />
        
        <div className="flex flex-col items-center gap-3">
          <FontAwesomeIcon
            icon={uploaded ? faCheckCircle : isDragActive ? faUpload : faFileAlt}
            className={clsx(
              'h-12 w-12',
              uploaded && 'text-success',
              isDragActive && 'text-primary',
              !uploaded && !isDragActive && 'text-muted-foreground'
            )}
          />
          
          <div>
            {uploaded ? (
              <p className="text-success font-medium">Persona uploaded successfully!</p>
            ) : isDragActive ? (
              <p className="text-primary font-medium">Drop the file here</p>
            ) : (
              <>
                <p className="text-foreground font-medium">
                  Drag & drop persona file here
                </p>
                <p className="text-sm text-muted-foreground mt-1">
                  or click to browse ({acceptedExtensions.join(', ')})
                </p>
              </>
            )}
          </div>
        </div>
      </div>
      
      {error && (
        <p className="text-sm text-destructive">{error}</p>
      )}
      
      <p className="text-xs text-muted-foreground">
        Upload a markdown file containing the writer's system prompt for specialized synthesis
      </p>
    </div>
  )
}
