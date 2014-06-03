'''
Created on 9. 1. 2013.

@author: filip
'''

import ply.yacc as yacc
from mister.ast import Program, Variables, Initial, Target, And, Or, Constraint, Rules, Rule, Constant, Statement, Invariants
import mister.lexer
from mister.lexer import get_lexer

tokens = mister.lexer.tokens

def p_program(p):
    'program : vars rules init target invariants'
    p[0] = Program(p[1], p[2], p[3], p[4], p[5])

def p_vars(p):
    'vars : VARS varlist'
    p[0] = Variables(p[2])

def p_empty(p):
    'empty : '
    pass

def p_varlist(p):
    '''varlist : ID varlist
               | empty'''
    p[0] = [p[1]] + p[2] if len(p) == 3 else []

def p_init(p):
    'init : INIT constrlistand'
    p[0] = Initial(p[2])

def p_target(p):
    'target : TARGET constrlistor'
    p[0] = Target(p[2])

def p_constrlistand(p):
    '''constrlistand : constraint ',' constrlistand
                     | constraint'''
    p[0] = And([p[1]] + p[3].and_list if len(p) == 4 else [p[1]])

def p_constrlistor(p):
    '''constrlistor : constrlistand constrlistor
                    | empty'''
    p[0] = Or([p[1]] + p[2].or_list if len(p) == 3 else [])

def p_constraint(p):
    '''constraint : ID '=' NUMBER
                  | ID GTE NUMBER
                  | ID IN '[' NUMBER ',' NUMBER ']' '''
    if len(p) == 4:
        p[0] = Constraint(p[2], p[1], p[3])
    else:
        p[0] = Constraint(p[2], p[1], p[4], p[6])

def p_rules(p):
    'rules : RULES rulelist'
    p[0] = Rules(p[2])
    
def p_rulelist(p):
    '''rulelist : rule rulelist
                | empty'''
    p[0] = [p[1]] + p[2] if len(p) == 3 else []

def p_rule(p):
    '''rule : guardlist ARROW statementlist ';' '''
    p[0] = Rule(p[1], p[3])

def p_guardlist(p):
    '''guardlist : guard ',' guardlist
                 | guard'''
    p[0] = [p[1]] + p[3] if len(p) == 4 else [p[1]]

def p_guard(p):
    '''guard : constraint
             | unconstrained'''
    p[0] = p[1]

def p_unconstrained(p):
    'unconstrained : TRUE'
    p[0] = Constant(p[1])

def p_statementlist(p):
    '''statementlist : statement statementfollow
                     | empty'''
    p[0] = [p[1]] + p[2] if len(p) == 3 else []

def p_statementfollow(p):
    '''statementfollow : ',' statement statementfollow
                       | empty'''
    p[0] = [p[2]] + p[3] if len(p) == 4 else []
    
# We only have simple statements corresponding to ordinary Petri nets
def p_statement(p):
    '''statement : ID PRIME '=' ID '+' NUMBER
                 | ID PRIME '=' ID '-' NUMBER'''
    p[0] = Statement(p[5], p[1], p[4], p[6])

def p_invariants(p):
    '''invariants : INVARIANTS equallistor
                  | empty'''
    p[0] = Invariants(p[2] if len(p) == 3 else None)

def p_equallistor(p):
    '''equallistor : equallistand equallistor
                   | empty'''
    p[0] = Or([p[1]] + p[2].or_list if len(p) == 3 else [])

def p_equallistand(p):
    '''equallistand : equal ',' equallistand
                    | equal'''
    p[0] = And([p[1]] + p[3].and_list if len(p) == 4 else [p[1]])

def p_equal(p):
    '''equal : ID '=' NUMBER'''
    p[0] = Constraint('=', p[1], p[3])

def p_error(p):
    print("Parsing error: Syntax error in the input at '%s', line %d." % (p.value, p.lineno))

def get_parser():
    return yacc.yacc(debug = False, optimize = True, tabmodule = 'mister_yacctab')

def parse(text):
    lexer = get_lexer()
    parser = get_parser()
    return parser.parse(text, lexer = lexer)

if __name__ == '__main__':
    data = '''
        # Test input
        vars
            x y z
        rules
            x >= 1 -> x' = x - 1, y' = y + 1;
            z >= 3, y >= 2 -> x' = x + 2;
            true -> ;

        init
            x = 0, y = 5 # I don't specify z
        target
            z >= 4
        
        invariants
            x = 10, y = 17
            z = 4
    '''
    print parse(data)
    