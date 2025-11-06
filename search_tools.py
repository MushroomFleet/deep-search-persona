"""
Search Tools - Interface for various search APIs and data sources
"""
import requests
from typing import List, Dict, Any, Optional
from abc import ABC, abstractmethod
import json


class SearchTool(ABC):
    """Abstract base class for search tools"""
    
    @abstractmethod
    def search(self, query: str, num_results: int = 5) -> List[Dict[str, Any]]:
        """Execute a search and return results"""
        pass


class WebSearchTool(SearchTool):
    """
    Web search tool - can integrate with various search APIs
    Examples: Brave Search, Serper, Tavily, etc.
    """
    
    def __init__(self, api_key: Optional[str] = None, provider: str = "brave"):
        self.api_key = api_key
        self.provider = provider
    
    def search(self, query: str, num_results: int = 5) -> List[Dict[str, Any]]:
        """
        Execute web search
        
        Note: This is a template. Replace with actual API integration.
        """
        if self.provider == "brave" and self.api_key:
            return self._brave_search(query, num_results)
        elif self.provider == "serper" and self.api_key:
            return self._serper_search(query, num_results)
        else:
            # Fallback: return mock results for demonstration
            return self._mock_search(query, num_results)
    
    def _brave_search(self, query: str, num_results: int) -> List[Dict[str, Any]]:
        """Brave Search API integration"""
        url = "https://api.search.brave.com/res/v1/web/search"
        headers = {
            "Accept": "application/json",
            "X-Subscription-Token": self.api_key
        }
        params = {
            "q": query,
            "count": num_results
        }
        
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            
            results = []
            for item in data.get('web', {}).get('results', []):
                results.append({
                    "title": item.get("title", ""),
                    "url": item.get("url", ""),
                    "snippet": item.get("description", ""),
                    "content": item.get("description", "")
                })
            return results
        except Exception as e:
            print(f"Brave search error: {e}")
            return []
    
    def _serper_search(self, query: str, num_results: int) -> List[Dict[str, Any]]:
        """Serper API integration"""
        url = "https://google.serper.dev/search"
        headers = {
            "X-API-KEY": self.api_key,
            "Content-Type": "application/json"
        }
        payload = {
            "q": query,
            "num": num_results
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            
            results = []
            for item in data.get('organic', []):
                results.append({
                    "title": item.get("title", ""),
                    "url": item.get("link", ""),
                    "snippet": item.get("snippet", ""),
                    "content": item.get("snippet", "")
                })
            return results
        except Exception as e:
            print(f"Serper search error: {e}")
            return []
    
    def _mock_search(self, query: str, num_results: int) -> List[Dict[str, Any]]:
        """Mock search results for testing without API keys"""
        return [
            {
                "title": f"Result {i+1} for: {query}",
                "url": f"https://example.com/result-{i+1}",
                "snippet": f"This is a mock search result {i+1} for the query: {query}. "
                          f"It contains relevant information about the topic.",
                "content": f"Extended content for result {i+1}. This would normally contain "
                          f"the full text or detailed information from the source."
            }
            for i in range(num_results)
        ]


class AcademicSearchTool(SearchTool):
    """Search academic papers and research"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
    
    def search(self, query: str, num_results: int = 5) -> List[Dict[str, Any]]:
        """
        Search academic sources
        Could integrate with: Semantic Scholar, arXiv, PubMed, etc.
        """
        # Template for academic search
        return self._mock_academic_search(query, num_results)
    
    def _mock_academic_search(self, query: str, num_results: int) -> List[Dict[str, Any]]:
        """Mock academic search results"""
        return [
            {
                "title": f"Academic Paper {i+1}: {query}",
                "authors": ["Author A", "Author B"],
                "year": 2024 - i,
                "abstract": f"Abstract for paper {i+1} about {query}",
                "url": f"https://arxiv.org/abs/2024.{i+1}",
                "citations": 100 - i*10
            }
            for i in range(num_results)
        ]


class SearchOrchestrator:
    """
    Orchestrates multiple search tools and combines results
    """
    
    def __init__(self):
        self.tools: Dict[str, SearchTool] = {}
    
    def register_tool(self, name: str, tool: SearchTool):
        """Register a search tool"""
        self.tools[name] = tool
    
    def search(
        self, 
        query: str, 
        tools: Optional[List[str]] = None,
        num_results: int = 5
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        Execute search across multiple tools
        
        Args:
            query: Search query
            tools: List of tool names to use (None = use all)
            num_results: Number of results per tool
            
        Returns:
            Dictionary mapping tool name to results
        """
        if tools is None:
            tools = list(self.tools.keys())
        
        results = {}
        for tool_name in tools:
            if tool_name in self.tools:
                try:
                    results[tool_name] = self.tools[tool_name].search(query, num_results)
                except Exception as e:
                    print(f"Error searching with {tool_name}: {e}")
                    results[tool_name] = []
        
        return results
    
    def search_and_combine(
        self,
        query: str,
        tools: Optional[List[str]] = None,
        num_results: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Search and combine results from multiple tools
        """
        all_results = self.search(query, tools, num_results)
        
        # Combine and deduplicate results
        combined = []
        seen_urls = set()
        
        for tool_name, results in all_results.items():
            for result in results:
                url = result.get('url', '')
                if url and url not in seen_urls:
                    result['source_tool'] = tool_name
                    combined.append(result)
                    seen_urls.add(url)
        
        return combined
