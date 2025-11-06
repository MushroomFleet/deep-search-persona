# Phase 3: Advanced Features Implementation Guide

**Timeline:** Week 5-6  
**Expected Impact:** 80%+ improvement in research comprehensiveness  
**Difficulty:** High  
**Priority:** 🟡 MEDIUM

---

## Overview

Phase 3 builds on the solid foundation from Phases 1 and 2 to add sophisticated features that maximize research quality, reliability, and adaptability. This phase focuses on dynamic workflow management, advanced validation systems, semantic memory, and continuous improvement through A/B testing.

---

## 1. Dynamic Workflow Management

### Current Problem
- Rigid phase-based workflow (Planning → Research → Synthesis)
- No ability to backtrack or branch
- Cannot adapt to unexpected findings
- Poor handling of edge cases

### Solution: State Machine with Dynamic Transitions

#### Create `workflow/state_machine.py`:

```python
"""
Dynamic workflow state machine for adaptive research
"""
from enum import Enum
from typing import Dict, Any, List, Callable, Optional
from dataclasses import dataclass
from datetime import datetime


class WorkflowState(Enum):
    """All possible workflow states"""
    PLANNING = "planning"
    SEARCHING = "searching"
    ANALYZING = "analyzing"
    VALIDATING = "validating"
    REFINING = "refining"
    SYNTHESIZING = "synthesizing"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class StateTransition:
    """Represents a state transition"""
    from_state: WorkflowState
    to_state: WorkflowState
    condition: str
    timestamp: datetime = None
    reason: str = ""
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()


class ResearchStateMachine:
    """
    Dynamic state machine that adapts workflow based on context
    """
    
    def __init__(self):
        self.current_state = WorkflowState.PLANNING
        self.state_history = []
        self.transition_rules = self._init_transition_rules()
        self.context = {}
    
    def _init_transition_rules(self) -> Dict[str, Callable]:
        """
        Define rules for state transitions
        
        Rules are condition functions that take context and return next state
        """
        return {
            "default_planning": lambda ctx: WorkflowState.SEARCHING,
            "default_searching": lambda ctx: WorkflowState.ANALYZING,
            "default_analyzing": lambda ctx: WorkflowState.SYNTHESIZING,
            
            # Adaptive rules
            "low_confidence_analyzing": lambda ctx: (
                WorkflowState.SEARCHING if ctx.get("confidence", 1.0) < 0.6
                else WorkflowState.SYNTHESIZING
            ),
            
            "contradictions_found": lambda ctx: (
                WorkflowState.VALIDATING if ctx.get("contradictions", 0) > 2
                else WorkflowState.ANALYZING
            ),
            
            "validation_failed": lambda ctx: (
                WorkflowState.REFINING if ctx.get("validation_passed", True) == False
                else WorkflowState.SYNTHESIZING
            ),
            
            "stuck_in_loop": lambda ctx: (
                WorkflowState.REFINING if ctx.get("iterations_without_progress", 0) > 2
                else WorkflowState.SEARCHING
            ),
            
            "high_quality_complete": lambda ctx: (
                WorkflowState.COMPLETED if (
                    ctx.get("confidence", 0) > 0.8 and
                    ctx.get("coverage", 0) > 0.7 and
                    ctx.get("contradictions", 99) == 0
                ) else WorkflowState.ANALYZING
            )
        }
    
    def next_state(self, context: Dict[str, Any]) -> WorkflowState:
        """
        Determine next state based on current state and context
        
        Uses intelligent rule selection to adapt workflow
        """
        self.context = context
        current = self.current_state
        
        # Check for special conditions first
        if self._should_validate(context):
            return self._transition_to(WorkflowState.VALIDATING, "contradictions_detected")
        
        if self._is_stuck(context):
            return self._transition_to(WorkflowState.REFINING, "stuck_in_loop")
        
        if self._can_complete(context):
            return self._transition_to(WorkflowState.COMPLETED, "objectives_met")
        
        # Default transitions based on current state
        next_state_map = {
            WorkflowState.PLANNING: self._next_from_planning,
            WorkflowState.SEARCHING: self._next_from_searching,
            WorkflowState.ANALYZING: self._next_from_analyzing,
            WorkflowState.VALIDATING: self._next_from_validating,
            WorkflowState.REFINING: self._next_from_refining,
            WorkflowState.SYNTHESIZING: self._next_from_synthesizing,
        }
        
        next_func = next_state_map.get(current)
        if next_func:
            return next_func(context)
        
        return current
    
    def _transition_to(self, new_state: WorkflowState, reason: str) -> WorkflowState:
        """Record and execute state transition"""
        transition = StateTransition(
            from_state=self.current_state,
            to_state=new_state,
            condition=reason,
            reason=reason
        )
        
        self.state_history.append(transition)
        self.current_state = new_state
        
        return new_state
    
    def _should_validate(self, ctx: Dict[str, Any]) -> bool:
        """Check if validation is needed"""
        return ctx.get("contradictions", 0) > 2 or ctx.get("confidence", 1.0) < 0.5
    
    def _is_stuck(self, ctx: Dict[str, Any]) -> bool:
        """Detect if research is stuck in a loop"""
        return ctx.get("iterations_without_progress", 0) > 2
    
    def _can_complete(self, ctx: Dict[str, Any]) -> bool:
        """Check if research objectives are met"""
        return (
            ctx.get("confidence", 0) > 0.8 and
            ctx.get("coverage", 0) > 0.75 and
            ctx.get("contradictions", 99) == 0 and
            self.current_state == WorkflowState.SYNTHESIZING
        )
    
    def _next_from_planning(self, ctx: Dict[str, Any]) -> WorkflowState:
        """Determine next state from PLANNING"""
        return self._transition_to(WorkflowState.SEARCHING, "plan_complete")
    
    def _next_from_searching(self, ctx: Dict[str, Any]) -> WorkflowState:
        """Determine next state from SEARCHING"""
        if ctx.get("results_found", 0) == 0:
            return self._transition_to(WorkflowState.REFINING, "no_results")
        return self._transition_to(WorkflowState.ANALYZING, "results_found")
    
    def _next_from_analyzing(self, ctx: Dict[str, Any]) -> WorkflowState:
        """Determine next state from ANALYZING"""
        confidence = ctx.get("confidence", 0.5)
        
        if confidence < 0.6:
            return self._transition_to(WorkflowState.SEARCHING, "low_confidence")
        elif ctx.get("contradictions", 0) > 2:
            return self._transition_to(WorkflowState.VALIDATING, "contradictions_found")
        elif ctx.get("coverage", 0) > 0.7:
            return self._transition_to(WorkflowState.SYNTHESIZING, "sufficient_coverage")
        else:
            return self._transition_to(WorkflowState.SEARCHING, "coverage_incomplete")
    
    def _next_from_validating(self, ctx: Dict[str, Any]) -> WorkflowState:
        """Determine next state from VALIDATING"""
        if ctx.get("validation_passed", False):
            return self._transition_to(WorkflowState.SYNTHESIZING, "validation_passed")
        else:
            return self._transition_to(WorkflowState.REFINING, "validation_failed")
    
    def _next_from_refining(self, ctx: Dict[str, Any]) -> WorkflowState:
        """Determine next state from REFINING"""
        return self._transition_to(WorkflowState.SEARCHING, "strategy_refined")
    
    def _next_from_synthesizing(self, ctx: Dict[str, Any]) -> WorkflowState:
        """Determine next state from SYNTHESIZING"""
        quality = ctx.get("synthesis_quality", 0.5)
        
        if quality > 0.8:
            return self._transition_to(WorkflowState.COMPLETED, "high_quality_synthesis")
        else:
            return self._transition_to(WorkflowState.ANALYZING, "synthesis_needs_improvement")
    
    def get_state_path(self) -> List[str]:
        """Get the path of states traversed"""
        return [self.current_state.value] + [
            t.to_state.value for t in self.state_history
        ]
    
    def can_backtrack(self) -> bool:
        """Check if we can go back to a previous state"""
        return len(self.state_history) > 0
    
    def backtrack(self, steps: int = 1) -> WorkflowState:
        """Go back to a previous state"""
        if not self.can_backtrack() or steps > len(self.state_history):
            return self.current_state
        
        # Remove recent transitions
        for _ in range(steps):
            self.state_history.pop()
        
        # Restore previous state
        if self.state_history:
            self.current_state = self.state_history[-1].to_state
        else:
            self.current_state = WorkflowState.PLANNING
        
        return self.current_state
```

