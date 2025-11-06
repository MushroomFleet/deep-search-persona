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
