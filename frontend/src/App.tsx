import MainLayout from './components/layout/MainLayout'
import ResearchForm from './components/features/research/ResearchForm'
import ResearchProgress from './components/features/research/ResearchProgress'
import ResultsDisplay from './components/features/results/ResultsDisplay'
import { useResearch } from './hooks/useResearch'
import { usePersonas } from './hooks/usePersonas'
import { WorkflowState } from './types'

function App() {
  const {
    currentState,
    progress,
    result,
    isRunning,
    error,
    executeResearch,
    reset,
  } = useResearch()
  
  const { selectedPersona } = usePersonas()
  
  const handleSubmit = async (query: string) => {
    await executeResearch(query, selectedPersona?.id)
  }
  
  const handleNewResearch = () => {
    reset()
  }
  
  return (
    <MainLayout>
      <div className="space-y-6">
        {/* Hero Section */}
        {!isRunning && !result && (
          <div className="text-center mb-8">
            <h1 className="text-4xl md:text-5xl font-bold mb-4 gradient-primary bg-clip-text text-transparent">
              Deep Search Research Pipeline
            </h1>
            <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
              Advanced AI-powered research with adaptive workflow, semantic memory, and specialized writer personas
            </p>
          </div>
        )}
        
        {/* Research Form */}
        {!isRunning && !result && (
          <>
            <ResearchForm onSubmit={handleSubmit} isLoading={isRunning} />
            
            {/* Info Section */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-12">
              <div className="bg-card rounded-lg p-6 border border-border">
                <div className="text-primary text-2xl mb-2">🔍</div>
                <h3 className="text-lg font-semibold mb-2">Smart Search</h3>
                <p className="text-sm text-muted-foreground">
                  Adaptive workflow that dynamically adjusts research strategy based on findings
                </p>
              </div>
              
              <div className="bg-card rounded-lg p-6 border border-border">
                <div className="text-accent text-2xl mb-2">🧠</div>
                <h3 className="text-lg font-semibold mb-2">Semantic Memory</h3>
                <p className="text-sm text-muted-foreground">
                  Embedding-based similarity search for discovering related findings
                </p>
              </div>
              
              <div className="bg-card rounded-lg p-6 border border-border">
                <div className="text-success text-2xl mb-2">✍️</div>
                <h3 className="text-lg font-semibold mb-2">Custom Personas</h3>
                <p className="text-sm text-muted-foreground">
                  Upload specialized writer prompts for tailored synthesis styles
                </p>
              </div>
            </div>
          </>
        )}
        
        {/* Progress Indicator */}
        {isRunning && (
          <ResearchProgress
            currentState={currentState}
            progress={progress || undefined}
            isComplete={currentState === WorkflowState.COMPLETED}
            hasError={!!error}
          />
        )}
        
        {/* Results */}
        {result && (
          <>
            <ResultsDisplay result={result} />
            <div className="flex justify-center mt-6">
              <button
                onClick={handleNewResearch}
                className="px-6 py-3 bg-primary text-primary-foreground rounded-md 
                         hover:bg-primary/90 transition-smooth font-medium"
              >
                Start New Research
              </button>
            </div>
          </>
        )}
        
        {/* Error State */}
        {error && !isRunning && !result && (
          <div className="bg-destructive/10 border border-destructive rounded-lg p-6">
            <h3 className="text-lg font-semibold text-destructive mb-2">
              Research Failed
            </h3>
            <p className="text-destructive-foreground mb-4">{error}</p>
            <button
              onClick={handleNewResearch}
              className="px-4 py-2 bg-destructive text-destructive-foreground rounded-md 
                       hover:bg-destructive/90 transition-smooth"
            >
              Try Again
            </button>
          </div>
        )}
      </div>
    </MainLayout>
  )
}

export default App