---

## 2. Advanced Validation System

### Create `validation/fact_checker.py`:

```python
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
```

---

## 3. Semantic Memory with Vector Search

### Create `memory/semantic_memory.py`:

```python
"""
Semantic memory using embeddings for similarity search
Future: Integrate with vector databases (Pinecone, Weaviate, ChromaDB)
"""
from typing import List, Dict, Any, Tuple
import numpy as np
from dataclasses import dataclass


@dataclass
class SemanticItem:
    """Item stored in semantic memory"""
    id: str
    content: str
    embedding: np.ndarray
    metadata: Dict[str, Any]
    timestamp: float


class SemanticMemory:
    """
    Semantic memory using vector embeddings for similarity search
    
    Note: This is a simplified implementation. 
    For production, use vector databases like:
    - Pinecone
    - Weaviate
    - ChromaDB
    - FAISS
    """
    
    def __init__(self, llm_client):
        self.llm = llm_client
        self.items = []  # List of SemanticItems
        self.embeddings_cache = {}
    
    def store(self, content: str, metadata: Dict[str, Any] = None) -> str:
        """Store content with semantic embedding"""
        import time
        
        # Generate embedding
        embedding = self._get_embedding(content)
        
        # Create item
        item_id = f"sem_{int(time.time() * 1000)}"
        item = SemanticItem(
            id=item_id,
            content=content,
            embedding=embedding,
            metadata=metadata or {},
            timestamp=time.time()
        )
        
        self.items.append(item)
        return item_id
    
    def search(self, query: str, top_k: int = 5, threshold: float = 0.7) -> List[Tuple[SemanticItem, float]]:
        """
        Semantic similarity search
        
        Returns items most similar to query with similarity scores
        """
        if not self.items:
            return []
        
        # Get query embedding
        query_embedding = self._get_embedding(query)
        
        # Calculate similarities
        similarities = []
        for item in self.items:
            similarity = self._cosine_similarity(query_embedding, item.embedding)
            if similarity >= threshold:
                similarities.append((item, similarity))
        
        # Sort by similarity
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        return similarities[:top_k]
    
    def find_related(self, item_id: str, top_k: int = 5) -> List[Tuple[SemanticItem, float]]:
        """Find items related to a specific item"""
        # Find item
        item = next((i for i in self.items if i.id == item_id), None)
        if not item:
            return []
        
        # Search using item content
        return self.search(item.content, top_k=top_k + 1)[1:]  # Exclude self
    
    def _get_embedding(self, text: str) -> np.ndarray:
        """
        Get embedding for text
        
        Simplified version using simple text features.
        For production, use:
        - OpenAI embeddings API
        - Sentence transformers
        - Custom embedding models
        """
        # Check cache
        if text in self.embeddings_cache:
            return self.embeddings_cache[text]
        
        # Simplified: Use word frequency as "embedding"
        # In production: Use actual embedding models
        words = text.lower().split()
        # Create a simple 100-dimensional vector
        vocab_size = 1000
        embedding = np.zeros(100)
        
        for word in words:
            idx = hash(word) % 100
            embedding[idx] += 1
        
        # Normalize
        norm = np.linalg.norm(embedding)
        if norm > 0:
            embedding = embedding / norm
        
        # Cache
        self.embeddings_cache[text] = embedding
        
        return embedding
    
    def _cosine_similarity(self, a: np.ndarray, b: np.ndarray) -> float:
        """Calculate cosine similarity between two vectors"""
        dot_product = np.dot(a, b)
        norm_a = np.linalg.norm(a)
        norm_b = np.linalg.norm(b)
        
        if norm_a == 0 or norm_b == 0:
            return 0.0
        
        return dot_product / (norm_a * norm_b)
    
    def cluster_items(self, num_clusters: int = 5) -> Dict[int, List[SemanticItem]]:
        """
        Cluster items by semantic similarity
        
        Useful for identifying themes in research
        """
        if len(self.items) < num_clusters:
            return {0: self.items}
        
        # Simple clustering using k-means-like approach
        # For production: Use scikit-learn or similar
        
        # Initialize random centroids
        import random
        centroids_items = random.sample(self.items, num_clusters)
        centroids = [item.embedding for item in centroids_items]
        
        # Assign items to clusters
        clusters = {i: [] for i in range(num_clusters)}
        
        for item in self.items:
            # Find closest centroid
            distances = [
                1 - self._cosine_similarity(item.embedding, centroid)
                for centroid in centroids
            ]
            closest = distances.index(min(distances))
            clusters[closest].append(item)
        
        return clusters
```

