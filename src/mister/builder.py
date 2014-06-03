'''
Created on Mar 21, 2013

@author: fniksic
'''
from data import CoverabilityInstance, Transition, Interval
from mister.ast import Constraint
from mister.data import ReachabilityInstance


def build_problem_instance(program_node):
    '''
    Process node of the form Program(variables, rules, initial, target, invariants)
    '''
    variables, n, var_ids = get_variables(program_node.variables)
    transitions = get_transitions(program_node.rules, n, var_ids)
    initial = get_initial(program_node.initial, n, var_ids)
    target, min_target = get_target(program_node.target, n, var_ids)
    invariants = get_invariants(program_node.invariants, n, var_ids)

    if min_target is None:
        return ReachabilityInstance(variables, transitions, initial, target, invariants)
    else:
        return CoverabilityInstance(variables, transitions, initial, target, min_target, invariants)

def get_variables(variables_node):
    '''
    Process node of the form Variables(variable_list)
    '''
    variables = variables_node.variable_list
    n = len(variables)
    var_ids = {}
    for i in xrange(n):
        if variables[i] in var_ids:
            raise Exception('Multiple occurrences of variable %s in the vars part of the input specification.' % variables[i])
        var_ids[variables[i]] = i
    return variables, n, var_ids

def get_var_id(v, var_ids):
    if v not in var_ids:
        raise Exception('Usage of an undefined variable %s.' % v)
    return var_ids[v]
    
def get_transitions(rules_node, n, var_ids):
    '''
    Process node of the form Rules(rule_list)
    '''
    return [rule_node_to_trans(rule_node, n, var_ids) for rule_node in rules_node.rule_list]

def rule_node_to_trans(rule_node, n, var_ids):
    '''
    Process node of the form Rule(guard_list, statement_list)
    '''
    guard = get_guard(rule_node.guard_list, n, var_ids)
    delta = get_delta(rule_node.statement_list, n, var_ids)
    return Transition(guard, delta)

def get_guard(constraints, n, var_ids):
    guard = [0] * n
    for constraint in constraints:
        if isinstance(constraint, Constraint):
            if constraint.constr_type != '>=':
                raise Exception('Guard not upward-closed.')
            i = get_var_id(constraint.variable, var_ids)
            guard[i] = max(guard[i], constraint.fst_arg)
    return guard

def get_delta(statements, n, var_ids):
    delta = [0] * n
    for stmnt in statements:
        if stmnt.lvar != stmnt.rvar:
            raise Exception('Two variables, %s and %s, used in a single update rule.' % (stmnt.lvar, stmnt.rvar))
        i = get_var_id(stmnt.lvar, var_ids)
        delta[i] = stmnt.number * (-1 if stmnt.operation == '-' else 1)
    return delta

def get_initial(initial_node, n, var_ids):
    '''
    Process node of the form Initial(constr_and)
    '''
    initial = get_intervals(initial_node.constr_and, n, var_ids)
    if not is_consistent(initial):
        raise Exception('Inconsistent initial condition.')
    return initial

def get_intervals(constr_and, n, var_ids):
    intervals = [Interval(0, None) for _ in xrange(n)]
    for constraint in constr_and.and_list:
        if isinstance(constraint, Constraint):
            v, lb, ub = get_bounds(constraint)
            i = get_var_id(v, var_ids)
            intervals[i].lb = max(intervals[i].lb, lb)
            intervals[i].ub = max(intervals[i].ub, ub) if intervals[i].ub is None or ub is None else min(intervals[i].ub, ub)
    return intervals

def get_bounds(constraint):
    if constraint.constr_type == '=':
        ub = constraint.fst_arg
    else:
        ub = constraint.snd_arg
    return constraint.variable, constraint.fst_arg, ub

def is_consistent(intervals):
    return all(interval.ub is None or interval.lb <= interval.ub for interval in intervals)

def is_upward_closed(intervals):
    return all(interval.ub is None for interval in intervals)

def get_target(target_node, n, var_ids):
    '''
    Process node of the form Target(constr_or). Returns target as a list of n-sized lists of Intervals, representing
    a union of target sets, and min_target, a set of minimal points if the target set is upward-closed.
    '''
    target = []
    min_target = []
    upward_closed = True
    for constr_and in target_node.constr_or.or_list:
        intervals = get_intervals(constr_and, n, var_ids)
        if is_consistent(intervals):
            target.append(intervals)
            upward_closed = upward_closed and is_upward_closed(intervals)
            if upward_closed:
                min_t = [interval.lb for interval in intervals]
                contained = any(lte(s, min_t, n) for s in min_target)
                if not contained:
                    min_target = [s for s in min_target if not lte(min_t, s, n)] + [min_t]
    return target, min_target if upward_closed else None

def lte(a, b, n):
    return all(a[i] <= b[i] for i in xrange(n))

def get_invariants(invariants_node, n, var_ids):
    '''
    Process node of the form Invariants(constr_or)
    '''
    # TODO: Deal with invariants
    return None
