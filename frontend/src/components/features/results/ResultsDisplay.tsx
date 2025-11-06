import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faFileAlt, faDownload } from '@fortawesome/free-solid-svg-icons'
import { ResearchResult } from '@/types'
import Card from '@/components/common/Card'
import Badge from '@/components/common/Badge'
import MarkdownRenderer from './MarkdownRenderer'

export interface ResultsDisplayProps {
  result: ResearchResult
}

export default function ResultsDisplay({ result }: ResultsDisplayProps) {
  const handleDownload = () => {
    const element = document.createElement('a')
    const file = new Blob([result.final_report], { type: 'text/markdown' })
    element.href = URL.createObjectURL(file)
    element.download = `research-${Date.now()}.md`
    document.body.appendChild(element)
    element.click()
    document.body.removeChild(element)
  }
  
  return (
    <div className="space-y-6">
      {/* Header */}
      <Card>
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-3">
            <FontAwesomeIcon icon={faFileAlt} className="h-6 w-6 text-primary" />
            <div>
              <h2 className="text-2xl font-semibold">Research Complete</h2>
              <p className="text-sm text-muted-foreground">
                Generated on {new Date().toLocaleDateString()}
              </p>
            </div>
          </div>
          <button
            onClick={handleDownload}
            className="flex items-center gap-2 px-4 py-2 bg-accent text-accent-foreground 
                     rounded-md hover:bg-accent/90 transition-smooth"
          >
            <FontAwesomeIcon icon={faDownload} className="h-4 w-4" />
            Download Report
          </button>
        </div>
        
        {/* Metadata */}
        <div className="flex flex-wrap gap-2">
          {result.phase3_metadata?.total_transitions && (
            <Badge variant="default">
              {result.phase3_metadata.total_transitions} Transitions
            </Badge>
          )}
          {result.phase3_metadata?.state_path && (
            <Badge variant="primary">
              {result.phase3_metadata.state_path.length} States
            </Badge>
          )}
          {result.research_history && (
            <Badge variant="accent">
              {result.research_history.length} Research Steps
            </Badge>
          )}
        </div>
      </Card>
      
      {/* Report Content */}
      <Card>
        <MarkdownRenderer content={result.final_report} />
      </Card>
    </div>
  )
}
