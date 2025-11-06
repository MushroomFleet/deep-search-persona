# Phase 2: UI Components & Design System

## Overview
This phase builds the complete UI component library using NSL branding, creating reusable components that implement the design system from Phase 1.

## Prerequisites
- Phase 1 completed successfully
- Development server running (`npm run dev`)

---

## 1. Component Architecture

### 1.1 Component Organization

```
src/components/
├── common/                  # Reusable UI primitives
│   ├── Button.tsx
│   ├── Input.tsx
│   ├── Textarea.tsx
│   ├── Card.tsx
│   ├── Badge.tsx
│   ├── Spinner.tsx
│   └── ProgressBar.tsx
├── layout/                  # Layout components
│   ├── Header.tsx
│   ├── Footer.tsx
│   ├── MainLayout.tsx
│   └── Container.tsx
└── features/                # Feature-specific components
    ├── research/
    │   ├── PromptInput.tsx
    │   ├── PersonaUpload.tsx
    │   ├── PersonaSelector.tsx
    │   ├── ResearchForm.tsx
    │   └── ResearchProgress.tsx
    └── results/
        ├── ResultsDisplay.tsx
        ├── MarkdownRenderer.tsx
        ├── MetadataPanel.tsx
        └── StatePathVisualization.tsx
```

---

## 2. Common Components

### 2.1 Button Component (`src/components/common/Button.tsx`)

```typescript
import { ButtonHTMLAttributes, forwardRef } from 'react'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { IconDefinition } from '@fortawesome/fontawesome-svg-core'
import clsx from 'clsx'

export type ButtonVariant = 'primary' | 'secondary' | 'accent' | 'outline' | 'ghost' | 'destructive'
export type ButtonSize = 'sm' | 'md' | 'lg'

export interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: ButtonVariant
  size?: ButtonSize
  icon?: IconDefinition
  iconPosition?: 'left' | 'right'
  isLoading?: boolean
  fullWidth?: boolean
}

const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  (
    {
      variant = 'primary',
      size = 'md',
      icon,
      iconPosition = 'left',
      isLoading = false,
      fullWidth = false,
      className,
      children,
      disabled,
      ...props
    },
    ref
  ) => {
    const baseStyles = 'inline-flex items-center justify-center rounded-md font-medium transition-smooth focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50'
    
    const variantStyles = {
      primary: 'bg-primary text-primary-foreground hover:bg-primary/90 shadow-glow',
      secondary: 'bg-secondary text-secondary-foreground hover:bg-secondary/80',
      accent: 'bg-accent text-accent-foreground hover:bg-accent/90 shadow-accent',
      outline: 'border border-input bg-background hover:bg-accent hover:text-accent-foreground',
      ghost: 'hover:bg-accent hover:text-accent-foreground',
      destructive: 'bg-destructive text-destructive-foreground hover:bg-destructive/90',
    }
    
    const sizeStyles = {
      sm: 'h-9 px-3 text-sm',
      md: 'h-10 px-4 text-base',
      lg: 'h-11 px-8 text-lg',
    }
    
    return (
      <button
        ref={ref}
        className={clsx(
          baseStyles,
          variantStyles[variant],
          sizeStyles[size],
          fullWidth && 'w-full',
          className
        )}
        disabled={disabled || isLoading}
        {...props}
      >
        {isLoading ? (
          <>
            <svg className="animate-spin -ml-1 mr-2 h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            Loading...
          </>
        ) : (
          <>
            {icon && iconPosition === 'left' && (
              <FontAwesomeIcon icon={icon} className="mr-2 h-4 w-4" />
            )}
            {children}
            {icon && iconPosition === 'right' && (
              <FontAwesomeIcon icon={icon} className="ml-2 h-4 w-4" />
            )}
          </>
        )}
      </button>
    )
  }
)

Button.displayName = 'Button'

export default Button
```

### 2.2 Input Component (`src/components/common/Input.tsx`)

