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
