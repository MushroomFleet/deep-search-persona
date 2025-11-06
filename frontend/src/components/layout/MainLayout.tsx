import { ReactNode } from 'react'
import Header from './Header'
import Footer from './Footer'
import Container from './Container'
import Notifications from '@/components/common/Notifications'

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
      <Notifications />
    </div>
  )
}
