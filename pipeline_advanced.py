"""
Advanced Research Pipeline - Phase 3 Implementation
Integrates dynamic workflow, validation, semantic memory, and A/B testing
"""
from typing import Dict, Any, List, Optional
from datetime import datetime
from pathlib import Path

from pipeline import ResearchPipeline
from config import Config
from workflow.state_machine import ResearchStateMachine, WorkflowState
from validation.fact_checker import FactChecker, ValidationLevel
from memory.semantic_memory import SemanticMemory
from testing.ab_testing import ABTestManager
from research_agent import ResearchPhase


class AdvancedResearchPipeline(ResearchPipeline):
    """
    Enhanced pipeline with Phase 3 advanced features:
    - Dynamic workflow state machine
    - Fact validation system
    - Semantic memory with embeddings
    - A/B testing framework
    """
    
    def __init__(self, writer_prompt_path: Optional[str] = None, *args, **kwargs):
        """
        Initialize advanced pipeline with Phase 3 components
        
        Args:
            writer_prompt_path: Optional path to markdown file with custom writer system prompt
        """
        super().__init__(*args, **kwargs)
        
        # Initialize Phase 3 components
        self.state_machine = ResearchStateMachine()
        self.fact_checker = FactChecker(self.llm)
        self.semantic_memory = SemanticMemory(
            openai_api_key=Config.OPENAI_API_KEY,
            model=Config.EMBEDDING_MODEL,
            dimensions=Config.EMBEDDING_DIMENSIONS,
            cache_enabled=Config.EMBEDDING_CACHE_ENABLED,
            max_cache_size=Config.EMBEDDING_MAX_CACHE_SIZE
        )
        self.ab_tests = ABTestManager()
        
        # Setup A/B tests for optimization
        self._setup_ab_tests()
        
        # Tracking for adaptive workflow
        self.iterations_without_progress = 0
        self.previous_confidence = 0.0
        self.validation_results = []
        
        # Custom writer prompt (for specialized synthesis)
        self.writer_prompt_path = writer_prompt_path
        self.custom_writer_prompt = None
        
        # Load custom writer prompt if provided
        if writer_prompt_path:
            self._load_writer_prompt()
    
    def _setup_ab_tests(self):
        """Setup A/B tests for various optimizations"""
        # Test different planning strategies
        self.ab_tests.create_test(
            name="planning_strategy",
            metric="plan_quality",
            variants={
                "A": "comprehensive",  # More detailed planning
                "B": "focused"  # Quick, focused planning
            }
        )
        
        # Test analysis depth
        self.ab_tests.create_test(
            name="analysis_depth",
            metric="confidence",
            variants={
                "A": "deep",  # Deep analysis with more context
                "B": "standard"  # Standard analysis
            }
        )
    
    def execute(self, query: str, max_iterations: Optional[int] = None) -> Dict[str, Any]:
        """
        Execute research with adaptive workflow
        
        Uses state machine to dynamically adapt the research process
        """
        print(f"\n{'='*60}")
        print(f"Starting Advanced Research Pipeline (Phase 3)")
        print(f"Query: {query}")
        print(f"Model: {self.llm.model}")
        print(f"Adaptive Workflow: ENABLED")
        print(f"{'='*60}\n")
        
        self.original_query = query
        max_iterations = max_iterations or Config.MAX_RESEARCH_ITERATIONS
        
        # Adaptive workflow loop
        iteration = 0
        while (self.state_machine.current_state != WorkflowState.COMPLETED and 
               self.state_machine.current_state != WorkflowState.FAILED and
               iteration < max_iterations):
            
            iteration += 1
            current_state = self.state_machine.current_state
            
            print(f"\n--- Iteration {iteration}: State = {current_state.value.upper()} ---")
            
            # Execute state-specific logic
            if current_state == WorkflowState.PLANNING:
                self._adaptive_planning()
            elif current_state == WorkflowState.SEARCHING:
                self._adaptive_searching()
            elif current_state == WorkflowState.ANALYZING:
                self._adaptive_analyzing()
            elif current_state == WorkflowState.VALIDATING:
                self._adaptive_validating()
            elif current_state == WorkflowState.REFINING:
                self._adaptive_refining()
            elif current_state == WorkflowState.SYNTHESIZING:
                self._adaptive_synthesizing()
            
            # Build context and determine next state
            context = self._build_context()
            next_state = self.state_machine.next_state(context)
            
            print(f"→ Transitioning: {current_state.value} → {next_state.value}")
            print(f"  Confidence: {context.get('confidence', 0):.2f} | Coverage: {context.get('coverage', 0):.2f} | Contradictions: {context.get('contradictions', 0)}")
        
        # Final synthesis if not already done
        if self.state_machine.current_state == WorkflowState.COMPLETED and not self.final_report:
            print("\n[Final Synthesis]")
            self._synthesis_phase()
        
        # Save results
        print("\n[Saving Results]")
        results = self._save_results()
        
        # Add Phase 3 metadata
        results['results']['phase3_metadata'] = {
            'state_path': self.state_machine.get_state_path(),
            'total_transitions': len(self.state_machine.state_history),
            'validation_results': len(self.validation_results),
            'semantic_memory_stats': self.semantic_memory.get_stats(),
            'ab_test_results': {
                test_name: self.ab_tests.get_test(test_name).get_winner()
                for test_name in self.ab_tests.list_tests()
            }
        }
        
        print(f"\n{'='*60}")
        print(f"Advanced Research Complete!")
        print(f"State Path: {' → '.join(self.state_machine.get_state_path())}")
        print(f"Total Transitions: {len(self.state_machine.state_history)}")
        print(f"Semantic Items Stored: {len(self.semantic_memory.items)}")
        print(f"{'='*60}\n")
        
        return results
    
    def _adaptive_planning(self):
        """PLANNING state logic with A/B testing"""
        # Get variant for planning strategy
        planning_test = self.ab_tests.get_test("planning_strategy")
        variant = planning_test.get_variant()
        
        print(f"Planning variant: {variant}")
        
        # Use standard planning phase
        self._plan_phase()
        
        # If planning failed, create default plan
        if not self.research_plan:
            print("  Warning: Planning generated 0 steps, creating default plan")
            self.research_plan = [
                {"step": 1, "query": self.original_query, "type": "broad_search"},
                {"step": 2, "query": f"{self.original_query} details", "type": "specific"},
                {"step": 3, "query": f"{self.original_query} examples", "type": "examples"}
            ]
        
        # Record A/B test result
        plan_quality = len(self.research_plan) / max(Config.MAX_SEARCH_QUERIES, 1)
        planning_test.record_result(variant, plan_quality)
    
    def _adaptive_searching(self):
        """SEARCHING state logic"""
        # Execute searches from plan
        queries_to_process = self._get_next_queries(num=3)
        
        if not queries_to_process:
            print("No queries to process")
            return
        
        print(f"Processing {len(queries_to_process)} queries...")
        
        # Use parallel search from Phase 2
        results = self.orchestrator.parallel_search_and_analyze(queries_to_process)
        
        # Store in both traditional memory and semantic memory
        for i, result in enumerate(results):
            if result.get('key_findings'):
                # Store in research history
                self._store_research_step(result, len(self.agent.research_history) + 1, 
                                         queries_to_process[i] if i < len(queries_to_process) else "")
                
                # Store in semantic memory for similarity search
                for finding in result.get('key_findings', []):
                    self.semantic_memory.store(
                        content=finding.get('finding', str(finding)),
                        metadata={
                            'query': queries_to_process[i] if i < len(queries_to_process) else "",
                            'confidence': result.get('confidence', 0.5),
                            'source': finding.get('source', 'unknown')
                        }
                    )
    
    def _adaptive_analyzing(self):
        """ANALYZING state logic with semantic search"""
        if not self.agent.research_history:
            return
        
        # Get recent findings
        recent_steps = self.agent.research_history[-3:]
        
        # Use semantic search to find related findings
        for step in recent_steps:
            if step.results and step.results.get('key_findings'):
                for finding in step.results['key_findings'][:2]:  # Limit to 2 findings per step
                    finding_text = finding.get('finding', str(finding))
                    
                    # Search for related content
                    related = self.semantic_memory.search(finding_text, top_k=3, threshold=0.75)
                    
                    if related:
                        print(f"  Found {len(related)} related findings (semantic similarity)")
    
    def _adaptive_validating(self):
        """VALIDATING state logic"""
        print("Validating findings...")
        
        # If no research history, can't validate - mark as needing refinement
        if not self.agent.research_history:
            print("  No findings to validate - needs more research")
            return
        
        # Collect findings to validate
        findings_to_validate = []
        sources = []
        
        for step in self.agent.research_history:
            if step.results and step.results.get('key_findings'):
                for finding in step.results['key_findings']:
                    findings_to_validate.append(finding.get('finding', str(finding)))
                    sources.append({
                        'title': finding.get('source', 'Unknown'),
                        'content': finding.get('finding', ''),
                        'type': 'web'
                    })
        
        # If no findings collected, skip validation
        if not findings_to_validate:
            print("  No findings to validate")
            return
        
        # Validate findings (sample up to 5 for performance)
        sample_findings = findings_to_validate[:5]
        
        for finding in sample_findings:
            validation = self.fact_checker.validate_finding(finding, sources)
            self.validation_results.append(validation)
            
            print(f"  Validated: {validation.level.value} (confidence: {validation.confidence:.2f})")
            
            if validation.level == ValidationLevel.FAILED:
                print(f"    ⚠️ Validation failed: {validation.explanation[:100]}")
    
    def _adaptive_refining(self):
        """REFINING state logic"""
        print("Refining search strategy...")
        
        # Analyze what went wrong
        if not self.agent.research_history:
            # No results found - broaden search
            print("  Strategy: Broadening search terms")
        elif self.validation_results and any(v.level == ValidationLevel.FAILED for v in self.validation_results[-3:]):
            # Validation failures - find better sources
            print("  Strategy: Seeking more reliable sources")
        else:
            # Low confidence - different angle
            print("  Strategy: Exploring different perspectives")
    
    def _load_writer_prompt(self):
        """Load custom writer prompt from markdown file"""
        if not self.writer_prompt_path:
            return
        
        try:
            # Resolve path relative to current directory
            prompt_path = Path(self.writer_prompt_path)
            
            if not prompt_path.exists():
                print(f"⚠️  Warning: Writer prompt file not found: {self.writer_prompt_path}")
                return
            
            with open(prompt_path, 'r', encoding='utf-8') as f:
                self.custom_writer_prompt = f.read()
            
            print(f"✓ Loaded custom writer prompt from: {self.writer_prompt_path}")
            print(f"  Prompt length: {len(self.custom_writer_prompt)} characters\n")
            
        except Exception as e:
            print(f"⚠️  Error loading writer prompt: {e}")
            self.custom_writer_prompt = None
    
    def _synthesis_phase(self):
        """Phase 3: Synthesize with optional custom writer prompt"""
        self.agent.current_phase = ResearchPhase.SYNTHESIZING
        
        print("Synthesizing all research findings...")
        
        # Use custom writer prompt if available
        if self.custom_writer_prompt:
            print("Using specialist writer prompt for synthesis")
            self.final_report = self._synthesize_with_custom_writer()
        else:
            # Fall back to standard synthesis
            self.final_report = self.agent.synthesize_findings(self.original_query)
        
        print(f"Final report generated ({len(self.final_report)} characters)")
    
    def _synthesize_with_custom_writer(self) -> str:
        """Synthesize findings using custom writer prompt"""
        # Compile all research findings
        all_findings = []
        for step in self.agent.research_history:
            if step.results and step.results.get('key_findings'):
                all_findings.extend(step.results['key_findings'])
        
        # Format findings for the writer
        findings_text = "\n\n".join([
            f"Finding {i+1}: {finding.get('finding', str(finding))}"
            for i, finding in enumerate(all_findings)
        ])
        
        # Compile research context
        user_prompt = f"""Research Query: {self.original_query}

Research Findings Collected:
{findings_text}

Please synthesize these findings into a comprehensive response to the research query, using your specialized writing style and expertise."""
        
        # Generate with custom writer prompt as system prompt
        synthesis = self.llm.generate_with_system_prompt(
            self.custom_writer_prompt,  # Custom system prompt from markdown
            user_prompt,
            temperature=0.7  # Slightly higher for creative writing
        )
        
        return synthesis
    
    def _adaptive_synthesizing(self):
        """SYNTHESIZING state logic"""
        print("Synthesizing findings...")
        
        # Use standard synthesis (which now checks for custom writer)
        self._synthesis_phase()
        
        # Calculate synthesis quality for state machine
        synthesis_quality = self._calculate_synthesis_quality()
        print(f"  Synthesis quality: {synthesis_quality:.2f}")
    
    def _build_context(self) -> Dict[str, Any]:
        """Build context for state machine decisions"""
        # Special case: If we have no research and no plan, force refining
        if not self.agent.research_history and not self.research_plan:
            self.iterations_without_progress += 1  # Actually increment the counter
            return {
                'confidence': 0.0,
                'coverage': 0.0,
                'contradictions': 0,
                'iterations_without_progress': self.iterations_without_progress,
                'results_found': 0,
                'validation_passed': False,  # Force transition away from validating
                'synthesis_quality': 0.0
            }
        
        # Calculate metrics
        confidence = self._calculate_confidence()
        coverage = self._calculate_coverage()
        contradictions = self._count_contradictions()
        
        # Check for progress
        progress_made = abs(confidence - self.previous_confidence) > 0.05
        if not progress_made:
            self.iterations_without_progress += 1
        else:
            self.iterations_without_progress = 0
        
        self.previous_confidence = confidence
        
        # Build context dictionary
        context = {
            'confidence': confidence,
            'coverage': coverage,
            'contradictions': contradictions,
            'iterations_without_progress': self.iterations_without_progress,
            'results_found': len(self.agent.research_history),
            'validation_passed': self._validation_passed(),
            'synthesis_quality': self._calculate_synthesis_quality()
        }
        
        return context
    
    def _calculate_confidence(self) -> float:
        """Calculate average confidence across research steps"""
        if not self.agent.research_history:
            return 0.0
        
        total_confidence = sum(step.confidence for step in self.agent.research_history)
        return total_confidence / len(self.agent.research_history)
    
    def _calculate_coverage(self) -> float:
        """Calculate coverage of planned research"""
        if not self.research_plan:
            return 0.0
        
        completed = len(self.agent.research_history)
        planned = len(self.research_plan)
        
        return min(1.0, completed / max(planned, 1))
    
    def _count_contradictions(self) -> int:
        """Count contradictions in validation results"""
        if not self.validation_results:
            return 0
        
        return sum(1 for v in self.validation_results if v.level == ValidationLevel.FAILED)
    
    def _validation_passed(self) -> bool:
        """Check if recent validations passed"""
        if not self.validation_results:
            return True
        
        recent_validations = self.validation_results[-3:]
        return all(v.level != ValidationLevel.FAILED for v in recent_validations)
    
    def _calculate_synthesis_quality(self) -> float:
        """Estimate synthesis quality"""
        if not self.final_report:
            return 0.0
        
        # Simple heuristic based on length and structure
        length_score = min(1.0, len(self.final_report) / 1000)
        confidence_score = self._calculate_confidence()
        
        return (length_score + confidence_score) / 2


