"""
Deep Research Agentic Pipeline
A Python-based autonomous research system using OpenRouter.ai
"""

__version__ = "1.0.0"
__author__ = "Research Pipeline Team"

from .pipeline import ResearchPipeline
from .research_agent import ResearchAgent, ResearchPhase, ResearchStep
from .llm_client import OpenRouterClient
from .search_tools import SearchOrchestrator, WebSearchTool, AcademicSearchTool
from .config import Config

__all__ = [
    "ResearchPipeline",
    "ResearchAgent",
    "ResearchPhase",
    "ResearchStep",
    "OpenRouterClient",
    "SearchOrchestrator",
    "WebSearchTool",
    "AcademicSearchTool",
    "Config",
]
