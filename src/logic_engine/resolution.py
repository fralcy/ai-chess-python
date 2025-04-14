"""
Resolution module for logic programming.
Implements SLD resolution for logic queries.
"""

from src.logic_engine.unification import unify, substitute, Variable


def resolve(goal, knowledge_base, predicate_handlers=None, max_depth=100):
    """
    Resolve a goal using SLD resolution.
    
    Args:
        goal: The goal to resolve (a list of facts)
        knowledge_base: The knowledge base to use
        predicate_handlers: Dictionary of handlers for special predicates
        max_depth: Maximum recursion depth
        
    Returns:
        A list of solutions (variable bindings)
    """
    if not isinstance(goal, list):
        goal = [goal]
    return resolve_goals(goal, knowledge_base, {}, predicate_handlers or {}, max_depth)


def resolve_goals(goals, kb, bindings, predicate_handlers, max_depth):
    """
    Resolve a list of goals.
    
    Args:
        goals: List of goals to resolve
        kb: Knowledge base
        bindings: Current variable bindings
        predicate_handlers: Dictionary of handlers for special predicates
        max_depth: Maximum recursion depth
        
    Returns:
        A list of solutions
    """
    if max_depth <= 0:
        return []  # Exceeded maximum depth
    
    if not goals:
        return [bindings]  # Empty goal list means success
    
    goal, rest_goals = goals[0], goals[1:]
    solutions = []
    
    # Try to resolve the first goal
    predicate, args = goal
    
    # If there is a handler for this predicate, use it
    if predicate in predicate_handlers:
        # Substitute any variables in the args
        bound_args = [substitute(arg, bindings) for arg in args]
        
        # Call the handler with the bound args
        result = predicate_handlers[predicate](bound_args, bindings)
        
        # If the handler returns True, the goal is satisfied
        if result:
            solutions.extend(resolve_goals(rest_goals, kb, bindings, predicate_handlers, max_depth - 1))
        
        return solutions
    
    # First, try facts
    for fact in kb.get_facts(predicate):
        _, fact_args = fact
        new_bindings = unify(args, fact_args, bindings.copy())
        if new_bindings is not None:
            solutions.extend(resolve_goals(rest_goals, kb, new_bindings, predicate_handlers, max_depth - 1))
    
    # Then, try rules
    for rule in kb.get_rules(predicate):
        head, body = rule
        # Create fresh variables (rename variables in the rule)
        var_map = {}
        head_fresh = freshen_variables(head, var_map)
        body_fresh = [freshen_variables(b, var_map) for b in body]
        
        # Try to unify the goal with the head of the rule
        new_bindings = unify(goal, head_fresh, bindings.copy())
        if new_bindings is not None:
            # Add the body goals to the goal list
            new_goals = body_fresh + rest_goals
            solutions.extend(resolve_goals(new_goals, kb, new_bindings, predicate_handlers, max_depth - 1))
    
    return solutions


def freshen_variables(term, var_map=None):
    """
    Create a copy of term with fresh variables.
    
    Args:
        term: The term to freshen
        var_map: Mapping from original variables to fresh variables
        
    Returns:
        A copy of term with fresh variables
    """
    if var_map is None:
        var_map = {}
    
    if isinstance(term, Variable):
        if term.name not in var_map:
            var_map[term.name] = Variable(f"{term.name}_{id(var_map)}")
        return var_map[term.name]
    
    if isinstance(term, (list, tuple)):
        # For a predicate and its arguments
        if len(term) == 2 and isinstance(term[0], str) and isinstance(term[1], tuple):
            predicate, args = term
            fresh_args = tuple(freshen_variables(arg, var_map) for arg in args)
            return (predicate, fresh_args)
        
        # For other lists/tuples
        return type(term)(freshen_variables(t, var_map) for t in term)
    
    return term