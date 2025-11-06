"""
Advanced fact-checking and validation system
"""
from typing import Dict, Any, List, Tuple
from dataclasses import dataclass
from enum import Enum


class ValidationLevel(Enum):
    """Validation confidence levels"""
    HIGH = "high"  # Multiple reliable sources agree
    MEDIUM = "medium"  # Some sources agree
    LOW = "low"  # Single source or conflicting info
    FAILED = "failed"  # Contradictory or false


@dataclass
class ValidationResult:
    """Result of fact validation"""
    claim: str
    level: ValidationLevel
    confidence: float
    supporting_sources: List[str]
    contradicting_sources: List[str]
    explanation: str


class FactChecker:
    """
    Validates claims by cross-referencing multiple sources
    """
    
    def __init__(self, llm_client):
        self.llm = llm_client
        self.validation_cache = {}
    
    def validate_finding(self, finding: str, sources: List[Dict[str, Any]]) -> ValidationResult:
        """
        Validate a single finding against sources
        
        Uses LLM to:
        1. Identify key claims in the finding
        2. Cross-reference against sources
        3. Detect contradictions
        4. Assess overall reliability
        """
        
        # Check cache
        cache_key = self._get_cache_key(finding)
        if cache_key in self.validation_cache:
            return self.validation_cache[cache_key]
        
        # Format sources
        sources_text = self._format_sources(sources)
        
        validation_prompt = f"""<task>
Validate this research finding by cross-referencing the provided sources.
</task>

<finding>
{finding}
</finding>

<sources>
{sources_text}
</sources>

<validation_steps>
1. Identify key factual claims in the finding
2. For each claim, check which sources support or contradict it
3. Assess source reliability (academic > news > blog)
4. Calculate confidence based on agreement and source quality
5. Flag any contradictions or inconsistencies
</validation_steps>

<output_format>
Return ONLY valid JSON:
{{
  "validation_level": "high|medium|low|failed",
  "confidence": 0.X,
  "supporting_sources": ["source 1", "source 2"],
  "contradicting_sources": ["source X"],
  "explanation": "detailed reasoning",
  "key_claims_status": [
    {{"claim": "...", "verified": true/false, "sources": [...]}}
  ]
}}
</output_format>"""
        
        response = self.llm.generate_with_system_prompt(
            "You are a fact-checking expert validating research findings.",
            validation_prompt,
            temperature=0.2  # Low temperature for consistency
        )
        
        # Parse response
        try:
            from research_agent import ResearchAgent
            result_data = ResearchAgent._robust_json_extract(response)
            
            result = ValidationResult(
                claim=finding,
                level=ValidationLevel(result_data.get("validation_level", "low")),
                confidence=result_data.get("confidence", 0.5),
                supporting_sources=result_data.get("supporting_sources", []),
                contradicting_sources=result_data.get("contradicting_sources", []),
                explanation=result_data.get("explanation", "")
            )
            
            # Cache result
            self.validation_cache[cache_key] = result
            
            return result
            
        except Exception as e:
            return ValidationResult(
                claim=finding,
                level=ValidationLevel.LOW,
                confidence=0.3,
                supporting_sources=[],
                contradicting_sources=[],
                explanation=f"Validation error: {str(e)}"
            )
    
    def validate_all_findings(self, findings: List[str], sources: List[Dict[str, Any]]) -> List[ValidationResult]:
        """Validate multiple findings"""
        return [self.validate_finding(f, sources) for f in findings]
    
    def get_reliability_score(self, validations: List[ValidationResult]) -> float:
        """Calculate overall reliability of research"""
        if not validations:
            return 0.0
        
        # Weighted average based on validation levels
        weights = {
            ValidationLevel.HIGH: 1.0,
            ValidationLevel.MEDIUM: 0.7,
            ValidationLevel.LOW: 0.4,
            ValidationLevel.FAILED: 0.0
        }
        
        total_weight = sum(weights[v.level] * v.confidence for v in validations)
        return total_weight / len(validations)
    
    def _format_sources(self, sources: List[Dict[str, Any]]) -> str:
        """Format sources for validation"""
        formatted = []
        for i, source in enumerate(sources, 1):
            formatted.append(
                f"Source {i}:\n"
                f"Title: {source.get('title', 'Unknown')}\n"
                f"Content: {source.get('content', source.get('snippet', 'N/A'))}\n"
                f"Type: {source.get('type', 'web')}\n"
            )
        return "\n".join(formatted)
    
    def _get_cache_key(self, finding: str) -> str:
        """Generate cache key for finding"""
        # Simple hash - could use better hashing
        return f"val_{hash(finding) % 100000}"
