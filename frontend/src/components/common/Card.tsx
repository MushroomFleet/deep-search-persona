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
