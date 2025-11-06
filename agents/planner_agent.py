"""
Planner Agent - Specializes in research planning
"""
from agents.base_agent import BaseAgent, AgentRole
from prompt_library import PromptLibrary, PromptVersion
from few_shot_examples import FewShotExamples
from typing import Dict, Any, List
import time


class PlannerAgent(BaseAgent):
    """Expert at creating structured research plans"""
    
    def __init__(self, llm_client):
        super().__init__(llm_client, AgentRole.PLANNER)
        self.prompt_lib = PromptLibrary()
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create research plan
        
        Input:
            - query: Research question
            - domain: Domain/field (optional)
            - depth: Depth level (optional)
        
        Output:
            - plan: List of research steps
            - confidence: Planning confidence
        """
        start_time = time.time()
        
        try:
            query = input_data["query"]
            domain = input_data.get("domain", "general")
            depth = input_data.get("depth", "comprehensive")
            
            # Get prompt and examples
            prompt_template = self.prompt_lib.get_prompt("research_planner", PromptVersion.V2)
            few_shot_examples = FewShotExamples.get_examples("research_planning", n=2)
            
            # Format prompt
            system_prompt = prompt_template.format(
                query=query,
                domain=domain,
                depth_level=depth,
                few_shot_examples=few_shot_examples
            )
            
            # Generate plan
            response = self.llm.generate_with_system_prompt(
                system_prompt,
                f"Create research plan for: {query}"
            )
            
            # Extract and validate
            from research_agent import ResearchAgent  # Import extraction logic
            plan = ResearchAgent._robust_json_extract(response, fallback_plan=query)
            
            # Self-validate
            is_valid, issues = self._validate_plan(plan)
            
            result = {
                "plan": plan,
                "confidence": 0.9 if is_valid else 0.6,
                "is_valid": is_valid,
                "issues": issues,
                "metadata": {
                    "agent": self.role.value,
                    "query": query,
                    "steps": len(plan)
                }
            }
            
            # Update metrics
            response_time = time.time() - start_time
            self.update_metrics(success=is_valid, response_time=response_time)
            
            return result
            
        except Exception as e:
            self.update_metrics(success=False, response_time=time.time() - start_time)
            return {
                "plan": [],
                "confidence": 0.0,
                "error": str(e)
            }
    
    def _validate_plan(self, plan: List[Dict]) -> tuple[bool, List[str]]:
        """Validate research plan quality"""
        issues = []
        
        # Check structure
        if not plan or len(plan) == 0:
            issues.append("Plan is empty")
        
        if len(plan) > 5:
            issues.append("Too many steps (max 5 recommended)")
        
        # Check each step
        required_keys = ["step", "query", "reasoning"]
        for step in plan:
            missing = [k for k in required_keys if k not in step]
            if missing:
                issues.append(f"Step {step.get('step', '?')} missing: {missing}")
        
        return len(issues) == 0, issues
