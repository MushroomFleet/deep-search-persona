"""
Deep Research Pipeline - Main orchestrator
"""
import json
import os
from datetime import datetime
from typing import Dict, Any, List, Optional
from pathlib import Path

from config import Config
from llm_client import OpenRouterClient
from research_agent import ResearchAgent, ResearchStep, ResearchPhase
from search_tools import SearchOrchestrator, WebSearchTool, AcademicSearchTool
from agents.orchestrator import AgentOrchestrator
from agents.base_agent import AgentRole
from memory.research_memory import ResearchMemory


class ResearchPipeline:
    """
    Main orchestrator for the deep research agentic pipeline
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        search_api_key: Optional[str] = None
    ):
        """
        Initialize the research pipeline
        
        Args:
            api_key: OpenRouter API key
            model: Model to use (defaults to Grok)
            search_api_key: API key for search tools
        """
        # Validate configuration
        Config.validate()
        
        # Initialize LLM client
        self.llm = OpenRouterClient(api_key=api_key, model=model)
        
        # Initialize research agent
        self.agent = ResearchAgent(self.llm)
        
        # Initialize search tools
        self.search = SearchOrchestrator()
        self.search.register_tool("web", WebSearchTool(api_key=search_api_key))
        self.search.register_tool("academic", AcademicSearchTool())
        
        # Initialize multi-agent system (Phase 2)
        self.orchestrator = AgentOrchestrator(self.llm, self.search)
        
        # Initialize memory system (Phase 2)
        self.memory = ResearchMemory()
        
        # Pipeline state
        self.original_query: str = ""
        self.research_plan: List[Dict[str, Any]] = []
        self.final_report: str = ""
        self.metadata: Dict[str, Any] = {}
        
        # Setup output directory
        self.output_dir = Path(Config.OUTPUT_DIR)
        self.output_dir.mkdir(exist_ok=True)
    
    def execute(self, query: str, max_iterations: Optional[int] = None) -> Dict[str, Any]:
        """
        Execute the full research pipeline
        
        Args:
            query: Research question or topic
            max_iterations: Maximum number of research iterations (None = use config)
            
        Returns:
            Dictionary with final report and metadata
        """
        print(f"\n{'='*60}")
        print(f"Starting Deep Research Pipeline")
        print(f"Query: {query}")
        print(f"Model: {self.llm.model}")
        print(f"{'='*60}\n")
        
        self.original_query = query
        max_iterations = max_iterations or Config.MAX_RESEARCH_ITERATIONS
        
        # Phase 1: Planning
        print("\n[Phase 1: Planning]")
        self._plan_phase()
        
        # Phase 2: Research Loop
        print("\n[Phase 2: Research Execution]")
        self._research_loop(max_iterations)
        
        # Phase 3: Synthesis
        print("\n[Phase 3: Synthesis]")
        self._synthesis_phase()
        
        # Phase 4: Save Results
        print("\n[Phase 4: Saving Results]")
        results = self._save_results()
        
        print(f"\n{'='*60}")
        print(f"Research Complete!")
        print(f"Total steps: {len(self.agent.research_history)}")
        print(f"Output saved to: {results['output_file']}")
        print(f"{'='*60}\n")
        
        return results
    
    def _plan_phase(self):
        """Phase 1: Create research plan using PlannerAgent"""
        self.agent.current_phase = ResearchPhase.PLANNING
        
        # Use specialized PlannerAgent (Phase 2)
        planner = self.orchestrator.get_agent(AgentRole.PLANNER)
        
        result = planner.process({
            "query": self.original_query,
            "domain": "general",
            "depth": "comprehensive"
        })
        
        self.research_plan = result["plan"]
        
        print(f"Research plan created with {len(self.research_plan)} steps (confidence: {result['confidence']:.2f}):")
        for step in self.research_plan:
            print(f"  Step {step['step']}: {step['query']}")
    
    def _research_loop(self, max_iterations: int):
        """Phase 2: Execute research steps with parallel processing"""
        iteration = 0
        
        while iteration < max_iterations:
            iteration += 1
            print(f"\n--- Iteration {iteration}/{max_iterations} ---")
            
            # Collect next queries to process
            queries_to_process = self._get_next_queries(num=3)
            
            if not queries_to_process:
                print("No more queries to process")
                break
            
            print(f"Processing {len(queries_to_process)} queries in parallel...")
            
            # PARALLEL EXECUTION - Major speedup! (Phase 2)
            results = self.orchestrator.parallel_search_and_analyze(queries_to_process)
            
            # Store results in memory and history
            for i, result in enumerate(results):
                if result.get('key_findings'):
                    self._store_research_step(result, iteration, queries_to_process[i] if i < len(queries_to_process) else "")
            
            # Check if we should continue
            if self._should_complete():
                print("Research objectives met")
                break
        
        self.agent.current_phase = ResearchPhase.COMPLETED
    
    def _execute_search_step(self, query: str, step_num: int):
        """Execute a single search step"""
        print(f"Executing search: {query}")
        
        # Perform search
        search_results = self.search.search_and_combine(
            query=query,
            tools=["web"],  # Can expand to multiple tools
            num_results=Config.SEARCH_RESULTS_PER_QUERY
        )
        
        print(f"Found {len(search_results)} results")
        
        # Analyze results
        print("Analyzing results...")
        analysis = self.agent.analyze_results(query, search_results)
        
        print(f"Key findings: {len(analysis.get('key_findings', []))} points")
        print(f"Confidence: {analysis.get('confidence', 0):.2f}")
        
        # Create research step
        step = ResearchStep(
            step_number=step_num,
            phase=ResearchPhase.SEARCHING,
            query=query,
            reasoning=f"Searching for: {query}",
            confidence=analysis.get('confidence', 0.5),
            results=analysis
        )
        
        self.agent.add_research_step(step)
        
        # Save intermediate results if configured
        if Config.SAVE_INTERMEDIATE_RESULTS:
            self._save_intermediate_step(step)
    
    def _deep_analysis(self):
        """Perform deeper analysis of existing findings"""
        if not self.agent.research_history:
            return
        
        # Compile recent findings
        recent_steps = self.agent.research_history[-3:]
        findings = [step.results for step in recent_steps if step.results]
        
        # Use LLM to find patterns or gaps
        system_prompt = """You are analyzing research findings to identify:
        1. Common themes or patterns
        2. Contradictions or inconsistencies
        3. Information gaps that need more research
        
        Provide insights in JSON format."""
        
        user_prompt = f"""Analyze these research findings:
        