```typescript
import { InputHTMLAttributes, forwardRef } from 'react'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { IconDefinition } from '@fortawesome/fontawesome-svg-core'
import clsx from 'clsx'

export interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  label?: string
  error?: string
  icon?: IconDefinition
  iconPosition?: 'left' | 'right'
}

const Input = forwardRef<HTMLInputElement, InputProps>(
  ({ label, error, icon, iconPosition = 'left', className, ...props }, ref) => {
    return (
      <div className="w-full">
        {label && (
          <label className="block text-sm font-medium mb-2 text-foreground">
            {label}
          </label>
        )}
        <div className="relative">
          {icon && iconPosition === 'left' && (
            <div className="absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground">
              <FontAwesomeIcon icon={icon} className="h-4 w-4" />
            </div>
          )}
          <input
            ref={ref}
            className={clsx(
              'w-full bg-background border border-input text-foreground rounded-md px-3 py-2',
              'focus:outline-none focus:ring-2 focus:ring-ring transition-smooth',
              'placeholder:text-muted-foreground',
              icon && iconPosition === 'left' && 'pl-10',
              icon && iconPosition === 'right' && 'pr-10',
              error && 'border-destructive',
              className
            )}
            {...props}
          />
          {icon && iconPosition === 'right' && (
            <div className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground">
              <FontAwesomeIcon icon={icon} className="h-4 w-4" />
            </div>
          )}
        </div>
        {error && (
          <p className="mt-1 text-sm text-destructive">{error}</p>
        )}
      </div>
    )
  }
)

Input.displayName = 'Input'

export default Input
```

### 2.3 Textarea Component (`src/components/common/Textarea.tsx`)

```typescript
import { TextareaHTMLAttributes, forwardRef } from 'react'
import clsx from 'clsx'

export interface TextareaProps extends TextareaHTMLAttributes<HTMLTextAreaElement> {
  label?: string
  error?: string
}

const Textarea = forwardRef<HTMLTextAreaElement, TextareaProps>(
  ({ label, error, className, ...props }, ref) => {
    return (
      <div className="w-full">
        {label && (
          <label className="block text-sm font-medium mb-2 text-foreground">
            {label}
          </label>
        )}
        <textarea
          ref={ref}
          className={clsx(
            'w-full bg-background border border-input text-foreground rounded-md px-3 py-2',
            'focus:outline-none focus:ring-2 focus:ring-ring transition-smooth resize-none',
            'placeholder:text-muted-foreground',
            error && 'border-destructive',
            className
          )}
          {...props}
        />
        {error && (
          <p className="mt-1 text-sm text-destructive">{error}</p>
        )}
      </div>
    )
  }
)

Textarea.displayName = 'Textarea'

export default Textarea
```

### 2.4 Card Component (`src/components/common/Card.tsx`)

```typescript
import { HTMLAttributes, forwardRef } from 'react'
import clsx from 'clsx'

export interface CardProps extends HTMLAttributes<HTMLDivElement> {
  variant?: 'default' | 'gradient'
  hover?: boolean
}

const Card = forwardRef<HTMLDivElement, CardProps>(
  ({ variant = 'default', hover = false, className, children, ...props }, ref) => {
    return (
      <div
        ref={ref}
        className={clsx(
          'rounded-lg p-6',
          variant === 'default' && 'bg-card text-card-foreground shadow-elegant',
          variant === 'gradient' && 'gradient-subtle shadow-glow border border-border',
          hover && 'transition-smooth hover:-translate-y-1 hover:shadow-glow',
          className
        )}
        {...props}
      >
        {children}
      </div>
    )
  }
)

Card.displayName = 'Card'

export default Card
```

### 2.5 Badge Component (`src/components/common/Badge.tsx`)

