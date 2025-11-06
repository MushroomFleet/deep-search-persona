# Phase 1: Quick Wins Implementation Guide

**Timeline:** Week 1-2  
**Expected Impact:** 40-60% improvement in response quality  
**Difficulty:** Low-Medium  
**Priority:** 🔥 HIGH

---

## Overview

Phase 1 focuses on immediately actionable improvements that require minimal architectural changes but deliver significant quality improvements. These are "quick wins" that lay the foundation for more advanced features in later phases.

---

## 1. Structured Prompt Templates

### Current Problem
- Prompts are hardcoded strings scattered across `research_agent.py`
- No version control or A/B testing capability
- Difficult to iterate and improve
- No standardized structure

### Solution: Prompt Library System

#### Step 1: Create `prompt_library.py`

```python
"""
Centralized prompt library with versioned templates
"""
from typing import Dict, Any, List
from dataclasses import dataclass
from enum import Enum


class PromptVersion(Enum):
    """Track prompt versions for A/B testing"""
    V1 = "v1"
    V2 = "v2"
    LATEST = "v2"


@dataclass
class PromptTemplate:
    """Structured prompt with metadata"""
    name: str
    version: PromptVersion
    template: str
    variables: List[str]
    description: str
    success_rate: float = 0.0  # Track performance
    
    def format(self, **kwargs) -> str:
        """Format template with variables"""
        return self.template.format(**kwargs)


class PromptLibrary:
    """Centralized storage for all prompts"""
    
    # Research Planning Prompts
    RESEARCH_PLANNER_V2 = PromptTemplate(
        name="research_planner",
        version=PromptVersion.V2,
        description="Creates structured research plans with validation",
        variables=["query", "domain", "depth_level", "few_shot_examples"],
        template="""<role>
You are Dr. ResearchBot, an expert research planner with PhD-level expertise in information science and systematic review methodology.
</role>

<task>
Create a comprehensive, structured research plan for the following query.
</task>

<context>
Query: {query}
Domain: {domain}
Research Depth: {depth_level}
</context>

<instructions>
1. **Decompose** the query into 3-5 atomic, focused sub-questions
2. **Order** them by logical dependency (foundational concepts → specific details)
3. **For each sub-question**, provide:
   - Precise search query (optimized for web/academic search)
   - Expected information type (facts, analysis, examples, etc.)
   - Validation criteria (how to verify answer quality)
   - Confidence threshold (minimum acceptable confidence: 0.7)

4. **Ensure coverage**:
   - Different perspectives (technical, practical, theoretical)
   - Current state and recent developments
   - Gaps or limitations in existing knowledge
</instructions>

<output_format>
Return ONLY valid JSON array (no markdown, no explanations):
[
  {{
    "step": 1,
    "query": "specific search query here",
    "reasoning": "why this step is foundational",
    "expected_info": "type of information needed",
    "validation_criteria": "how to verify quality",
    "confidence_threshold": 0.7
  }},
  ...
]
</output_format>

<examples>
{few_shot_examples}
</examples>

<constraints>
- Maximum 5 steps for focus
- Each query must be independently searchable
- No duplicate or overlapping queries
- Clear success criteria for each step
</constraints>"""
    )
    
    # Decision Making Prompts
    DECISION_MAKER_V2 = PromptTemplate(
        name="decision_maker",
        version=PromptVersion.V2,
        description="Agent decides next action with chain-of-thought",
        variables=["original_query", "steps_completed", "current_phase", 
                   "last_findings", "remaining_questions", "confidence_trend"],
        template="""<role>
You are an autonomous research agent making strategic decisions about investigation progress.
</role>

<current_state>
Original Query: {original_query}
Research Steps Completed: {steps_completed}
Current Phase: {current_phase}
Average Confidence Trend: {confidence_trend}
</current_state>

<recent_findings>
{last_findings}
</recent_findings>

<remaining_questions>
{remaining_questions}
</remaining_questions>

<thinking>
Analyze the current research state step-by-step:

Step 1: **Coverage Assessment**
- What aspects of the query have been adequately covered?
- What critical gaps remain?
- Are there contradictions that need resolution?

Step 2: **Quality Evaluation**
- Is the confidence level acceptable (>0.7)?
- Are findings from reliable sources?
- Do we have enough depth of information?

Step 3: **Efficiency Check**
- Are we making progress or circling?
- Is current search strategy effective?
- Should we pivot to different sources or queries?

Step 4: **Next Action Decision**
Based on the above analysis, determine the optimal next action.
</thinking>

<available_actions>
- **search**: Execute a new search query for missing information
- **analyze**: Deep dive into existing results for patterns/insights
- **refine**: Adjust search strategy or query formulation
- **validate**: Cross-check facts and verify contradictions
- **synthesize**: Sufficient information gathered, ready to compile
- **complete**: Research objectives fully met
</available_actions>

<output_format>
Return ONLY valid JSON (no markdown):
{{
  "action": "one of the available actions",
  "reasoning": "detailed explanation of why this action is optimal",
  "confidence": 0.X,
  "next_query": "specific query if action is search/refine (otherwise null)",
  "priority": "high|medium|low"
}}
</output_format>

<decision_criteria>
- If confidence < 0.6 → search for more information
- If contradictions found → validate or refine
- If gaps identified → search targeted queries
- If confidence > 0.8 and comprehensive → synthesize or complete
- If stuck (no progress in 2 steps) → refine strategy
</decision_criteria>"""
    )
    
    # Analysis Prompts
    RESULT_ANALYZER_V2 = PromptTemplate(
        name="result_analyzer",
        version=PromptVersion.V2,
        description="Deep analysis of search results with structured extraction",
        variables=["query", "results_text", "result_count"],
        template="""<role>
You are a research analyst expert at extracting key insights from search results.
</role>

<task>
Analyze search results and extract structured, actionable insights.
</task>

<context>
Search Query: {query}
Number of Results: {result_count}
</context>

<search_results>
{results_text}
</search_results>

<analysis_framework>
1. **Key Findings** (3-7 main points)
   - Extract the most important facts, insights, or discoveries
   - Each finding should be specific and evidence-based
   - Cite which result number supports each finding

2. **Information Quality Assessment**
   - Source credibility (academic, news, blog, etc.)
   - Recency of information
   - Consistency across sources
   - Overall confidence level (0-1)

3. **Knowledge Gaps**
   - What questions remain unanswered?
   - What aspects need deeper investigation?
   - Are there missing perspectives?

4. **Contradictions & Uncertainties**
   - Conflicting information between sources
   - Areas of debate or disagreement
   - Claims lacking strong evidence

5. **Actionable Next Steps**
   - Specific follow-up queries needed
   - Alternative search angles to consider
</analysis_framework>

<output_format>
Return ONLY valid JSON:
{{
  "key_findings": [
    {{"finding": "...", "source": "Result #X", "confidence": 0.X}}
  ],
  "confidence": 0.X,
  "source_quality": {{"academic": X, "news": X, "other": X}},
  "gaps": ["gap 1", "gap 2"],
  "contradictions": ["contradiction 1"],
  "summary": "2-3 sentence synthesis",
  "recommended_next_queries": ["query 1", "query 2"]
}}
</output_format>

<quality_standards>
- Findings must be factual, not speculative
- Confidence scores must be justified by evidence
- Gaps should be specific, not generic
- Summary should directly address the search query
</quality_standards>"""
    )
    
    # Synthesis Prompts  
    SYNTHESIZER_V2 = PromptTemplate(
        name="synthesizer",
        version=PromptVersion.V2,
        description="Comprehensive synthesis of all research findings",
        variables=["original_query", "research_summary", "total_steps"],
        template="""<role>
You are an expert research synthesizer creating comprehensive, well-structured reports.
</role>

<task>
Synthesize ALL research findings into a cohesive, authoritative answer to the original query.
</task>

<original_query>
{original_query}
</original_query>

<research_conducted>
Total Research Steps: {total_steps}

{research_summary}
</research_conducted>

<synthesis_requirements>
1. **Direct Answer**
   - Start with a clear, direct answer to the query
   - 2-3 sentences that capture the essence

2. **Comprehensive Analysis**
   - Integrate findings from all research steps
   - Organize thematically, not chronologically
   - Use evidence from multiple sources
   - Include relevant examples and data

3. **Structure**
   - Introduction (context and scope)
   - Main findings (organized by theme)
   - Analysis and implications
   - Limitations and uncertainties
   - Conclusion

4. **Quality Standards**
   - Academic rigor with clear citations
   - Balanced perspective (multiple viewpoints)
   - Evidence-based claims
   - Acknowledgment of gaps or limitations
   - Practical relevance where applicable

5. **Clarity**
   - Clear, professional language
   - Well-organized with headers
   - Logical flow of ideas
   - Concrete examples
</synthesis_requirements>

<output_format>
Generate a comprehensive markdown report with the following structure:

# [Topic]

## Executive Summary
[2-3 paragraphs directly answering the query]

## Background & Context
[Relevant background information]

## Key Findings
### [Theme 1]
[Findings with evidence]

### [Theme 2]
[Findings with evidence]

### [Theme 3]
[Findings with evidence]

## Analysis & Implications
[Deeper analysis and real-world implications]

## Limitations & Uncertainties
[Acknowledged gaps, contradictions, areas needing more research]

## Conclusion
[Summary and final thoughts]

## References
[Key sources cited]
</output_format>

<quality_checklist>
- [ ] Directly addresses original query
- [ ] Integrates findings from all research steps
- [ ] Well-structured and organized
- [ ] Evidence-based with specific examples
- [ ] Acknowledges limitations
- [ ] Professional and clear language
- [ ] Provides actionable insights
</quality_checklist>"""
    )
    
    @classmethod
    def get_prompt(cls, name: str, version: PromptVersion = PromptVersion.LATEST) -> PromptTemplate:
        """Retrieve a prompt template by name and version"""
        prompt_map = {
            ("research_planner", PromptVersion.V2): cls.RESEARCH_PLANNER_V2,
            ("decision_maker", PromptVersion.V2): cls.DECISION_MAKER_V2,
            ("result_analyzer", PromptVersion.V2): cls.RESULT_ANALYZER_V2,
            ("synthesizer", PromptVersion.V2): cls.SYNTHESIZER_V2,
        }
        return prompt_map.get((name, version))
    
    @classmethod
    def list_prompts(cls) -> List[str]:
        """List all available prompts"""
        return [
            "research_planner",
            "decision_maker",
            "result_analyzer",
            "synthesizer"
        ]
```

