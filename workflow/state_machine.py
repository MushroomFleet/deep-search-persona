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
        # Don't trigger validation if we have no research results yet
        if ctx.get("results_found", 0) == 0:
            return False
        # Don't re-trigger validation if already validating
        if self.current_state == WorkflowState.VALIDATING:
            return False
        return ctx.get("contradictions", 0) > 2 or ctx.get("confidence", 1.0) < 0.5
    
    def _is_stuck(self, ctx: Dict[str, Any]) -> bool:
        """Detect if research is stuck in a loop"""
        # Don't trigger stuck detection if already in REFINING state
        if self.current_state == WorkflowState.REFINING:
            return False
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
        # If stuck in refining loop (with or without results), force synthesis
        # This prevents infinite refining→searching loops
        if ctx.get("iterations_without_progress", 0) > 2:
            # We're stuck - synthesize whatever we have
            return self._transition_to(WorkflowState.SYNTHESIZING, "forcing_synthesis_stuck_in_loop")
        
        # If we have good coverage, move to synthesis
        if ctx.get("coverage", 0) > 0.7 and ctx.get("results_found", 0) > 0:
            return self._transition_to(WorkflowState.SYNTHESIZING, "sufficient_results_for_synthesis")
        
        # Otherwise, try searching again with refined strategy
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
