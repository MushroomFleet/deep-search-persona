"""
Workflow Management Package
Dynamic state machine for adaptive research workflows
"""
from workflow.state_machine import (
    WorkflowState,
    StateTransition,
    ResearchStateMachine
)

__all__ = [
    'WorkflowState',
    'StateTransition',
    'ResearchStateMachine'
]
