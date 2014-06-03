__author__ = 'fniksic'

class Node(object):
    pass

class Program(Node):
    def __init__(self, variables, rules, initial, target, invariants):
        self.variables = variables
        self.rules = rules
        self.initial = initial
        self.target = target
        self.invariants = invariants

    def __str__(self):
        strings = map_str((self.variables, self.rules, self.initial, self.target, self.invariants))
        return '\n'.join(strings)

class Variables(Node):
    def __init__(self, variable_list):
        self.variable_list = variable_list

    def __str__(self):
        return 'vars\n\t%s\n' % ' '.join(self.variable_list)

class Rules(Node):
    def __init__(self, rule_list):
        self.rule_list = rule_list

    def __str__(self):
        return 'rules\n\t%s\n' % '\n\n\t'.join(map_str(self.rule_list))

class Rule(Node):
    def __init__(self, guard_list, statement_list):
        self.guard_list = guard_list
        self.statement_list = statement_list

    def __str__(self):
        return '%s ->\n\t\t%s;' % (', '.join(map_str(self.guard_list)), ',\n\t\t'.join(map_str(self.statement_list)))

class Constraint(Node):
    def __init__(self, constr_type, variable, fst_arg, snd_arg = None):
        self.constr_type = constr_type
        self.variable = variable
        self.fst_arg = fst_arg
        self.snd_arg = snd_arg

    def __str__(self):
        if self.constr_type == 'in':
            return '%s in [%d, %d]' % (self.variable, self.fst_arg, self.snd_arg)
        else:
            return '%s %s %d' % (self.variable, self.constr_type, self.fst_arg)

class Constant(Node):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value

class Statement(Node):
    def __init__(self, operation, lvar, rvar, number):
        self.operation = operation
        self.lvar = lvar
        self.rvar = rvar
        self.number = number

    def __str__(self):
        return "%s' = %s %s %d" % (self.lvar, self.rvar, self.operation, self.number)

class Initial(Node):
    def __init__(self, constr_and):
        self.constr_and = constr_and

    def __str__(self):
        return 'init\n\t%s\n' % str(self.constr_and)

class Target(Node):
    def __init__(self, constr_or):
        self.constr_or = constr_or

    def __str__(self):
        return 'target\n\t%s\n' % str(self.constr_or)

class And(Node):
    def __init__(self, and_list):
        self.and_list = and_list

    def __str__(self):
        return ', '.join(map_str(self.and_list))

class Or(Node):
    def __init__(self, or_list):
        self.or_list = or_list

    def __str__(self):
        return '\n\t'.join(map_str(self.or_list))

class Invariants(Node):
    def __init__(self, constr_or):
        self.constr_or = constr_or

    def __str__(self):
        if self.constr_or is None:
            return ''
        else:
            return 'invariants\n\t%s\n' % str(self.constr_or)

def map_str(lst):
    return (str(item) for item in lst)
