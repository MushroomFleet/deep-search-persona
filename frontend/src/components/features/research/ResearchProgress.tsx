import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import {
  faClipboardList,
  faMagnifyingGlass,
  faChartLine,
  faCheckCircle,
  faExclamationCircle,
  faCircleNotch
} from '@fortawesome/free-solid-svg-icons'
import { WorkflowState, ProgressUpdate } from '@/types'
import Card from '@/components/common/Card'
import Badge from '@/components/common/Badge'
import ProgressBar from '@/components/common/ProgressBar'

export interface ResearchProgressProps {
  currentState: WorkflowState
  progress?: ProgressUpdate
  isComplete: boolean
  hasError: boolean
}

export default function ResearchProgress({
  currentState,
  progress,
  isComplete,
  hasError
}: ResearchProgressProps) {
  const stateIcons = {
    [WorkflowState.PLANNING]: faClipboardList,
    [WorkflowState.SEARCHING]: faMagnifyingGlass,
    [WorkflowState.ANALYZING]: faChartLine,
    [WorkflowState.VALIDATING]: faCheckCircle,
    [WorkflowState.REFINING]: faCircleNotch,
    [WorkflowState.SYNTHESIZING]: faCheckCircle,
    [WorkflowState.COMPLETED]: faCheckCircle,
    [WorkflowState.FAILED]: faExclamationCircle,
  }
  
  const stateLabels = {
    [WorkflowState.PLANNING]: 'Planning Research',
    [WorkflowState.SEARCHING]: 'Searching Sources',
    [WorkflowState.ANALYZING]: 'Analyzing Findings',
    [WorkflowState.VALIDATING]: 'Validating Facts',
    [WorkflowState.REFINING]: 'Refining Search',
    [WorkflowState.SYNTHESIZING]: 'Synthesizing Report',
    [WorkflowState.COMPLETED]: 'Research Complete',
    [WorkflowState.FAILED]: 'Research Failed',
  }
  
  return (
    <Card variant="gradient">
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="text-lg font-semibold">Research Progress</h3>
          {isComplete && (
            <Badge variant="success">Complete</Badge>
          )}
          {hasError && (
            <Badge variant="destructive">Error</Badge>
          )}
        </div>
        
        <div className="flex items-center gap-3">
          <FontAwesomeIcon
            icon={stateIcons[currentState]}
            className="h-6 w-6 text-primary animate-pulse"
          />
          <div>
            <p className="font-medium text-foreground">{stateLabels[currentState]}</p>
            {progress && (
              <p className="text-sm text-muted-foreground">
                Iteration {progress.iteration} · {progress.message}
              </p>
            )}
          </div>
        </div>
        
        {progress && (
          <div className="space-y-3">
            <ProgressBar
              value={progress.confidence * 100}
              label="Confidence"
              variant="primary"
            />
            <ProgressBar
              value={progress.coverage * 100}
              label="Coverage"
              variant="accent"
            />
          </div>
        )}
      </div>
    </Card>
  )
}
