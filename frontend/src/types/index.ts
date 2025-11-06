/**
 * Core type definitions for Deep Search Frontend
 */

// Persona file representation
export interface Persona {
  id: string;
  name: string;
  filename: string;
  content: string;
  uploadedAt: Date;
}

// Research job configuration
export interface ResearchJob {
  id: string;
  query: string;
  persona?: Persona;
  status: JobStatus;
  createdAt: Date;
  startedAt?: Date;
  completedAt?: Date;
  error?: string;
}

// Job execution status
export const JobStatus = {
  PENDING: 'pending',
  RUNNING: 'running',
  COMPLETED: 'completed',
  FAILED: 'failed',
} as const;

export type JobStatus = typeof JobStatus[keyof typeof JobStatus];

// Pipeline execution state (from workflow/state_machine.py)
export const WorkflowState = {
  PLANNING: 'planning',
  SEARCHING: 'searching',
  ANALYZING: 'analyzing',
  VALIDATING: 'validating',
  REFINING: 'refining',
  SYNTHESIZING: 'synthesizing',
  COMPLETED: 'completed',
  FAILED: 'failed',
} as const;

export type WorkflowState = typeof WorkflowState[keyof typeof WorkflowState];

// Real-time pipeline output message
export interface PipelineMessage {
  type: 'state' | 'progress' | 'result' | 'error';
  timestamp: Date;
  data: any;
}

// Progress update from pipeline
export interface ProgressUpdate {
  iteration: number;
  state: WorkflowState;
  confidence: number;
  coverage: number;
  contradictions: number;
  message: string;
}

// Final research results
export interface ResearchResult {
  query: string;
  final_report: string;
  research_history: ResearchStep[];
  phase3_metadata: Phase3Metadata;
  timestamp: string;
}

// Individual research step
export interface ResearchStep {
  step_number: number;
  query: string;
  confidence: number;
  results: {
    key_findings: Finding[];
    sources: Source[];
  };
}

// Research finding
export interface Finding {
  finding: string;
  source: string;
  confidence: number;
}

// Research source
export interface Source {
  title: string;
  url?: string;
  type: string;
}

// Phase 3 metadata
export interface Phase3Metadata {
  state_path: string[];
  total_transitions: number;
  validation_results: number;
  semantic_memory_stats: {
    total_items: number;
    cache_hits: number;
    cache_misses: number;
  };
  ab_test_results: Record<string, string>;
}
