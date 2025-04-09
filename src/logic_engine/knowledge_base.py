"""
Knowledge Base module for storing facts and rules.
"""

class KnowledgeBase:
    """
    Knowledge Base stores facts and rules for the logic engine.
    A fact is a tuple (predicate, arguments)
    A rule is a tuple (head, body) where head is a fact and body is a list of facts
    """
    
    def __init__(self):
        self.facts = set()  # Using a set to avoid duplicates
        self.rules = []
    
    def assert_fact(self, predicate, *args):
        """
        Add a fact to the knowledge base.
        
        Args:
            predicate: The name of the predicate (string)
            args: Arguments to the predicate
        """
        fact = (predicate, args)
        self.facts.add(fact)
        return fact
    
    def retract_fact(self, predicate, *args):
        """
        Remove a fact from the knowledge base.
        
        Args:
            predicate: The name of the predicate
            args: Arguments to the predicate
        """
        fact = (predicate, args)
        if fact in self.facts:
            self.facts.remove(fact)
    
    def add_rule(self, head, body):
        """
        Add a rule to the knowledge base.
        
        Args:
            head: A fact representing the head of the rule
            body: A list of facts representing the body of the rule
        """
        rule = (head, body)
        self.rules.append(rule)
        return rule
    
    def get_facts(self, predicate=None):
        """
        Get all facts with a specific predicate.
        
        Args:
            predicate: The predicate to filter by (optional)
            
        Returns:
            A list of matching facts
        """
        if predicate is None:
            return list(self.facts)
        
        return [fact for fact in self.facts if fact[0] == predicate]
    
    def get_rules(self, head_predicate=None):
        """
        Get all rules with a specific head predicate.
        
        Args:
            head_predicate: The predicate of the head to filter by (optional)
            
        Returns:
            A list of matching rules
        """
        if head_predicate is None:
            return self.rules
        
        return [rule for rule in self.rules if rule[0][0] == head_predicate]
    
    def clear(self):
        """Clear all facts and rules from the knowledge base."""
        self.facts = set()
        self.rules = []