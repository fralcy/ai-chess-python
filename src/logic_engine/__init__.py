"""
Logic Programming Module for Chess AI.
This module implements a logic programming paradigm for chess rules and AI.
"""

from src.logic_engine.engine import LogicEngine
from src.logic_engine.knowledge_base import KnowledgeBase
from src.logic_engine.unification import Variable
from src.logic_engine.resolution import resolve

__all__ = [
    'LogicEngine',
    'KnowledgeBase',
    'Variable',
    'resolve'
]