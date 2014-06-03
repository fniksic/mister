'''
Created on 8. 1. 2013.

@author: filip
'''

import ply.lex as lex

reserved = {
    'init' : 'INIT',
    'rules': 'RULES',
    'target' : 'TARGET',
    'invariants' : 'INVARIANTS',
    'vars' : 'VARS',
    'true' : 'TRUE',
    'in' : 'IN'
}

literals = "=,;[]+-"

tokens = [
    'ID',
    'NUMBER',
    'ARROW',
    'GTE',
    'PRIME'
] + list(reserved.values())

t_ignore = ' \t'
t_ignore_COMMENT = r'\#.*'

t_ARROW  = r'\->'
t_GTE    = r'>='
t_PRIME  = r'\''

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print("Parsing error: Illegal character '%s'." % t.value[0])
    t.lexer.skip(1)

def get_lexer():
    return lex.lex(optimize = True, lextab = 'mister_lextab')

if __name__ == '__main__':
    data = '''
        # Test input
        vars
            x y z
        rules
            x >= 1 -> x' = x - 1, y' = y + 1;
            z >= 3, y >= 2 -> x' = x + 2;

        init
            x = 0, y = 5 # I don't specify z
        target
            z >= 4
            
        invariants
            x = 10, y = 17
            z = 4
    '''
    lexer = get_lexer()
    lexer.input(data)
    for token in lexer:
        print(token)