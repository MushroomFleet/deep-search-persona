# Phase 2: Architecture Foundations Implementation Guide

**Timeline:** Week 3-4  
**Expected Impact:** 2-3x throughput improvement  
**Difficulty:** Medium-High  
**Priority:** 🔥 HIGH

---

## Overview

Phase 2 transforms the single-agent architecture into a specialized multi-agent system with parallel processing capabilities. This phase builds on the prompt engineering improvements from Phase 1 to create a more scalable and efficient research pipeline.

---

## 1. Specialized Sub-Agent Architecture

### Current Problem
- Single `ResearchAgent` handles all tasks (planning, searching, analyzing, validating, synthesizing)
- No specialization leads to suboptimal performance
- Sequential processing is inefficient
- Difficult to optimize individual capabilities

### Solution: Multi-Agent Orchestration

#### Step 1: Create Agent Base Class

Create `agents/base_agent.py`:

```python
"""
Base agent class for all specialized agents
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class AgentRole(Enum):
    """Types of specialized agents"""
    PLANNER = "planner"
    SEARCHER = "searcher"
    ANALYZER = "analyzer"
    VALIDATOR = "validator"
    SYNTHESIZER = "synthesizer"
    COORDINATOR = "coordinator"


@dataclass
class AgentMessage:
    """Message passed between agents"""
    sender: AgentRole
    recipient: AgentRole
    message_type: str  # REQUEST, RESPONSE, BROADCAST, STATUS
    content: Dict[str, Any]
    priority: int = 1  # 1=high, 3=low
    timestamp: datetime = None
    correlation_id: str = None  # Link request/response
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()


class BaseAgent(ABC):
    """Base class for all specialized agents"""
    
    def __init__(self, llm_client, role: AgentRole):
        self.llm = llm_client
        self.role = role
        self.message_queue = []
        self.state = {}
        self.performance_metrics = {
            "tasks_completed": 0,
            "avg_response_time": 0.0,
            "success_rate": 0.0
        }
    
    @abstractmethod
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Main processing method - must be implemented by subclasses"""
        pass
    
    def send_message(self, recipient: AgentRole, message_type: str, 
                     content: Dict[str, Any], priority: int = 1) -> AgentMessage:
        """Send a message to another agent"""
        message = AgentMessage(
            sender=self.role,
            recipient=recipient,
            message_type=message_type,
            content=content,
            priority=priority
        )
        return message
    
    def receive_message(self, message: AgentMessage):
        """Receive and queue a message"""
        self.message_queue.append(message)
        # Sort by priority
        self.message_queue.sort(key=lambda m: m.priority)
    
    def get_status(self) -> Dict[str, Any]:
        """Get current agent status"""
        return {
            "role": self.role.value,
            "queue_length": len(self.message_queue),
            "metrics": self.performance_metrics,
            "state": self.state
        }
    
    def update_metrics(self, success: bool, response_time: float):
        """Update performance metrics"""
        self.performance_metrics["tasks_completed"] += 1
        
        # Running average of response time
        n = self.performance_metrics["tasks_completed"]
        current_avg = self.performance_metrics["avg_response_time"]
        self.performance_metrics["avg_response_time"] = (
            (current_avg * (n - 1) + response_time) / n
        )
        
        # Running success rate
        current_rate = self.performance_metrics["success_rate"]
        success_value = 1.0 if success else 0.0
        self.performance_metrics["success_rate"] = (
            (current_rate * (n - 1) + success_value) / n
        )
```

#### Step 2: Create Specialized Agents

Create `agents/planner_agent.py`:

```python
"""
Planner Agent - Specializes in research planning
"""
from agents.base_agent import BaseAgent, AgentRole
from prompt_library import PromptLibrary, PromptVersion
from few_shot_examples import FewShotExamples
from typing import Dict, Any, List
import time


class PlannerAgent(BaseAgent):
    """Expert at creating structured research plans"""
    
    def __init__(self, llm_client):
        super().__init__(llm_client, AgentRole.PLANNER)
        self.prompt_lib = PromptLibrary()
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create research plan
        
        Input:
            - query: Research question
            - domain: Domain/field (optional)
            - depth: Depth level (optional)
        
        Output:
            - plan: List of research steps
            - confidence: Planning confidence
        """
        start_time = time.time()
        
        try:
            query = input_data["query"]
            domain = input_data.get("domain", "general")
            depth = input_data.get("depth", "comprehensive")
            
            # Get prompt and examples
            prompt_template = self.prompt_lib.get_prompt("research_planner", PromptVersion.V2)
            few_shot_examples = FewShotExamples.get_examples("research_planning", n=2)
            
            # Format prompt
            system_prompt = prompt_template.format(
                query=query,
                domain=domain,
                depth_level=depth,
                few_shot_examples=few_shot_examples
            )
            
            # Generate plan
            response = self.llm.generate_with_system_prompt(
                system_prompt,
                f"Create research plan for: {query}"
            )
            
            # Extract and validate
            from research_agent import ResearchAgent  # Import extraction logic
            plan = ResearchAgent._robust_json_extract(response, fallback_plan=query)
            
            # Self-validate
            is_valid, issues = self._validate_plan(plan)
            
            result = {
                "plan": plan,
                "confidence": 0.9 if is_valid else 0.6,
                "issues": issues,
                "metadata": {
                    "agent": self.role.value,
                    "query": query,
                    "steps": len(plan)
                }
            }
            
            # Update metrics
            response_time = time.time() - start_time
            self.update_metrics(success=is_valid, response_time=response_time)
            
            return result
            
        except Exception as e:
            self.update_metrics(success=False, response_time=time.time() - start_time)
            return {
                "plan": [],
                "confidence": 0.0,
                "error": str(e)
            }
    
    def _validate_plan(self, plan: List[Dict]) -> tuple[bool, List[str]]:
        """Validate research plan quality"""
        issues = []
        
        # Check structure
        if not plan or len(plan) == 0:
            issues.append("Plan is empty")
        
        if len(plan) > 5:
            issues.append("Too many steps (max 5 recommended)")
        
        # Check each step
        required_keys = ["step", "query", "reasoning"]
        for step in plan:
            missing = [k for k in required_keys if k not in step]
            if missing:
                issues.append(f"Step {step.get('step', '?')} missing: {missing}")
        
        return len(issues) == 0, issues
```

Create `agents/searcher_agent.py`:

```python
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
```

Create `agents/analyzer_agent.py`:

```python
"""
Analyzer Agent - Specializes in deep analysis of search results
"""
from agents.base_agent import BaseAgent, AgentRole
from prompt_library import PromptLibrary, PromptVersion
from typing import Dict, Any, List
import time


class AnalyzerAgent(BaseAgent):
    """Expert at analyzing and extracting insights from data"""
    
    def __init__(self, llm_client):
        super().__init__(llm_client, AgentRole.ANALYZER)
        self.prompt_lib = PromptLibrary()
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze search results
        
        Input:
            - query: Original search query
            - results: Search results to analyze
        
        Output:
            - key_findings: Extracted findings
            - confidence: Analysis confidence
            - gaps: Identified knowledge gaps
            - contradictions: Found contradictions
        """
        start_time = time.time()
        
        try:
            query = input_data["query"]
            results = input_data["results"]
            
            # Format results
            results_text = self._format_results(results)
            
            # Get analysis prompt
            prompt_template = self.prompt_lib.get_prompt("result_analyzer", PromptVersion.V2)
            
            system_prompt = prompt_template.format(
                query=query,
                results_text=results_text,
                result_count=len(results)
            )
            
            # Generate analysis
            response = self.llm.generate_with_system_prompt(
                system_prompt,
                f"Analyze results for: {query}",
                max_tokens=2000
            )
            
            # Extract analysis
            from research_agent import ResearchAgent
            analysis = ResearchAgent._robust_json_extract(response)
            
            result = {
                **analysis,
                "metadata": {
                    "agent": self.role.value,
                    "results_analyzed": len(results)
                }
            }
            
            # Update metrics
            response_time = time.time() - start_time
            confidence = analysis.get("confidence", 0.5)
            self.update_metrics(success=confidence > 0.6, response_time=response_time)
            
            return result
            
        except Exception as e:
            self.update_metrics(success=False, response_time=time.time() - start_time)
            return {
                "key_findings": [],
                "confidence": 0.0,
                "error": str(e)
            }
    
    def _format_results(self, results: List[Dict]) -> str:
        """Format search results for analysis"""
        formatted = []
        for i, result in enumerate(results[:5], 1):
            formatted.append(
                f"Result {i}:\n"
                f"Title: {result.get('title', 'N/A')}\n"
                f"Content: {result.get('content', result.get('snippet', 'N/A'))}\n"
            )
        return "\n\n".join(formatted)
```

