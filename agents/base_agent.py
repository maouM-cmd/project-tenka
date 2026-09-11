"""
Project TENKA - Base Agent Module
Abstract base class for hero agents with RAG querying and reasoning capabilities.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any
from project_tenka.core.rag_engine import HybridRAGEngine

class BaseHeroAgent(ABC):
    def __init__(self, name: str, title: str, creed: str, rag_engine: HybridRAGEngine):
        self.name = name
        self.title = title
        self.creed = creed
        self.rag_engine = rag_engine
        self.insights: List[str] = []

    def consult_knowledge(self, query: str, top_k: int = 3, category: str = None) -> List[Dict[str, Any]]:
        """Query the shared RAG knowledge base for grounding evidence."""
        return self.rag_engine.search(query, top_k=top_k, category=category)

    @abstractmethod
    def deliberate(self, topic: str, context: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Produce strategic reasoning, cited RAG sources, and concrete action proposals.
        topic: The central challenge/theme being addressed.
        context: Prior statements and arguments from other council agents.
        Returns: {
            "speaker": self.name,
            "title": self.title,
            "stance": str,
            "cited_facts": List[str],
            "critique": str,
            "proposal": str,
            "actionable_prototype": Dict[str, Any]
        }
        """
        pass