---

## 4. A/B Testing Framework

### Create `testing/ab_testing.py`:

```python
"""
A/B testing framework for prompt optimization
"""
from typing import Dict, Any, List, Callable
from dataclasses import dataclass
from enum import Enum
import random
import json
from datetime import datetime


class Variant(Enum):
    """A/B test variants"""
    A = "A"
    B = "B"
    CONTROL = "control"


@dataclass
class TestResult:
    """Single A/B test result"""
    variant: Variant
    metric_name: str
    metric_value: float
    timestamp: datetime
    metadata: Dict[str, Any]


class ABTest:
    """
    A/B test for comparing prompt versions or strategies
    """
    
    def __init__(self, name: str, metric: str, variants: Dict[str, Any]):
        """
        Args:
            name: Test name
            metric: Metric to optimize (e.g., 'confidence', 'accuracy')
            variants: Dict mapping variant name to configuration
        """
        self.name = name
        self.metric = metric
        self.variants = variants
        self.results = []
        self.variant_stats = {v: [] for v in variants.keys()}
    
    def get_variant(self, traffic_split: Dict[str, float] = None) -> str:
        """
        Select variant based on traffic split
        
        Args:
            traffic_split: Dict mapping variant to % traffic (e.g., {'A': 0.5, 'B': 0.5})
        """
        if traffic_split is None:
            # Equal split
            traffic_split = {v: 1.0 / len(self.variants) for v in self.variants}
        
        # Weighted random selection
        variants = list(traffic_split.keys())
        weights = list(traffic_split.values())
        
        return random.choices(variants, weights=weights)[0]
    
    def record_result(self, variant: str, metric_value: float, metadata: Dict[str, Any] = None):
        """Record test result for a variant"""
        result = TestResult(
            variant=Variant(variant) if variant in ['A', 'B'] else Variant.CONTROL,
            metric_name=self.metric,
            metric_value=metric_value,
            timestamp=datetime.now(),
            metadata=metadata or {}
        )
        
        self.results.append(result)
        self.variant_stats[variant].append(metric_value)
    
    def get_winner(self, min_samples: int = 30) -> Dict[str, Any]:
        """
        Determine winning variant
        
        Returns variant with best average metric
        """
        if len(self.results) < min_samples:
            return {
                "winner": None,
                "reason": f"Insufficient data (need {min_samples} samples, have {len(self.results)})"
            }
        
        # Calculate statistics
        stats = {}
        for variant, values in self.variant_stats.items():
            if not values:
                continue
            
            stats[variant] = {
                "mean": sum(values) / len(values),
                "count": len(values),
                "std": self._std(values)
            }
        
        # Find best variant
        best_variant = max(stats.items(), key=lambda x: x[1]["mean"])
        
        return {
            "winner": best_variant[0],
            "mean": best_variant[1]["mean"],
            "confidence": self._calculate_confidence(best_variant[0], stats),
            "all_stats": stats
        }
    
    def _std(self, values: List[float]) -> float:
        """Calculate standard deviation"""
        if len(values) < 2:
            return 0.0
        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / (len(values) - 1)
        return variance ** 0.5
    
    def _calculate_confidence(self, winner: str, stats: Dict) -> float:
        """Calculate confidence in winner (simplified)"""
        winner_mean = stats[winner]["mean"]
        
        # Compare to other variants
        margins = []
        for variant, variant_stats in stats.items():
            if variant != winner:
                margin = (winner_mean - variant_stats["mean"]) / max(winner_mean, 0.01)
                margins.append(margin)
        
        if not margins:
            return 0.5
        
        avg_margin = sum(margins) / len(margins)
        return min(0.95, 0.5 + avg_margin)
    
    def export_results(self, filepath: str):
        """Export test results to JSON"""
        export_data = {
            "test_name": self.name,
            "metric": self.metric,
            "results": [
                {
                    "variant": r.variant.value,
                    "value": r.metric_value,
                    "timestamp": r.timestamp.isoformat()
                }
                for r in self.results
            ],
            "winner": self.get_winner()
        }
        
        with open(filepath, 'w') as f:
            json.dump(export_data, f, indent=2)


class ABTestManager:
    """Manages multiple A/B tests"""
    
    def __init__(self):
        self.active_tests = {}
    
    def create_test(self, name: str, metric: str, variants: Dict[str, Any]) -> ABTest:
        """Create and register new A/B test"""
        test = ABTest(name, metric, variants)
        self.active_tests[name] = test
        return test
    
    def get_test(self, name: str) -> ABTest:
        """Get active test by name"""
        return self.active_tests.get(name)
    
    def list_tests(self) -> List[str]:
        """List all active tests"""
        return list(self.active_tests.keys())
```