#### Step 2: Update `research_agent.py` to use PromptLibrary

Replace hardcoded prompts with library calls:

```python
from prompt_library import PromptLibrary, PromptVersion

class ResearchAgent:
    def __init__(self, llm_client: OpenRouterClient):
        self.llm = llm_client
        self.prompt_lib = PromptLibrary()
        # ... rest of init
    
    def plan_research(self, query: str) -> List[Dict[str, Any]]:
        """Create research plan using v2 prompt"""
        
        # Get prompt template
        prompt_template = self.prompt_lib.get_prompt("research_planner", PromptVersion.V2)
        
        # Add few-shot examples
        few_shot = self._get_few_shot_examples("research_planning")
        
        # Format prompt
        system_prompt = prompt_template.format(
            query=query,
            domain="general",  # Could be detected automatically
            depth_level="comprehensive",
            few_shot_examples=few_shot
        )
        
        user_prompt = f"Create research plan for: {query}"
        
        response = self.llm.generate_with_system_prompt(system_prompt, user_prompt)
        
        # Use robust extraction
        return self._robust_json_extract(response, fallback_plan=query)
```

---

## 2. Few-Shot Examples Integration

### Implementation

Create `few_shot_examples.py`:

```python
"""
Few-shot examples for improved prompt performance
"""

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
        }
    ]
    
    @classmethod
    def get_examples(cls, task_type: str, n: int = 2) -> str:
        """Get formatted examples for a task type"""
        examples_map = {
            "research_planning": cls.RESEARCH_PLANNING,
        }
        
        examples = examples_map.get(task_type, [])[:n]
        
        # Format as text
        formatted = []
        for ex in examples:
            formatted.append(f"Input: {ex['input']}\nOutput: {json.dumps(ex['output'], indent=2)}")
        
        return "\n\n---\n\n".join(formatted)
```

