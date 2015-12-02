'''
Created on Aug 30, 2013

@author: fniksic
'''
from data import Transition, CoverabilityInstance, eq, ge


def convert_to_single_init(instance):
    '''
    Converts an instance with more than one initial marking into an instance with just one initial marking.
    '''
    new_n = instance.n
    for i in xrange(instance.n):
        interval = instance.initial[i]
        if interval.ub is None:
            # We just add a new transition which pumps tokens into this place
            guard = [0] * new_n
            delta = [0] * new_n
            delta[i] = 1
            instance.transitions.append(Transition(guard, delta))
            interval.ub = interval.lb
        elif interval.lb < interval.ub:
            # We also have to add a new place
            new_n += 1
            guard = [0] * new_n
            delta = [0] * new_n
            guard[new_n - 1] = 1
            delta[new_n - 1] = -1
            delta[i] = 1
            instance.transitions.append(Transition(guard, delta))
            instance.vars.append('init__' + instance.vars[i])
            diff = interval.ub - interval.lb
            instance.initial.append(eq(diff))
            interval.ub = interval.lb
    
    instance.n = new_n
    
    # Pad the transitions and targets
    for t in instance.transitions:
        if len(t.w) < new_n:
            t.w.extend([0] * (new_n - len(t.w)))
            t.d.extend([0] * (new_n - len(t.w)))
    for t in instance.target:
        if len(t) < new_n:
            t.extend([ge(0) for _ in xrange(new_n - len(t))])
    if isinstance(instance, CoverabilityInstance):
        for t in instance.min_target:
            if len(t) < new_n:
                t.extend([0] * (new_n - len(t)))