---

## Integration Example

### Using All Advanced Features Together:

```python
"""
Example: Using advanced features in pipeline
"""
from workflow.state_machine import ResearchStateMachine, WorkflowState
from validation.fact_checker import FactChecker
from memory.semantic_memory import SemanticMemory
from testing.ab_testing import ABTestManager


class AdvancedResearchPipeline(ResearchPipeline):
    """
    Enhanced pipeline with Phase 3 features
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Initialize advanced features
        self.state_machine = ResearchStateMachine()
        self.fact_checker = FactChecker(self.llm)
        self.semantic_memory = SemanticMemory(self.llm)
        self.ab_tests = ABTestManager()
        
        # Create A/B test for prompt variations
        self.ab_tests.create_test(
            name="research_planner_prompt",
            metric="plan_quality",
            variants={"A": "v1", "B": "v2"}
        )
    
    def execute(self, query: str) -> Dict[str, Any]:
        """Execute with dynamic workflow"""
        
        # Dynamic workflow instead of rigid phases
        while self.state_machine.current_state != WorkflowState.COMPLETED:
            current_state = self.state_machine.current_state
            
            # Execute state-specific logic
            if current_state == WorkflowState.PLANNING:
                self._adaptive_planning()
            elif current_state == WorkflowState.SEARCHING:
                self._adaptive_searching()
            elif current_state == WorkflowState.ANALYZING:
                self._adaptive_analyzing()
            elif current_state == WorkflowState.VALIDATING:
                self._adaptive_validating()
            elif current_state == WorkflowState.SYNTHESIZING:
                self._adaptive_synthesizing()
            
            # Determine next state
            context = self._build_context()
            next_state = self.state_machine.next_state(context)
            
            print(f"State: {current_state.value} → {next_state.value}")
        
        return self._save_results()
    
    def _build_context(self) -> Dict[str, Any]:
        """Build context for state machine"""
        return {
            "confidence": self._calculate_confidence(),
            "coverage": self._calculate_coverage(),
            "contradictions": self._count_contradictions(),
            "iterations_without_progress": self._check_progress(),
            "validation_passed": getattr(self, 'last_validation_passed', True)
        }
```

---

## Success Criteria

✅ **Phase 3 Complete When:**
1. Dynamic workflow adapts to research quality
2. Fact validation achieves >90% accuracy
3. Semantic search retrieves relevant findings
4. A/B tests identify best prompt variants
5. End-to-end tests with all features passing

---

## Expected Outcomes

- **Adaptability:** Workflow responds to quality signals
- **Reliability:** Validated facts with confidence scores
- **Intelligence:** Semantic search finds relevant context
- **Optimization:** Continuous improvement via A/B testing
- **Quality:** 80%+ improvement in research comprehensiveness

---

## Next Steps

After Phase 3 completion:
→ Review **Implementation Roadmap** (`IMPLEMENTATION_ROADMAP.md`)
→ Begin production deployment
→ Monitor metrics and iterate
