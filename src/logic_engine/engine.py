"""
Logic Engine module for chess rules and AI reasoning.
Provides the main interface for logic programming operations.
"""

from src.logic_engine.knowledge_base import KnowledgeBase
from src.logic_engine.resolution import resolve
from src.logic_engine.unification import Variable


class LogicEngine:
    """
    Logic Engine for chess rules and AI reasoning.
    """
    
    def __init__(self):
        self.kb = KnowledgeBase()
    
    def assert_fact(self, predicate, *args):
        """
        Add a fact to the knowledge base.
        
        Args:
            predicate: The name of the predicate
            args: Arguments to the predicate
        """
        return self.kb.assert_fact(predicate, *args)
    
    def retract_fact(self, predicate, *args):
        """
        Remove a fact from the knowledge base.
        
        Args:
            predicate: The name of the predicate
            args: Arguments to the predicate
        """
        self.kb.retract_fact(predicate, *args)
    
    def add_rule(self, head_predicate, head_args, body):
        """
        Add a rule to the knowledge base.
        
        Args:
            head_predicate: The predicate for the head
            head_args: Arguments for the head predicate
            body: A list of (predicate, args) tuples representing the body
        """
        head = (head_predicate, head_args)
        return self.kb.add_rule(head, body)
    
    def query(self, predicate, *args):
        """
        Query the knowledge base.
        
        Args:
            predicate: The predicate to query
            args: Arguments with potential variables
            
        Returns:
            A list of solutions (variable bindings)
        """
        goal = (predicate, args)
        return resolve([goal], self.kb)
    
    def query_all(self, goals):
        """
        Query multiple goals.
        
        Args:
            goals: A list of (predicate, args) tuples
            
        Returns:
            A list of solutions (variable bindings)
        """
        return resolve(goals, self.kb)
    
    def clear(self):
        """Clear the knowledge base."""
        self.kb.clear()
    
    def variable(self, name):
        """
        Create a logic variable.
        
        Args:
            name: The name of the variable
            
        Returns:
            A Variable object
        """
        return Variable(name)