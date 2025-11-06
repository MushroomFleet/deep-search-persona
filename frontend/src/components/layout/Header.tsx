import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faMagnifyingGlass, faHeart } from '@fortawesome/free-solid-svg-icons'

export default function Header() {
  return (
    <header className="bg-card border-b border-border px-6 py-4 shadow-elegant">
      <div className="container mx-auto flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="flex items-center justify-center w-10 h-10 rounded-lg gradient-primary">
            <FontAwesomeIcon icon={faMagnifyingGlass} className="h-5 w-5 text-primary-foreground" />
          </div>
          <div>
            <h1 className="text-xl font-semibold text-foreground">Deep Search Persona</h1>
            <p className="text-xs text-muted-foreground">Zero Vector 8</p>
          </div>
        </div>
        
        <a
          href="https://ko-fi.com/driftjohnson"
          target="_blank"
          rel="noopener noreferrer"
          className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-[#FF5E5B] hover:bg-[#FF4845] transition-colors text-white text-sm font-medium shadow-sm hover:shadow-md group"
          title="Support this project"
        >
          <FontAwesomeIcon icon={faHeart} className="h-4 w-4 group-hover:scale-110 transition-transform" />
          <span>Donate</span>
        </a>
      </div>
    </header>
  )
}