---

## 3. Robust JSON Extraction

### Current Problem
- Simple string manipulation fails frequently
- No fallback strategies
- Silent failures lead to poor results

### Solution: Multi-Strategy Extraction

Add to `research_agent.py`:

```python
import json
import re
from typing import Any, Optional, Dict, List


class JSONExtractionError(Exception):
    """Raised when all JSON extraction strategies fail"""
    pass


def _robust_json_extract(
    self, 
    response: str, 
    fallback_plan: Optional[Any] = None
) -> Any:
    """
    Multi-strategy JSON extraction with automatic repair
    
    Strategies (in order):
    1. Direct JSON parse
    2. Extract from markdown code blocks
    3. Extract with regex patterns
    4. Auto-repair common issues
    5. LLM-based repair
    6. Fallback to simple structure
    """
    
    # Strategy 1: Direct parse
    try:
        return json.loads(response.strip())
    except json.JSONDecodeError:
        pass
    
    # Strategy 2: Extract from code blocks
    try:
        code_block_pattern = r'```(?:json)?\s*([\s\S]*?)\s*```'
        matches = re.findall(code_block_pattern, response)
        if matches:
            return json.loads(matches[0].strip())
    except (json.JSONDecodeError, IndexError):
        pass
    
    # Strategy 3: Find JSON-like structures
    try:
        # Look for array brackets or object braces
        json_pattern = r'(\[[\s\S]*\]|\{[\s\S]*\})'
        matches = re.findall(json_pattern, response)
        if matches:
            return json.loads(matches[0])
    except (json.JSONDecodeError, IndexError):
        pass
    
    # Strategy 4: Auto-repair common issues
    try:
        repaired = self._repair_json(response)
        return json.loads(repaired)
    except json.JSONDecodeError:
        pass
    
    # Strategy 5: LLM-based repair (expensive but effective)
    try:
        repaired = self._llm_json_repair(response)
        return json.loads(repaired)
    except json.JSONDecodeError:
        pass
    
    # Strategy 6: Fallback
    if fallback_plan:
        return self._create_fallback_structure(fallback_plan)
    
    # All strategies failed
    raise JSONExtractionError(
        f"Failed to extract JSON from response. First 200 chars: {response[:200]}"
    )


def _repair_json(self, text: str) -> str:
    """Attempt to repair common JSON issues"""
    # Remove markdown formatting
    text = re.sub(r'```(?:json)?', '', text)
    text = text.strip()
    
    # Fix common issues
    # 1. Replace single quotes with double quotes
    text = re.sub(r"'([^']*)':", r'"\1":', text)
    
    # 2. Add missing commas between objects in arrays
    text = re.sub(r'\}\s*\{', '},{', text)
    
    # 3. Remove trailing commas
    text = re.sub(r',(\s*[\]}])', r'\1', text)
    
    # 4. Fix unquoted keys
    text = re.sub(r'(\w+):', r'"\1":', text)
    
    return text


