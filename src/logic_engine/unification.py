"""
Unification module for logic programming.
Implements variable binding and unification algorithms.
"""

class Variable:
    """
    Represents a logic variable.
    """
    
    def __init__(self, name):
        self.name = name
    
    def __repr__(self):
        return f"Var({self.name})"
    
    def __eq__(self, other):
        if not isinstance(other, Variable):
            return False
        return self.name == other.name
    
    def __hash__(self):
        return hash(('Variable', self.name))


def is_variable(term):
    """Check if a term is a variable."""
    return isinstance(term, Variable)


def unify(t1, t2, bindings=None):
    """
    Unify two terms t1 and t2.
    
    Args:
        t1: First term
        t2: Second term
        bindings: Current variable bindings
        
    Returns:
        Updated bindings if unification succeeded, None otherwise
    """
    if bindings is None:
        bindings = {}
    
    # If terms are equal, no need for unification
    if t1 == t2:
        return bindings
    
    # If t1 is a variable, bind it to t2
    if is_variable(t1):
        return unify_var(t1, t2, bindings)
    
    # If t2 is a variable, bind it to t1
    if is_variable(t2):
        return unify_var(t2, t1, bindings)
    
    # If both are compounds (lists or tuples)
    if isinstance(t1, (list, tuple)) and isinstance(t2, (list, tuple)):
        if len(t1) != len(t2):
            return None
        
        # Unify each element
        for i in range(len(t1)):
            bindings = unify(t1[i], t2[i], bindings)
            if bindings is None:
                return None
        
        return bindings
    
    # If we get here, unification failed
    return None


def unify_var(var, term, bindings):
    """
    Unify a variable with a term.
    
    Args:
        var: The variable
        term: The term to unify with
        bindings: Current variable bindings
        
    Returns:
        Updated bindings
    """
    # If var is already bound, unify the binding with term
    if var.name in bindings:
        return unify(bindings[var.name], term, bindings)
    
    # If term is a variable and is bound, unify var with the binding
    if is_variable(term) and term.name in bindings:
        return unify(var, bindings[term.name], bindings)
    
    # Check for circular references (occurs check)
    if is_variable(term) and var.name == term.name:
        return bindings
    
    # If term contains var, unification fails (occurs check)
    if isinstance(term, (list, tuple)) and occurs_check(var, term, bindings):
        return None
    
    # Add the binding
    bindings[var.name] = term
    return bindings


def occurs_check(var, term, bindings):
    """
    Check if variable occurs in term.
    
    Args:
        var: The variable
        term: The term to check
        bindings: Current variable bindings
        
    Returns:
        True if var occurs in term, False otherwise
    """
    if term == var:
        return True
    
    if is_variable(term) and term.name in bindings:
        return occurs_check(var, bindings[term.name], bindings)
    
    if isinstance(term, (list, tuple)):
        return any(occurs_check(var, t, bindings) for t in term)
    
    return False


def substitute(term, bindings):
    """
    Apply variable bindings to a term.
    
    Args:
        term: The term to substitute variables in
        bindings: Variable bindings
        
    Returns:
        The term with variables substituted
    """
    if is_variable(term):
        if term.name in bindings:
            return substitute(bindings[term.name], bindings)
        return term
    
    if isinstance(term, (list, tuple)):
        return type(term)(substitute(t, bindings) for t in term)
    
    return term