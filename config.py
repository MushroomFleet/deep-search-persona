"""
Configuration for the Deep Research Agentic Pipeline
"""
import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration management for the research pipeline"""
    
    # OpenRouter API Configuration
    OPENROUTER_API_KEY: str = os.getenv("OPENROUTER_API_KEY", "")
    OPENROUTER_BASE_URL: str = "https://openrouter.ai/api/v1"
    
    # Default Model Configuration
    DEFAULT_MODEL: str = "x-ai/grok-4-fast:online"  # Grok model
    MODEL_TEMPERATURE: float = 0.7
    MAX_TOKENS: int = 4000
    
    # Research Pipeline Configuration
    MAX_RESEARCH_ITERATIONS: int = 10
    MAX_SEARCH_QUERIES: int = 5
    SEARCH_RESULTS_PER_QUERY: int = 5
    
    # Agent Configuration
    AGENT_THINKING_BUDGET: int = 2000  # tokens for reasoning
    MIN_CONFIDENCE_THRESHOLD: float = 0.7
    
    # Output Configuration
    OUTPUT_DIR: str = "./research_outputs"
    SAVE_INTERMEDIATE_RESULTS: bool = True
    
    # Embedding Configuration (Phase 3)
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    EMBEDDING_PROVIDER: str = os.getenv("EMBEDDING_PROVIDER", "openai")
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
    EMBEDDING_DIMENSIONS: int = int(os.getenv("EMBEDDING_DIMENSIONS", "1536"))
    EMBEDDING_CACHE_ENABLED: bool = os.getenv("EMBEDDING_CACHE_ENABLED", "true").lower() == "true"
    EMBEDDING_MAX_CACHE_SIZE: int = int(os.getenv("EMBEDDING_MAX_CACHE_SIZE", "10000"))
    
    @classmethod
    def validate(cls) -> bool:
        """Validate that required configuration is present"""
        if not cls.OPENROUTER_API_KEY:
            raise ValueError("OPENROUTER_API_KEY environment variable must be set")
        return True
    
    @classmethod
    def get_model_config(cls, model: Optional[str] = None) -> dict:
        """Get configuration for API calls"""
        return {
            "model": model or cls.DEFAULT_MODEL,
            "temperature": cls.MODEL_TEMPERATURE,
            "max_tokens": cls.MAX_TOKENS,
        }
