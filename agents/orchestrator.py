"""
Agent Orchestrator - Coordinates all specialized agents
"""
from agents.base_agent import BaseAgent, AgentRole, AgentMessage
from agents.planner_agent import PlannerAgent
from agents.searcher_agent import SearcherAgent
from agents.analyzer_agent import AnalyzerAgent
from typing import Dict, Any, List, Optional
import asyncio
from concurrent.futures import ThreadPoolExecutor
import time


class AgentOrchestrator:
    """Coordinates communication and work distribution among agents"""
    
    def __init__(self, llm_client, search_orchestrator):
        """Initialize all specialized agents"""
        self.agents = {
            AgentRole.PLANNER: PlannerAgent(llm_client),
            AgentRole.SEARCHER: SearcherAgent(llm_client, search_orchestrator),
            AgentRole.ANALYZER: AnalyzerAgent(llm_client),
            # Future: ValidatorAgent, SynthesizerAgent, etc.
        }
        
        self.message_bus = []
        self.executor = ThreadPoolExecutor(max_workers=5)
    
    def route_message(self, message: AgentMessage):
        """Route message to appropriate agent"""
        recipient_agent = self.agents.get(message.recipient)
        if recipient_agent:
            recipient_agent.receive_message(message)
        else:
            print(f"Warning: No agent found for role {message.recipient}")
    
    def broadcast(self, sender: AgentRole, message_type: str, content: Dict[str, Any]):
        """Broadcast message to all agents"""
        for role, agent in self.agents.items():
            if role != sender:
                message = AgentMessage(
                    sender=sender,
                    recipient=role,
                    message_type=message_type,
                    content=content
                )
                agent.receive_message(message)
    
    def get_agent(self, role: AgentRole) -> Optional[BaseAgent]:
        """Get agent by role"""
        return self.agents.get(role)
    
    def parallel_search_and_analyze(self, queries: List[str]) -> List[Dict[str, Any]]:
        """
        Execute multiple searches in parallel and analyze results
        
        This is a key optimization over sequential processing
        """
        results = []
        
        # Create search tasks
        search_tasks = []
        for query in queries[:3]:  # Limit parallelism
            task = self.executor.submit(
                self._search_task,
                query
            )
            search_tasks.append((query, task))
        
        # Wait for all searches to complete
        search_results = []
        for query, task in search_tasks:
            try:
                result = task.result(timeout=30)
                search_results.append({'query': query, 'data': result})
            except Exception as e:
                print(f"Search failed for '{query}': {e}")
                search_results.append({'query': query, 'data': {'results': []}})
        
        # Analyze results in parallel
        analysis_tasks = []
        for search_result in search_results:
            task = self.executor.submit(
                self._analyze_task,
                search_result['query'],
                search_result['data']['results']
            )
            analysis_tasks.append(task)
        
        # Collect analyses
        for task in analysis_tasks:
            try:
                analysis = task.result(timeout=30)
                results.append(analysis)
            except Exception as e:
                print(f"Analysis failed: {e}")
        
        return results
    
    def _search_task(self, query: str) -> Dict[str, Any]:
        """Execute single search task"""
        searcher = self.agents[AgentRole.SEARCHER]
        return searcher.process({
            "query": query,
            "tools": ["web"],
            "num_results": 5
        })
    
    def _analyze_task(self, query: str, results: List[Dict]) -> Dict[str, Any]:
        """Execute single analysis task"""
        analyzer = self.agents[AgentRole.ANALYZER]
        return analyzer.process({
            "query": query,
            "results": results
        })
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get status of all agents"""
        return {
            role.value: agent.get_status()
            for role, agent in self.agents.items()
        }
    
    def shutdown(self):
        """Cleanup resources"""
        self.executor.shutdown(wait=True)