def main():
    """Advanced pipeline with optional custom writer prompt"""
    import argparse
    
    # Setup argument parser
    parser = argparse.ArgumentParser(
        description='Advanced Research Pipeline with Phase 3 Features',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Standard usage
  python pipeline_advanced.py "What are quantum computing breakthroughs?"
  
  # With custom writer prompt
  python pipeline_advanced.py "Explain black holes" --writer-prompt isaac.md
  
  # Custom writer with detailed query
  python pipeline_advanced.py "summarize the voynich manuscript" --writer-prompt prompts/asimov.md
        """
    )
    
    parser.add_argument(
        'query',
        help='Research query or topic to investigate'
    )
    
    parser.add_argument(
        '--writer-prompt',
        type=str,
        default=None,
        metavar='PATH',
        dest='writer_prompt',
        help='Path to markdown file containing specialist writer system prompt (relative to current directory)'
    )
    
    args = parser.parse_args()
    
    # Initialize pipeline with optional custom writer
    pipeline = AdvancedResearchPipeline(writer_prompt_path=args.writer_prompt)
    
    # Execute research
    results = pipeline.execute(args.query)
    
    # Display summary
    print("\n" + "="*60)
    print("FINAL REPORT PREVIEW")
    print("="*60)
    print(results['results']['final_report'][:500] + "...")
    print("\n" + "="*60)
    print("PHASE 3 METRICS")
    print("="*60)
    phase3 = results['results']['phase3_metadata']
    print(f"State Path: {' → '.join(phase3['state_path'])}")
    print(f"Transitions: {phase3['total_transitions']}")
    print(f"Validations: {phase3['validation_results']}")
    print(f"Semantic Items: {phase3['semantic_memory_stats']['total_items']}")
    print("="*60)


if __name__ == "__main__":
    main()