{json.dumps(findings, indent=2)}

What patterns, gaps, or contradictions do you see?"""
        
        analysis = self.llm.generate_with_system_prompt(system_prompt, user_prompt)
        print(f"Deep analysis: {analysis[:200]}...")
    
    def _synthesis_phase(self):
        """Phase 3: Synthesize all findings"""
        self.agent.current_phase = ResearchPhase.SYNTHESIZING
        
        print("Synthesizing all research findings...")
        self.final_report = self.agent.synthesize_findings(self.original_query)
        
        print(f"Final report generated ({len(self.final_report)} characters)")
    
    def _get_next_queries(self, num: int = 3) -> List[str]:
        """Get next queries from plan or generate new ones"""
        queries = []
        completed_steps = len(self.agent.research_history)
        
        # Get queries from remaining plan steps
        for i, step in enumerate(self.research_plan[completed_steps:completed_steps + num]):
            if step.get('query'):
                queries.append(step['query'])
        
        return queries
    
    def _should_complete(self) -> bool:
        """Determine if research is complete"""
        # Simple heuristic: completed all planned steps
        completed_steps = len(self.agent.research_history)
        return completed_steps >= len(self.research_plan)
    
    def _store_research_step(self, analysis: Dict[str, Any], iteration: int, query: str):
        """Store research step in history and memory"""
        # Store in traditional research history
        step = ResearchStep(
            step_number=iteration,
            phase=ResearchPhase.SEARCHING,
            query=query,
            reasoning=f"Parallel search and analysis for: {query}",
            confidence=analysis.get('confidence', 0.5),
            results=analysis
        )
        self.agent.add_research_step(step)
        
        # Store in memory system (Phase 2)
        if analysis.get('key_findings'):
            importance = analysis.get('confidence', 0.5)
            tags = [query.split()[0], "findings"]  # Simple tagging
            self.memory.store(
                content={"findings": analysis['key_findings'], "query": query},
                importance=importance,
                tags=tags
            )
        
        print(f"Stored step {iteration}: {len(analysis.get('key_findings', []))} findings (confidence: {analysis.get('confidence', 0):.2f})")
    
    def _save_results(self) -> Dict[str, Any]:
        """Save final results to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"research_{timestamp}.json"
        filepath = self.output_dir / filename
        
        # Compile results
        results = {
            "query": self.original_query,
            "model": self.llm.model,
            "timestamp": timestamp,
            "research_plan": self.research_plan,
            "research_steps": [step.to_dict() for step in self.agent.research_history],
            "final_report": self.final_report,
            "metadata": {
                "total_steps": len(self.agent.research_history),
                "avg_confidence": sum(s.confidence for s in self.agent.research_history) / len(self.agent.research_history) if self.agent.research_history else 0,
                "phases_completed": list(set(s.phase.value for s in self.agent.research_history)),
                "agent_stats": self.orchestrator.get_system_status(),
                "memory_stats": self.memory.get_stats()
            }
        }
        
        # Save to file
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2)
        
        # Also save human-readable report
        report_filename = f"report_{timestamp}.md"
        report_filepath = self.output_dir / report_filename
        
        with open(report_filepath, 'w', encoding='utf-8') as f:
            f.write(f"# Research Report\n\n")
            f.write(f"**Query:** {self.original_query}\n\n")
            f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(f"**Model:** {self.llm.model}\n\n")
            f.write(f"---\n\n")
            f.write(self.final_report)
        
        return {
            "output_file": str(filepath),
            "report_file": str(report_filepath),
            "results": results
        }
    
    def _save_intermediate_step(self, step: ResearchStep):
        """Save intermediate research step"""
        filename = f"step_{step.step_number}.json"
        filepath = self.output_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(step.to_dict(), f, indent=2)


def main():
    """Example usage"""
    import sys
    
    # Get query from command line or use default
    query = sys.argv[1] if len(sys.argv) > 1 else "What are the latest developments in quantum computing?"
    
    # Initialize and run pipeline
    pipeline = ResearchPipeline()
    results = pipeline.execute(query)
    
    # Display summary
    print("\n" + "="*60)
    print("FINAL REPORT PREVIEW")
    print("="*60)
    print(results['results']['final_report'][:500] + "...")
    print("\n" + "="*60)


if __name__ == "__main__":
    main()
