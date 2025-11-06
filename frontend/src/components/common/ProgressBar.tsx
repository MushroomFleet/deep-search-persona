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
