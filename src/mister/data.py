'''
Created on 22. 3. 2013.

@author: filip
'''

class ReachabilityInstance(object):
    '''
    The instance of the reachability problem for Petri nets
    '''

    def __init__(self, variables, transitions, initial, target, invariants = None):
        self.n = len(variables)
        self.variables = variables
        self.transitions = transitions
        self.initial = initial
        self.target = target
        self.invariants = invariants

class CoverabilityInstance(ReachabilityInstance):
    '''
    The instance of the coverability problem for Petri nets
    '''
    
    def __init__(self, variables, transitions, initial, target, min_target, invariants = None):
        super(CoverabilityInstance, self).__init__(variables, transitions, initial, target, invariants)
        self.min_target = min_target

class Transition:
    '''
    Represents a transition in a Petri net.
    '''

    def __init__(self, w, d):
        '''
        w - a list of n natural numbers representing the preconditions for a transition
        d - a list of n integers representing the delta (increment/decrement) on each place
        '''
        self.w = w
        self.d = d

class Interval(object):
    '''
    Interval represents an interval of the form [lb, ub], where ub can be infinity (ub == None).
    '''

    def __init__(self, lb, ub = None):
        '''
        lb - a non-negative integer (lower bound)
        ub - a non-negative integer (upper bound) or None (unbounded)
        '''
        self.lb = lb
        self.ub = ub
    
def ge(x):
    return Interval(x)

def eq(x):
    return Interval(x, x)