```typescript
import { HTMLAttributes } from 'react'
import clsx from 'clsx'

export type BadgeVariant = 'default' | 'primary' | 'accent' | 'success' | 'destructive'

export interface BadgeProps extends HTMLAttributes<HTMLDivElement> {
  variant?: BadgeVariant
}

export default function Badge({ variant = 'default', className, children, ...props }: BadgeProps) {
  const variantStyles = {
    default: 'bg-secondary text-secondary-foreground',
    primary: 'bg-primary text-primary-foreground',
    accent: 'bg-accent text-accent-foreground',
    success: 'bg-success text-success-foreground',
    destructive: 'bg-destructive text-destructive-foreground',
  }
  
  return (
    <div
      className={clsx(
        'inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-semibold transition-smooth',
        variantStyles[variant],
        className
      )}
      {...props}
    >
      {children}
    </div>
  )
}
```

### 2.6 Spinner Component (`src/components/common/Spinner.tsx`)

```typescript
import clsx from 'clsx'

export interface SpinnerProps {
  size?: 'sm' | 'md' | 'lg'
  className?: string
}

export default function Spinner({ size = 'md', className }: SpinnerProps) {
  const sizeStyles = {
    sm: 'h-4 w-4',
    md: 'h-8 w-8',
    lg: 'h-12 w-12',
  }
  
  return (
    <div className={clsx('inline-block', className)}>
      <svg
        className={clsx('animate-spin text-primary', sizeStyles[size])}
        xmlns="http://www.w3.org/2000/svg"
        fill="none"
        viewBox="0 0 24 24"
      >
        <circle
          className="opacity-25"
          cx="12"
          cy="12"
          r="10"
          stroke="currentColor"
          strokeWidth="4"
        ></circle>
        <path
          className="opacity-75"
          fill="currentColor"
          d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
        ></path>
      </svg>
    </div>
  )
}
```

### 2.7 ProgressBar Component (`src/components/common/ProgressBar.tsx`)

```typescript
import clsx from 'clsx'

export interface ProgressBarProps {
  value: number // 0-100
  label?: string
  showPercentage?: boolean
  variant?: 'primary' | 'accent' | 'success'
  className?: string
}

export default function ProgressBar({
  value,
  label,
  showPercentage = true,
  variant = 'primary',
  className
}: ProgressBarProps) {
  const variantStyles = {
    primary: 'gradient-primary',
    accent: 'gradient-accent',
    success: 'bg-success',
  }
  
  const clampedValue = Math.min(100, Math.max(0, value))
  
  return (
    <div className={clsx('w-full', className)}>
      {(label || showPercentage) && (
        <div className="flex justify-between items-center mb-2">
          {label && <span className="text-sm font-medium text-foreground">{label}</span>}
          {showPercentage && (
            <span className="text-sm text-muted-foreground">{clampedValue.toFixed(0)}%</span>
          )}
        </div>
      )}
      <div className="w-full bg-secondary rounded-full h-2 overflow-hidden">
        <div
          className={clsx('h-full transition-all duration-500 ease-out', variantStyles[variant])}
          style={{ width: `${clampedValue}%` }}
        />
      </div>
    </div>
  )
}
```

---

## 3. Layout Components

### 3.1 Header Component (`src/components/layout/Header.tsx`)

```typescript
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faMagnifyingGlass, faFlask } from '@fortawesome/free-solid-svg-icons'

export default function Header() {
  return (
    <header className="bg-card border-b border-border px-6 py-4 shadow-elegant">
      <div className="container mx-auto flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="flex items-center justify-center w-10 h-10 rounded-lg gradient-primary">
            <FontAwesomeIcon icon={faMagnifyingGlass} className="h-5 w-5 text-primary-foreground" />
          </div>
          <div>
            <h1 className="text-xl font-semibold text-foreground">Deep Search</h1>
            <p className="text-xs text-muted-foreground">NSL Research Pipeline</p>
          </div>
        </div>
        
        <div className="flex items-center gap-2 text-sm text-muted-foreground">
          <FontAwesomeIcon icon={faFlask} className="h-4 w-4" />
          <span>Phase 3 Advanced</span>
        </div>
      </div>
    </header>
  )
}
```

