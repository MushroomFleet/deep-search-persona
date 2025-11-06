"""
Research Memory System - Short-term and long-term storage
"""
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
import json
import uuid


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
        self._id_counter = 0  # Counter for unique IDs
    
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
    
    def get_all_items(self) -> List[MemoryItem]:
        """Get all items in short-term memory"""
        return list(self.short_term.values())
    
    def _consolidate_to_long_term(self, item: MemoryItem):
        """Move important items to long-term storage"""
        # Future: Store in vector database for semantic search
        # For now: Store in JSON file
        pass
    
    def _generate_id(self) -> str:
        """Generate unique ID for memory item"""
        self._id_counter += 1
        return f"mem_{datetime.now().strftime('%Y%m%d%H%M%S%f')}_{self._id_counter}"
    
    def clear_short_term(self):
        """Clear short-term memory (new session)"""
        self.short_term.clear()
        self.semantic_index.clear()
    
    def get_stats(self) -> Dict[str, Any]:
        """Get memory statistics"""
        return {
            "total_items": len(self.short_term),
            "total_tags": len(self.semantic_index),
            "avg_importance": sum(item.importance for item in self.short_term.values()) / len(self.short_term) if self.short_term else 0,
            "high_importance_count": len([item for item in self.short_term.values() if item.importance > 0.7])
        }
