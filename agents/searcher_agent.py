"""
Searcher Agent - Specializes in query optimization and search execution
"""
from agents.base_agent import BaseAgent, AgentRole
from typing import Dict, Any, List
import time


class SearcherAgent(BaseAgent):
    """Expert at optimizing queries and executing searches"""
    
    def __init__(self, llm_client, search_orchestrator):
        super().__init__(llm_client, AgentRole.SEARCHER)
        self.search = search_orchestrator
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute search with query optimization
        
        Input:
            - query: Search query
            - tools: List of search tools to use
            - num_results: Number of results per tool
        
        Output:
            - results: Combined search results
            - query_used: Optimized query
            - sources: List of sources used
        """
        start_time = time.time()
        
        try:
            query = input_data["query"]
            tools = input_data.get("tools", ["web"])
            num_results = input_data.get("num_results", 5)
            
            # Optimize query (if needed)
            optimized_query = self._optimize_query(query)
            
            # Execute search
            results = self.search.search_and_combine(
                query=optimized_query,
                tools=tools,
                num_results=num_results
            )
            
            result = {
                "results": results,
                "query_used": optimized_query,
                "num_results": len(results),
                "sources": tools,
                "metadata": {
                    "agent": self.role.value,
                    "original_query": query
                }
            }
            
            # Update metrics
            response_time = time.time() - start_time
            self.update_metrics(success=len(results) > 0, response_time=response_time)
            
            return result
            
        except Exception as e:
            self.update_metrics(success=False, response_time=time.time() - start_time)
            return {
                "results": [],
                "error": str(e)
            }
    
    def _optimize_query(self, query: str) -> str:
        """Optimize search query for better results"""
        # Could use LLM to rephrase/optimize
        # For now, return as-is
        return query