#### Step 3: Create Agent Orchestrator

Create `agents/orchestrator.py`:

```python
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
```

---

## 2. Parallel Processing Implementation

### Update `pipeline.py` to use multi-agent system

```python
"""
Updated pipeline with multi-agent architecture
"""
from agents.orchestrator import AgentOrchestrator
from agents.base_agent import AgentRole


class ResearchPipeline:
    """
    Main orchestrator - now uses specialized agents
    """
    
    def __init__(self, api_key=None, model=None, search_api_key=None):
        # ... existing init code ...
        
        # Initialize multi-agent system
        self.orchestrator = AgentOrchestrator(self.llm, self.search)
    
    def _plan_phase(self):
        """Phase 1: Create research plan using PlannerAgent"""
        planner = self.orchestrator.get_agent(AgentRole.PLANNER)
        
        result = planner.process({
            "query": self.original_query,
            "domain": "general",
            "depth": "comprehensive"
        })
        
        self.research_plan = result["plan"]
        
        print(f"Research plan created with {len(self.research_plan)} steps:")
        for step in self.research_plan:
            print(f"  Step {step['step']}: {step['query']}")
    
    def _research_loop_parallel(self, max_iterations: int):
        """
        Phase 2: Execute research with parallel processing
        
        Major optimization: Search and analyze multiple queries simultaneously
        """
        iteration = 0
        
        while iteration < max_iterations:
            iteration += 1
            print(f"\n--- Iteration {iteration}/{max_iterations} ---")
            
            # Collect next queries to process
            queries_to_process = self._get_next_queries(num=3)
            
            if not queries_to_process:
                print("No more queries to process")
                break
            
            print(f"Processing {len(queries_to_process)} queries in parallel...")
            
            # PARALLEL EXECUTION - Major speedup!
            results = self.orchestrator.parallel_search_and_analyze(queries_to_process)
            
            # Store results
            for result in results:
                if result.get('key_findings'):
                    self._store_research_step(result, iteration)
            
            # Check if we should continue
            if self._should_complete():
                print("Research objectives met")
                break
        
        self.agent.current_phase = ResearchPhase.COMPLETED
    
    def _get_next_queries(self, num: int = 3) -> List[str]:
        """Get next queries from plan or generate new ones"""
        # Simple implementation: take next N from plan
        queries = []
        for step in self.research_plan[:num]:
            if step.get('query'):
                queries.append(step['query'])
        return queries
    
    def _should_complete(self) -> bool:
        """Determine if research is complete"""
        # Simple heuristic: completed all planned steps
        return len(self.agent.research_history) >= len(self.research_plan)
```

---

## 3. Memory and Context Management

Create `memory/research_memory.py`:

