import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import {
  faCheckCircle,
  faExclamationCircle,
  faInfoCircle,
  faTriangleExclamation,
  faTimes
} from '@fortawesome/free-solid-svg-icons'
import { useUIStore } from '@/stores/useUIStore'
import clsx from 'clsx'

export default function Notifications() {
  const { notifications, removeNotification } = useUIStore()
  
  const icons = {
    success: faCheckCircle,
    error: faExclamationCircle,
    info: faInfoCircle,
    warning: faTriangleExclamation,
  }
  
  const colors = {
    success: 'bg-success/10 border-success text-success',
    error: 'bg-destructive/10 border-destructive text-destructive',
    info: 'bg-primary/10 border-primary text-primary',
    warning: 'bg-accent/10 border-accent text-accent',
  }
  
  if (notifications.length === 0) {
    return null
  }
  
  return (
    <div className="fixed top-4 right-4 z-50 space-y-2 max-w-md">
      {notifications.map((notification) => (
        <div
          key={notification.id}
          className={clsx(
            'flex items-start gap-3 p-4 rounded-lg border shadow-elegant',
            'animate-slide-up',
            colors[notification.type]
          )}
        >
          <FontAwesomeIcon
            icon={icons[notification.type]}
            className="h-5 w-5 mt-0.5"
          />
          <p className="flex-1 text-sm font-medium">{notification.message}</p>
          <button
            onClick={() => removeNotification(notification.id)}
            className="text-current hover:opacity-70 transition-smooth"
            aria-label="Close notification"
          >
            <FontAwesomeIcon icon={faTimes} className="h-4 w-4" />
          </button>
        </div>
      ))}
    </div>
  )
}