### 3.2 Footer Component (`src/components/layout/Footer.tsx`)

```typescript
export default function Footer() {
  return (
    <footer className="bg-card border-t border-border px-6 py-4 mt-auto">
      <div className="container mx-auto text-center text-sm text-muted-foreground">
        <p>
          Deep Search Pipeline &copy; {new Date().getFullYear()} · 
          <span className="text-primary"> NSL Ecosystem</span>
        </p>
      </div>
    </footer>
  )
}
```

### 3.3 MainLayout Component (`src/components/layout/MainLayout.tsx`)

```typescript
import { ReactNode } from 'react'
import Header from './Header'
import Footer from './Footer'
import Container from './Container'

export interface MainLayoutProps {
  children: ReactNode
}

export default function MainLayout({ children }: MainLayoutProps) {
  return (
    <div className="min-h-screen bg-background text-foreground flex flex-col">
      <Header />
      <main className="flex-1 py-8">
        <Container>{children}</Container>
      </main>
      <Footer />
    </div>
  )
}
```

### 3.4 Container Component (`src/components/layout/Container.tsx`)

```typescript
import { HTMLAttributes, forwardRef } from 'react'
import clsx from 'clsx'

export interface ContainerProps extends HTMLAttributes<HTMLDivElement> {
  size?: 'sm' | 'md' | 'lg' | 'xl' | 'full'
}

const Container = forwardRef<HTMLDivElement, ContainerProps>(
  ({ size = 'xl', className, children, ...props }, ref) => {
    const sizeStyles = {
      sm: 'max-w-screen-sm',
      md: 'max-w-screen-md',
      lg: 'max-w-screen-lg',
      xl: 'max-w-screen-xl',
      full: 'max-w-full',
    }
    
    return (
      <div
        ref={ref}
        className={clsx('container mx-auto px-4', sizeStyles[size], className)}
        {...props}
      >
        {children}
      </div>
    )
  }
)

Container.displayName = 'Container'

export default Container
```

---

## 4. Feature Components - Research

### 4.1 PromptInput Component (`src/components/features/research/PromptInput.tsx`)

```typescript
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
```

### 4.2 PersonaUpload Component (`src/components/features/research/PersonaUpload.tsx`)

```typescript
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
```

### 4.3 PersonaSelector Component (`src/components/features/research/PersonaSelector.tsx`)

```typescript
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
```

### 4.4 ResearchForm Component (`src/components/features/research/ResearchForm.tsx`)

```typescript
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
```

### 4.5 ResearchProgress Component (`src/components/features/research/ResearchProgress.tsx`)