```python
"""
Research Memory System - Short-term and long-term storage
"""
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
import json


@dataclass
class MemoryItem:
    """Single item in research memory"""
    id: str
    content: Dict[str, Any]
    timestamp: datetime
    importance: float  # 0-1
    tags: List[str] = field(default_factory=list)
    relationships: List[str] = field(default_factory=list)  # IDs of related items


class ResearchMemory:
    """
    Manages short-term and long-term research memory
    
    Short-term: Current session findings
    Long-term: Persistent storage across sessions (future: vector DB)
    """
    
    def __init__(self):
        self.short_term = {}  # id -> MemoryItem
        self.long_term_file = "memory/long_term_memory.json"
        self.semantic_index = {}  # tag -> List[item_ids]
    
    def store(self, content: Dict[str, Any], importance: float = 0.5,
              tags: List[str] = None) -> str:
        """Store finding in memory"""
        item_id = self._generate_id()
        
        item = MemoryItem(
            id=item_id,
            content=content,
            timestamp=datetime.now(),
            importance=importance,
            tags=tags or []
        )
        
        # Store in short-term
        self.short_term[item_id] = item
        
        # Update semantic index
        for tag in item.tags:
            if tag not in self.semantic_index:
                self.semantic_index[tag] = []
            self.semantic_index[tag].append(item_id)
        
        # Auto-consolidate important items
        if importance > 0.8:
            self._consolidate_to_long_term(item)
        
        return item_id
    
    def retrieve_by_tag(self, tag: str, limit: int = 5) -> List[MemoryItem]:
        """Retrieve items by tag"""
        item_ids = self.semantic_index.get(tag, [])
        items = [self.short_term.get(id) for id in item_ids[:limit]]
        return [item for item in items if item is not None]
    
    def retrieve_recent(self, limit: int = 10) -> List[MemoryItem]:
        """Retrieve most recent items"""
        items = sorted(
            self.short_term.values(),
            key=lambda x: x.timestamp,
            reverse=True
        )
        return items[:limit]
    
    def retrieve_important(self, threshold: float = 0.7, limit: int = 10) -> List[MemoryItem]:
        """Retrieve high-importance items"""
        items = [
            item for item in self.short_term.values()
            if item.importance >= threshold
        ]
        items.sort(key=lambda x: x.importance, reverse=True)
        return items[:limit]
    
    def _consolidate_to_long_term(self, item: MemoryItem):
        """Move important items to long-term storage"""
        # Future: Store in vector database for semantic search
        # For now: Store in JSON file
        pass
    
    def _generate_id(self) -> str:
        """Generate unique ID for memory item"""
        return f"mem_{datetime.now().strftime('%Y%m%d%H%M%S%f')}"
    
    def clear_short_term(self):
        """Clear short-term memory (new session)"""
        self.short_term.clear()
        self.semantic_index.clear()
```

---

## Testing Procedures

### Test 1: Agent Communication
```python
def test_agent_communication():
    orchestrator = AgentOrchestrator(llm, search)
    
    # Test message routing
    message = AgentMessage(
        sender=AgentRole.PLANNER,
        recipient=AgentRole.SEARCHER,
        message_type="REQUEST",
        content={"query": "test"}
    )
    
    orchestrator.route_message(message)
    searcher = orchestrator.get_agent(AgentRole.SEARCHER)
    assert len(searcher.message_queue) == 1
    
    print("✓ Agent communication working")
```

### Test 2: Parallel Processing
```python
import time

def test_parallel_processing():
    orchestrator = AgentOrchestrator(llm, search)
    
    queries = ["query 1", "query 2", "query 3"]
    
    # Time parallel execution
    start = time.time()
    results = orchestrator.parallel_search_and_analyze(queries)
    parallel_time = time.time() - start
    
    assert len(results) == 3
    print(f"✓ Parallel processing completed in {parallel_time:.2f}s")
    
    # Compare with sequential (estimate)
    # Should be ~3x faster
```

### Test 3: Memory System
```python
def test_memory_system():
    memory = ResearchMemory()
    
    # Store items
    id1 = memory.store(
        {"finding": "test 1"},
        importance=0.9,
        tags=["important", "quantum"]
    )
    
    id2 = memory.store(
        {"finding": "test 2"},
        importance=0.5,
        tags=["quantum"]
    )
    
    # Retrieve
    quantum_items = memory.retrieve_by_tag("quantum")
    assert len(quantum_items) == 2
    
    important_items = memory.retrieve_important(threshold=0.8)
    assert len(important_items) == 1
    
    print("✓ Memory system working")
```

---

## Success Criteria

✅ **Phase 2 Complete When:**
1. All specialized agents implemented and tested
2. Agent orchestrator successfully coordinates agents
3. Parallel processing achieves 2-3x speedup
4. Memory system stores and retrieves findings
5. All integration tests passing

---

## Expected Outcomes

- **Throughput:** 2-3x improvement via parallelization
- **Specialization:** Each agent optimized for its task
- **Scalability:** Easy to add new agent types
- **Maintainability:** Clear separation of concerns
- **Performance Tracking:** Per-agent metrics

---

## Migration Guide

### From Single Agent to Multi-Agent

1. **Keep existing `ResearchAgent` temporarily** for compatibility
2. **Gradually migrate functions** to specialized agents
3. **Update `pipeline.py`** to use orchestrator
4. **Test each agent** individually before integration
5. **Enable parallel processing** once agents are stable

---

## Next Steps

After Phase 2 completion, proceed to:
→ **Phase 3: Advanced Features** (`PHASE3_ADVANCED.md`)
