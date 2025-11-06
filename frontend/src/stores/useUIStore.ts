import { create } from 'zustand'
import { devtools } from 'zustand/middleware'

type NotificationType = 'success' | 'error' | 'info' | 'warning'

interface Notification {
  id: string
  type: NotificationType
  message: string
  duration?: number
}

interface UIState {
  // State
  notifications: Notification[]
  isResultsDrawerOpen: boolean
  isSettingsModalOpen: boolean
  
  // Actions
  showNotification: (type: NotificationType, message: string, duration?: number) => void
  removeNotification: (id: string) => void
  clearNotifications: () => void
  toggleResultsDrawer: () => void
  openSettingsModal: () => void
  closeSettingsModal: () => void
}

export const useUIStore = create<UIState>()(
  devtools(
    (set) => ({
      notifications: [],
      isResultsDrawerOpen: false,
      isSettingsModalOpen: false,
      
      showNotification: (type, message, duration = 5000) => {
        const id = `notification-${Date.now()}`
        
        set((state) => ({
          notifications: [...state.notifications, { id, type, message, duration }]
        }), false, 'showNotification')
        
        // Auto-remove notification
        if (duration > 0) {
          setTimeout(() => {
            set((state) => ({
              notifications: state.notifications.filter(n => n.id !== id)
            }))
          }, duration)
        }
      },
      
      removeNotification: (id: string) =>
        set((state) => ({
          notifications: state.notifications.filter(n => n.id !== id)
        }), false, 'removeNotification'),
      
      clearNotifications: () =>
        set({ notifications: [] }, false, 'clearNotifications'),
      
      toggleResultsDrawer: () =>
        set((state) => ({
          isResultsDrawerOpen: !state.isResultsDrawerOpen
        }), false, 'toggleResultsDrawer'),
      
      openSettingsModal: () =>
        set({ isSettingsModalOpen: true }, false, 'openSettingsModal'),
      
      closeSettingsModal: () =>
        set({ isSettingsModalOpen: false }, false, 'closeSettingsModal'),
    }),
    { name: 'UIStore' }
  )
)
