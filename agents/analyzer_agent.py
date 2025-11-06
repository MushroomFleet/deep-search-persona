"""
Analyzer Agent - Specializes in deep analysis of search results
"""
from agents.base_agent import BaseAgent, AgentRole
from prompt_library import PromptLibrary, PromptVersion
from typing import Dict, Any, List
import time


class AnalyzerAgent(BaseAgent):
    """Expert at analyzing and extracting insights from data"""
    
    def __init__(self, llm_client):
        super().__init__(llm_client, AgentRole.ANALYZER)
        self.prompt_lib = PromptLibrary()
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze search results
        
        Input:
            - query: Original search query
            - results: Search results to analyze
        
        Output:
            - key_findings: Extracted findings
            - confidence: Analysis confidence
            - gaps: Identified knowledge gaps
            - contradictions: Found contradictions
        """
        start_time = time.time()
        
        try:
            query = input_data["query"]
            results = input_data["results"]
            
            # Format results
            results_text = self._format_results(results)
            
            # Get analysis prompt
            prompt_template = self.prompt_lib.get_prompt("result_analyzer", PromptVersion.V2)
            
            system_prompt = prompt_template.format(
                query=query,
                results_text=results_text,
                result_count=len(results)
            )
            
            # Generate analysis
            response = self.llm.generate_with_system_prompt(
                system_prompt,
                f"Analyze results for: {query}",
                max_tokens=2000
            )
            
            # Extract analysis
            from research_agent import ResearchAgent
            analysis = ResearchAgent._robust_json_extract(response)
            
            result = {
                **analysis,
                "metadata": {
                    "agent": self.role.value,
                    "results_analyzed": len(results)
                }
            }
            
            # Update metrics
            response_time = time.time() - start_time
            confidence = analysis.get("confidence", 0.5)
            self.update_metrics(success=confidence > 0.6, response_time=response_time)
            
            return result
            
        except Exception as e:
            self.update_metrics(success=False, response_time=time.time() - start_time)
            return {
                "key_findings": [],
                "confidence": 0.0,
                "error": str(e)
            }
    
    def _format_results(self, results: List[Dict]) -> str:
        """Format search results for analysis"""
        formatted = []
        for i, result in enumerate(results[:5], 1):
            formatted.append(
                f"Result {i}:\n"
                f"Title: {result.get('title', 'N/A')}\n"
                f"Content: {result.get('content', result.get('snippet', 'N/A'))}\n"
            )
        return "\n\n".join(formatted)
