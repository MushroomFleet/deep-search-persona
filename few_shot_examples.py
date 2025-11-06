"""
Few-shot examples for improved prompt performance
"""
import json
from typing import List, Dict, Any


class FewShotExamples:
    """Storage for high-quality few-shot examples"""
    
    RESEARCH_PLANNING = [
        {
            "input": "What is quantum computing?",
            "output": [
                {
                    "step": 1,
                    "query": "quantum computing fundamentals principles",
                    "reasoning": "Establish foundational understanding of core concepts",
                    "expected_info": "Basic principles, key components, how it differs from classical computing",
                    "validation_criteria": "Clear explanation of qubits, superposition, entanglement",
                    "confidence_threshold": 0.7
                },
                {
                    "step": 2,
                    "query": "quantum computing applications use cases 2024",
                    "reasoning": "Understand practical applications and current state",
                    "expected_info": "Real-world applications, industries using it, success stories",
                    "validation_criteria": "Specific examples with evidence of deployment",
                    "confidence_threshold": 0.7
                },
                {
                    "step": 3,
                    "query": "quantum computing challenges limitations",
                    "reasoning": "Balanced view including difficulties and constraints",
                    "expected_info": "Technical challenges, scalability issues, error rates",
                    "validation_criteria": "Concrete technical details from credible sources",
                    "confidence_threshold": 0.7
                }
            ]
        },
        {
            "input": "Latest developments in AI safety",
            "output": [
                {
                    "step": 1,
                    "query": "AI safety research 2024 recent breakthroughs",
                    "reasoning": "Get most current developments in the field",
                    "expected_info": "Recent papers, breakthroughs, new techniques",
                    "validation_criteria": "Dated sources from 2024, academic citations",
                    "confidence_threshold": 0.8
                },
                {
                    "step": 2,
                    "query": "AI alignment problem current approaches",
                    "reasoning": "Core technical challenge in AI safety",
                    "expected_info": "Technical approaches, methodologies, progress",
                    "validation_criteria": "Detailed technical explanations",
                    "confidence_threshold": 0.7
                },
                {
                    "step": 3,
                    "query": "AI safety regulations policy 2024",
                    "reasoning": "Understand governance and policy landscape",
                    "expected_info": "Government policies, industry standards, regulations",
                    "validation_criteria": "Official sources, policy documents",
                    "confidence_threshold": 0.7
                }
            ]
        },
        {
            "input": "How does photosynthesis work?",
            "output": [
                {
                    "step": 1,
                    "query": "photosynthesis process steps light reactions",
                    "reasoning": "Understand the fundamental biochemical process",
                    "expected_info": "Step-by-step process, light and dark reactions, chemical equations",
                    "validation_criteria": "Clear explanation of light and Calvin cycle",
                    "confidence_threshold": 0.7
                },
                {
                    "step": 2,
                    "query": "chloroplast structure function photosynthesis",
                    "reasoning": "Understand where and how the process occurs",
                    "expected_info": "Organelle structure, thylakoids, stroma, pigments",
                    "validation_criteria": "Detailed structural information with diagrams",
                    "confidence_threshold": 0.7
                },
                {
                    "step": 3,
                    "query": "photosynthesis efficiency factors environmental",
                    "reasoning": "Understand what affects the process and its limitations",
                    "expected_info": "Environmental factors, efficiency rates, limiting factors",
                    "validation_criteria": "Quantitative data on efficiency and factors",
                    "confidence_threshold": 0.7
                }
            ]
        }
    ]
    
    RESULT_ANALYSIS = [
        {
            "input": "Search query: quantum computing fundamentals",
            "results": "5 results about quantum mechanics, qubits, and superposition",
            "output": {
                "key_findings": [
                    {
                        "finding": "Quantum computers use qubits that can exist in superposition states",
                        "source": "Result #1",
                        "confidence": 0.9
                    },
                    {
                        "finding": "Quantum entanglement enables faster computation for specific problems",
                        "source": "Result #2",
                        "confidence": 0.85
                    },
                    {
                        "finding": "Current quantum computers have ~100-1000 qubits with high error rates",
                        "source": "Result #3",
                        "confidence": 0.8
                    }
                ],
                "confidence": 0.85,
                "source_quality": {"academic": 3, "news": 1, "other": 1},
                "gaps": ["Specific algorithms and complexity classes", "Cost and accessibility"],
                "contradictions": ["Varying estimates on timeline to quantum advantage"],
                "summary": "Quantum computing leverages quantum mechanical properties like superposition and entanglement to perform computations differently from classical computers, with current systems still in early stages.",
                "recommended_next_queries": ["quantum algorithms applications", "quantum computing timeline predictions"]
            }
        }
    ]
    
    DECISION_MAKING = [
        {
            "input": {
                "query": "What is quantum computing?",
                "steps_completed": 2,
                "confidence_trend": [0.75, 0.8],
                "gaps": ["Practical applications", "Current limitations"]
            },
            "output": {
                "action": "search",
                "reasoning": "Good foundational understanding established (confidence 0.8), but identified gaps in practical applications and limitations. Need one more search to provide complete answer.",
                "confidence": 0.8,
                "next_query": "quantum computing applications challenges 2024",
                "priority": "high"
            }
        },
        {
            "input": {
                "query": "Climate change impacts",
                "steps_completed": 5,
                "confidence_trend": [0.7, 0.75, 0.85, 0.85, 0.9],
                "gaps": []
            },
            "output": {
                "action": "synthesize",
                "reasoning": "Comprehensive information gathered across 5 steps with increasing confidence trend reaching 0.9. No significant gaps identified. Ready to compile findings into coherent answer.",
                "confidence": 0.9,
                "next_query": None,
                "priority": "high"
            }
        }
    ]
    
    @classmethod
    def get_examples(cls, task_type: str, n: int = 2) -> str:
        """
        Get formatted examples for a task type
        
        Args:
            task_type: Type of task (research_planning, result_analysis, decision_making)
            n: Number of examples to return
            
        Returns:
            Formatted string of examples
        """
        examples_map = {
            "research_planning": cls.RESEARCH_PLANNING,
            "result_analysis": cls.RESULT_ANALYSIS,
            "decision_making": cls.DECISION_MAKING,
        }
        
        examples = examples_map.get(task_type, [])[:n]
        
        if not examples:
            return "No examples available for this task type."
        
        # Format as text
        formatted = []
        for ex in examples:
            if task_type == "research_planning":
                formatted.append(f"Input: {ex['input']}\nOutput: {json.dumps(ex['output'], indent=2)}")
            elif task_type == "result_analysis":
                formatted.append(
                    f"Input Query: {ex['input']}\n"
                    f"Results: {ex['results']}\n"
                    f"Output: {json.dumps(ex['output'], indent=2)}"
                )
            elif task_type == "decision_making":
                formatted.append(
                    f"Input State: {json.dumps(ex['input'], indent=2)}\n"
                    f"Output Decision: {json.dumps(ex['output'], indent=2)}"
                )
        
        return "\n\n---\n\n".join(formatted)
    
    @classmethod
    def get_available_types(cls) -> List[str]:
        """Get list of available example types"""
        return ["research_planning", "result_analysis", "decision_making"]
    
    @classmethod
    def add_example(cls, task_type: str, example: Dict[str, Any]) -> bool:
        """
        Add a new example to the library (for future expansion)
        
        Args:
            task_type: Type of task
            example: Example dictionary
            
        Returns:
            True if added successfully
        """
        # This could be expanded to persist examples to a file
        # For now, it just validates the structure
        required_keys = {
            "research_planning": ["input", "output"],
            "result_analysis": ["input", "results", "output"],
            "decision_making": ["input", "output"]
        }
        
        if task_type not in required_keys:
            return False
        
        if not all(key in example for key in required_keys[task_type]):
            return False
        
        return True
