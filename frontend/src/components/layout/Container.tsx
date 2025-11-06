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
