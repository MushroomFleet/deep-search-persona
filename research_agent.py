"""
Research Agent - Core agentic component for autonomous research
"""
import json
import re
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum
from llm_client import OpenRouterClient
from config import Config
from prompt_library import PromptLibrary, PromptVersion
from few_shot_examples import FewShotExamples


class JSONExtractionError(Exception):
    """Raised when all JSON extraction strategies fail"""
    pass


class ResearchPhase(Enum):
    """Phases of the research process"""
    PLANNING = "planning"
    SEARCHING = "searching"
    ANALYZING = "analyzing"
    SYNTHESIZING = "synthesizing"
    VALIDATING = "validating"
    COMPLETED = "completed"


@dataclass
class ResearchStep:
    """Represents a single step in the research process"""
    step_number: int
    phase: ResearchPhase
    query: str
    reasoning: str
    confidence: float
    results: Optional[Any] = None
    
    def to_dict(self) -> dict:
        data = asdict(self)
        data['phase'] = self.phase.value
        return data


class ResearchAgent:
    """
    Autonomous research agent that plans and executes research tasks
    """
    
    def __init__(self, llm_client: OpenRouterClient):
        self.llm = llm_client
        self.research_history: List[ResearchStep] = []
        self.knowledge_base: Dict[str, Any] = {}
        self.current_phase = ResearchPhase.PLANNING
        self.prompt_lib = PromptLibrary()
    
    @staticmethod
    def _robust_json_extract(
        response: str, 
        fallback_plan: Optional[Any] = None,
        llm_client: Optional[OpenRouterClient] = None
    ) -> Any:
        """
        Multi-strategy JSON extraction with automatic repair
        
        Strategies (in order):
        1. Direct JSON parse
        2. Extract from markdown code blocks
        3. Extract with regex patterns
        4. Auto-repair common issues
        5. LLM-based repair (if llm_client provided)
        6. Fallback to simple structure
        
        Args:
            response: The raw response string
            fallback_plan: Optional fallback structure if all parsing fails
            llm_client: Optional LLM client for LLM-based repair
            
        Returns:
            Parsed JSON object
            
        Raises:
            JSONExtractionError: If all strategies fail and no fallback provided
        """
        
        # Strategy 1: Direct parse
        try:
            return json.loads(response.strip())
        except json.JSONDecodeError:
            pass
        
        # Strategy 2: Extract from code blocks
        try:
            code_block_pattern = r'```(?:json)?\s*([\s\S]*?)\s*```'
            matches = re.findall(code_block_pattern, response)
            if matches:
                return json.loads(matches[0].strip())
        except (json.JSONDecodeError, IndexError):
            pass
        
        # Strategy 3: Find JSON-like structures
        try:
            # Look for array brackets or object braces
            json_pattern = r'(\[[\s\S]*\]|\{[\s\S]*\})'
            matches = re.findall(json_pattern, response)
            if matches:
                return json.loads(matches[0])
        except (json.JSONDecodeError, IndexError):
            pass
        
        # Strategy 4: Auto-repair common issues
        try:
            repaired = ResearchAgent._repair_json(response)
            return json.loads(repaired)
        except json.JSONDecodeError:
            pass
        
        # Strategy 5: LLM-based repair (expensive but effective)
        if llm_client:
            try:
                repaired = ResearchAgent._llm_json_repair(response, llm_client)
                return json.loads(repaired)
            except json.JSONDecodeError:
                pass
        
        # Strategy 6: Fallback
        if fallback_plan:
            return ResearchAgent._create_fallback_structure(fallback_plan)
        
        # All strategies failed
        raise JSONExtractionError(
            f"Failed to extract JSON from response. First 200 chars: {response[:200]}"
        )
    
    @staticmethod
    def _repair_json(text: str) -> str:
        """Attempt to repair common JSON issues"""
        # Remove markdown formatting
        text = re.sub(r'```(?:json)?', '', text)
        text = text.strip()
        
        # Fix common issues
        # 1. Remove trailing commas first
        text = re.sub(r',(\s*[\]}])', r'\1', text)
        
        # 2. Replace single quotes with double quotes for both keys and values
        text = text.replace("'", '"')
        
        # 3. Add missing commas between objects in arrays
        text = re.sub(r'\}\s*\{', '},{', text)
        
        return text
    
    @staticmethod
    def _llm_json_repair(broken_json: str, llm_client: OpenRouterClient) -> str:
        """Use LLM to repair JSON (last resort)"""
        repair_prompt = f"""Fix this broken JSON and return ONLY valid JSON:

{broken_json}

Return the corrected JSON without any explanation or markdown formatting."""
        
        response = llm_client.generate_with_system_prompt(
            "You are a JSON repair expert. Return only valid JSON.",
            repair_prompt,
            temperature=0.1  # Low temperature for deterministic output
        )
        
        return response.strip()
    
    @staticmethod
    def _create_fallback_structure(query: str) -> List[Dict[str, Any]]:
        """Create a simple fallback research plan"""
        return [{
            "step": 1,
            "query": query,
            "reasoning": "Direct search for the main query (fallback mode)",
            "expected_info": "General information about the topic",
            "validation_criteria": "Relevant results returned",
            "confidence_threshold": 0.5
        }]
    
    def _validate_research_plan(self, plan: List[Dict[str, Any]]) -> tuple[bool, List[str]]:
        """
        Agent validates its own research plan
        
        Args:
            plan: The research plan to validate
            
        Returns:
            Tuple of (is_valid, list of issues)
        """
        
        validation_prompt = f"""<task>
Review this research plan for quality and coherence.
</task>

<plan>
{json.dumps(plan, indent=2)}
</plan>

<validation_criteria>
1. Are questions atomic and focused (not too broad)?
2. Is there logical progression (foundational → specific)?
3. Are there redundant or overlapping queries?
4. Does it comprehensively cover the topic?
5. Are validation criteria specific and measurable?
6. Is the number of steps appropriate (3-5 ideal)?
</validation_criteria>

<output_format>
Return ONLY valid JSON:
{{
  "is_valid": true/false,
  "issues": ["issue 1", "issue 2", ...],
  "suggestions": ["suggestion 1", "suggestion 2", ...],
  "quality_score": 0.X
}}
</output_format>"""
        
        response = self.llm.generate_with_system_prompt(
            "You are a research plan validator ensuring quality and coherence.",
            validation_prompt
        )
        
        try:
            validation = self._robust_json_extract(response, llm_client=self.llm)
            return validation.get('is_valid', False), validation.get('issues', [])
        except JSONExtractionError:
            # If validation fails, assume plan is okay
            return True, []
        
    def plan_research(self, query: str, max_attempts: int = 2) -> List[Dict[str, Any]]:
        """
        Create a research plan with self-validation
        
        Args:
            query: The research question or topic
            max_attempts: Maximum validation attempts
            
        Returns:
            List of research steps to execute
        """
        for attempt in range(max_attempts):
            # Generate plan using V2 prompt template
            plan = self._generate_plan(query)
            
            # Validate plan
            is_valid, issues = self._validate_research_plan(plan)
            
            if is_valid:
                return plan
            
            # If invalid, add feedback for retry
            if attempt < max_attempts - 1:
                feedback = f"Previous plan had issues: {', '.join(issues)}. Please revise."
                query = f"{query}\n\nFeedback: {feedback}"
        
        # Return best attempt
        return plan
    
    def _generate_plan(self, query: str) -> List[Dict[str, Any]]:
        """Generate research plan using V2 prompt template"""
        
        # Get prompt template
        prompt_template = self.prompt_lib.get_prompt("research_planner", PromptVersion.V2)
        
        # Get few-shot examples
        few_shot = FewShotExamples.get_examples("research_planning", n=2)
        
        # Format prompt
        system_prompt = prompt_template.format(
            query=query,
            domain="general",  # Could be detected automatically
            depth_level="comprehensive",
            few_shot_examples=few_shot
        )
        
        user_prompt = f"Create research plan for: {query}"
        
        response = self.llm.generate_with_system_prompt(system_prompt, user_prompt)
        
        # Use robust extraction
        return self._robust_json_extract(response, fallback_plan=query, llm_client=self.llm)
    
    def decide_next_action(self, current_context: Dict[str, Any]) -> Dict[str, str]:
        """
        Agent decides what to do next based on current research state (using V2 prompt)
        
        Args:
            current_context: Dictionary containing current research state
            
        Returns:
            Dictionary with 'action' and 'reasoning'
        """
        # Get prompt template
        prompt_template = self.prompt_lib.get_prompt("decision_maker", PromptVersion.V2)
        
        # Format prompt
        system_prompt = prompt_template.format(
            original_query=current_context.get('original_query', 'N/A'),
            steps_completed=len(self.research_history),
            current_phase=self.current_phase.value,
            last_findings=json.dumps(current_context.get('last_findings', {}), indent=2),
            remaining_questions=json.dumps(current_context.get('remaining_questions', []), indent=2),
            confidence_trend=str(current_context.get('confidence_trend', []))
        )
        
        user_prompt = "Analyze the current state and decide the next action."
        
        response = self.llm.generate_with_system_prompt(system_prompt, user_prompt)
        
        # Use robust extraction with fallback
        try:
            return self._robust_json_extract(response, llm_client=self.llm)
        except JSONExtractionError:
            # Default action
            return {
                "action": "search",
                "reasoning": "Continue gathering information (fallback decision)",
                "confidence": 0.5,
                "next_query": current_context.get('original_query', ''),
                "priority": "medium"
            }
    
    def analyze_results(self, query: str, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze search results to extract key information (using V2 prompt)
        
        Args:
            query: The query that was searched
            results: List of search result dictionaries
            
        Returns:
            Analysis with key findings and insights
        """
        # Get prompt template
        prompt_template = self.prompt_lib.get_prompt("result_analyzer", PromptVersion.V2)
        
        # Format results for analysis
        results_text = "\n\n".join([
            f"Result {i+1}:\nTitle: {r.get('title', 'N/A')}\n"
            f"Content: {r.get('content', r.get('snippet', 'N/A'))}"
            for i, r in enumerate(results[:5])  # Limit to top 5 results
        ])
        
        # Format prompt
        system_prompt = prompt_template.format(
            query=query,
            results_text=results_text,
            result_count=min(len(results), 5)
        )
        
        user_prompt = "Analyze the provided search results."
        
        response = self.llm.generate_with_system_prompt(
            system_prompt, 
            user_prompt,
            max_tokens=2000
        )
        
        # Use robust extraction with fallback
        try:
            return self._robust_json_extract(response, llm_client=self.llm)
        except JSONExtractionError:
            # Return basic analysis as fallback
            return {
                "key_findings": [{"finding": "Information gathered but parsing failed", "source": "System", "confidence": 0.5}],
                "confidence": 0.5,
                "source_quality": {"academic": 0, "news": 0, "other": len(results)},
                "gaps": ["Unable to parse analysis"],
                "contradictions": [],
                "summary": response[:500] if response else "Analysis failed",
                "recommended_next_queries": []
            }
    
    def synthesize_findings(self, original_query: str) -> str:
        """
        Synthesize all research findings into a comprehensive answer (using V2 prompt)
        
        Args:
            original_query: The original research question
            
        Returns:
            Comprehensive synthesized answer
        """
        # Get prompt template
        prompt_template = self.prompt_lib.get_prompt("synthesizer", PromptVersion.V2)
        
        # Compile all research history
        research_summary = "\n\n".join([
            f"Step {step.step_number} ({step.phase.value}):\n"
            f"Query: {step.query}\n"
            f"Findings: {json.dumps(step.results, indent=2) if step.results else 'No results'}"
            for step in self.research_history
        ])
        
        # Format prompt
        system_prompt = prompt_template.format(
            original_query=original_query,
            research_summary=research_summary,
            total_steps=len(self.research_history)
        )
        
        user_prompt = "Synthesize all research findings into a comprehensive report."
        
        response = self.llm.generate_with_system_prompt(
            system_prompt, 
            user_prompt,
            max_tokens=3000
        )
        
        return response
    
    def add_research_step(self, step: ResearchStep):
        """Add a completed research step to history"""
        self.research_history.append(step)
        
        # Update knowledge base
        if step.results:
            self.knowledge_base[f"step_{step.step_number}"] = step.results
    
    def get_context(self, original_query: str) -> Dict[str, Any]:
        """Get current research context for decision making"""
        last_step = self.research_history[-1] if self.research_history else None
        
        return {
            "original_query": original_query,
            "steps_completed": len(self.research_history),
            "current_phase": self.current_phase.value,
            "last_findings": last_step.results if last_step else {},
            "remaining_questions": [],  # Could be populated based on gaps
            "confidence_trend": [s.confidence for s in self.research_history[-3:]]
        }
