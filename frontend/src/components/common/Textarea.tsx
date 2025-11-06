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