def _llm_json_repair(self, broken_json: str) -> str:
    """Use LLM to repair JSON (last resort)"""
    repair_prompt = f"""Fix this broken JSON and return ONLY valid JSON:

{broken_json}

Return the corrected JSON without any explanation or markdown formatting."""
    
    response = self.llm.generate_with_system_prompt(
        "You are a JSON repair expert. Return only valid JSON.",
        repair_prompt,
        temperature=0.1  # Low temperature for deterministic output
    )
    
    return response.strip()


def _create_fallback_structure(self, query: str) -> List[Dict[str, Any]]:
    """Create a simple fallback research plan"""
    return [{
        "step": 1,
        "query": query,
        "reasoning": "Direct search for the main query (fallback mode)",
        "expected_info": "General information about the topic",
        "validation_criteria": "Relevant results returned",
        "confidence_threshold": 0.5
    }]
```

---

## 4. Self-Validation Loops

### Implementation

Add validation methods to `research_agent.py`:

```python
def _validate_research_plan(self, plan: List[Dict[str, Any]]) -> tuple[bool, List[str]]:
    """
    Agent validates its own research plan
    
    Returns:
        (is_valid, list of issues)
    """
    
    validation_prompt = f"""<task>
Review this research plan for quality and coherence.
</task>

<plan>
{json.dumps(plan, indent=2)}
</plan>

<validation_criteria>
1. Are questions atomic and focused (not too broad)?
2. Is there logical progression (foundational → specific)?
3. Are there redundant or overlapping queries?
4. Does it comprehensively cover the topic?
5. Are validation criteria specific and measurable?
6. Is the number of steps appropriate (3-5 ideal)?
</validation_criteria>

<output_format>
Return ONLY valid JSON:
{{
  "is_valid": true/false,
  "issues": ["issue 1", "issue 2", ...],
  "suggestions": ["suggestion 1", "suggestion 2", ...],
  "quality_score": 0.X
}}
</output_format>"""
    
    response = self.llm.generate_with_system_prompt(
        "You are a research plan validator ensuring quality and coherence.",
        validation_prompt
    )
    
    try:
        validation = self._robust_json_extract(response)
        return validation.get('is_valid', False), validation.get('issues', [])
    except JSONExtractionError:
        # If validation fails, assume plan is okay
        return True, []