```typescript
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import {
  faClipboardList,
  faMagnifyingGlass,
  faChartLine,
  faCheckCircle,
  faExclamationCircle,
  faCircleNotch
} from '@fortawesome/free-solid-svg-icons'
import { WorkflowState, ProgressUpdate } from '@/types'
import Card from '@/components/common/Card'
import Badge from '@/components/common/Badge'
import ProgressBar from '@/components/common/ProgressBar'

export interface ResearchProgressProps {
  currentState: WorkflowState
  progress?: ProgressUpdate
  isComplete: boolean
  hasError: boolean
}

export default function ResearchProgress({
  currentState,
  progress,
  isComplete,
  hasError
}: ResearchProgressProps) {
  const stateIcons = {
    [WorkflowState.PLANNING]: faClipboardList,
    [WorkflowState.SEARCHING]: faMagnifyingGlass,
    [WorkflowState.ANALYZING]: faChartLine,
    [WorkflowState.VALIDATING]: faCheckCircle,
    [WorkflowState.REFINING]: faCircleNotch,
    [WorkflowState.SYNTHESIZING]: faCheckCircle,
    [WorkflowState.COMPLETED]: faCheckCircle,
    [WorkflowState.FAILED]: faExclamationCircle,
  }
  
  const stateLabels = {
    [WorkflowState.PLANNING]: 'Planning Research',
    [WorkflowState.SEARCHING]: 'Searching Sources',
    [WorkflowState.ANALYZING]: 'Analyzing Findings',
    [WorkflowState.VALIDATING]: 'Validating Facts',
    [WorkflowState.REFINING]: 'Refining Search',
    [WorkflowState.SYNTHESIZING]: 'Synthesizing Report',
    [WorkflowState.COMPLETED]: 'Research Complete',
    [WorkflowState.FAILED]: 'Research Failed',
  }
  
  return (
    <Card variant="gradient">
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="text-lg font-semibold">Research Progress</h3>
          {isComplete && (
            <Badge variant="success">Complete</Badge>
          )}
          {hasError && (
            <Badge variant="destructive">Error</Badge>
          )}
        </div>
        
        <div className="flex items-center gap-3">
          <FontAwesomeIcon
            icon={stateIcons[currentState]}
            className="h-6 w-6 text-primary animate-pulse"
          />
          <div>
            <p className="font-medium text-foreground">{stateLabels[currentState]}</p>
            {progress && (
              <p className="text-sm text-muted-foreground">
                Iteration {progress.iteration} · {progress.message}
              </p>
            )}
          </div>
        </div>
        
        {progress && (
          <div className="space-y-3">
            <ProgressBar
              value={progress.confidence * 100}
              label="Confidence"
              variant="primary"
            />
            <ProgressBar
              value={progress.coverage * 100}
              label="Coverage"
              variant="accent"
            />
          </div>
        )}
      </div>
    </Card>
  )
}
```

---

## 5. Feature Components - Results

### 5.1 MarkdownRenderer Component (`src/components/features/results/MarkdownRenderer.tsx`)

```typescript
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import rehypeRaw from 'rehype-raw'

export interface MarkdownRendererProps {
  content: string
  className?: string
}

export default function MarkdownRenderer({ content, className }: MarkdownRendererProps) {
  return (
    <div className={className}>
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        rehypePlugins={[rehypeRaw]}
        className="prose prose-invert prose-purple max-w-none"
        components={{
          h1: ({ children }) => (
            <h1 className="text-3xl font-bold text-foreground mb-4 mt-6">{children}</h1>
          ),
          h2: ({ children }) => (
            <h2 className="text-2xl font-semibold text-foreground mb-3 mt-5">{children}</h2>
          ),
          h3: ({ children }) => (
            <h3 className="text-xl font-semibold text-foreground mb-2 mt-4">{children}</h3>
          ),
          p: ({ children }) => (
            <p className="text-foreground mb-4 leading-relaxed">{children}</p>
          ),
          ul: ({ children }) => (
            <ul className="list-disc list-inside text-foreground mb-4 space-y-2">{children}</ul>
          ),
          ol: ({ children }) => (
            <ol className="list-decimal list-inside text-foreground mb-4 space-y-2">{children}</ol>
          ),
          li: ({ children }) => (
            <li className="text-foreground">{children}</li>
          ),
          a: ({ href, children }) => (
            <a
              href={href}
              className="text-primary hover:text-primary-glow underline transition-smooth"
              target="_blank"
              rel="noopener noreferrer"
            >
              {children}
            </a>
          ),
          code: ({ children, className }) => {
            const isInline = !className
            return isInline ? (
              <code className="bg-muted text-accent px-1.5 py-0.5 rounded text-sm font-mono">
                {children}
              </code>
            ) : (
              <code className="block bg-muted text-foreground p-4 rounded-lg overflow-x-auto text-sm font-mono">
                {children}
              </code>
            )
          },
          blockquote: ({ children }) => (
            <blockquote className="border-l-4 border-primary pl-4 italic text-muted-foreground my-4">
              {children}
            </blockquote>
          ),
        }}
      >
        {content}
      </ReactMarkdown>
    </div>
  )
}
```

### 5.2 Complete Phase 2 Documentation

Continue to next section...
