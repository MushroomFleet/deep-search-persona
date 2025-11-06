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