def plan_research(self, query: str, max_attempts: int = 2) -> List[Dict[str, Any]]:
    """
    Create research plan with self-validation
    """
    for attempt in range(max_attempts):
        # Generate plan
        plan = self._generate_plan(query)
        
        # Validate plan
        is_valid, issues = self._validate_research_plan(plan)
        
        if is_valid:
            return plan
        
        # If invalid, add feedback for retry
        if attempt < max_attempts - 1:
            feedback = f"Previous plan had issues: {', '.join(issues)}. Please revise."
            query = f"{query}\n\nFeedback: {feedback}"
    
    # Return best attempt
    return plan
```

---

## Testing Procedures

### Test 1: Prompt Template Functionality
```python
def test_prompt_templates():
    lib = PromptLibrary()
    
    # Test retrieval
    prompt = lib.get_prompt("research_planner", PromptVersion.V2)
    assert prompt is not None
    
    # Test formatting
    formatted = prompt.format(
        query="test query",
        domain="test",
        depth_level="basic",
        few_shot_examples="example"
    )
    assert "test query" in formatted
    print("✓ Prompt templates working")
```

### Test 2: JSON Extraction Robustness
```python
def test_json_extraction():
    agent = ResearchAgent(llm)
    
    # Test various broken formats
    test_cases = [
        '```json\n[{"step": 1}]\n```',  # Code block
        "[{'step': 1}]",  # Single quotes
        '[{"step": 1,}]',  # Trailing comma
        'Here is the plan: [{"step": 1}]',  # Extra text
    ]
    
    for test in test_cases:
        result = agent._robust_json_extract(test)
        assert isinstance(result, list)
    
    print("✓ JSON extraction working")
```

### Test 3: Few-Shot Integration
```python
def test_few_shot():
    examples = FewShotExamples.get_examples("research_planning", n=2)
    assert len(examples) > 0
    assert "quantum computing" in examples.lower()
    print("✓ Few-shot examples working")
```

---

## Success Criteria

✅ **Phase 1 Complete When:**
1. All prompts migrated to `PromptLibrary`
2. Few-shot examples integrated for all critical prompts
3. JSON extraction success rate > 95%
4. Self-validation reduces invalid plans by 50%+
5. All tests passing

---

## Expected Outcomes

- **Response Quality:** +40-60% improvement
- **JSON Parse Failures:** Reduced from ~20% to <5%
- **Invalid Plans:** Reduced by 50%
- **Development Speed:** Faster iteration on prompts
- **A/B Testing:** Foundation for testing improvements

---

## Next Steps

After Phase 1 completion, proceed to:
→ **Phase 2: Architecture Foundations** (`PHASE2_ARCHITECTURE.md`)
