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
        self.predicate_handlers = {}
    
    def assert_fact(self, predicate, *args):
        """
        Add a fact to the knowledge base.
        
        Args:
            predicate: The name of the predicate
            args: Arguments to the predicate
            
        Returns:
            The created fact
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
    
    def add_rule(self, head, body):
        """
        Add a rule to the knowledge base.
        
        Args:
            head: A tuple (predicate, args) representing the head of the rule
            body: A list of tuples representing the body of the rule
            
        Returns:
            The created rule
        """
        return self.kb.add_rule(head, body)
    
    def register_predicate_handler(self, predicate_name, handler_function):
        """
        Register a handler function for a special predicate.
        
        Args:
            predicate_name: The name of the predicate
            handler_function: A function that takes (args, bindings) and returns True/False
        """
        self.predicate_handlers[predicate_name] = handler_function
    
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
        return resolve(goal, self.kb, self.predicate_handlers)
    
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