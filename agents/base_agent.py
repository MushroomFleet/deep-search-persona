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
