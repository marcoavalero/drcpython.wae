# ------------- # -------------- #
# J. Paul Daigle
# CSC 6340
# Fall 2009
# Assignment 1
# -------------- # ------------- #
# wae.py
# A complete python lex/yacc file
# creates an interpreter for the following
# <WAEStart ::= <WAE> SEMI
# <WAE> ::= <num> | {+ <WAE> <WAE> } | { - <WAE> <WAE> } | { with { <id> <WAE> } WAE } | <id> 
# ------------- # -------------- #

# token names

reserved = {
    'with' : 'WITH',
    'exit' : 'EXIT',}

tokens = [
    'NUMBER',
    'SEMI',
    'ID', 
    'PLUS','MINUS',
    'LBRACKET', 'RBRACKET' 
    ] + list(reserved.values())

# Tokens

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_RESERVED(t):
    r'[a-z][a-z]+'
    t.type = reserved.get(t.value, 'BOMB')
    return t

t_SEMI = r';'
t_ID = r'[a-z]'
t_PLUS = r'\+'
t_MINUS = r'\-'
t_LBRACKET = r'\{'
t_RBRACKET = r'\}'

#ignore spaces 
t_ignore = " \t \n \r"


#error handling

def t_error(t):
    print "Syntax Error: illegal character '%s'" % t.value[0]
    t.lexer.skip(1)

#Build lexer
import ply.lex as lex
lex.lex()

#dictionary of ids 

ids = {}

start = 'waestart'

def p_waestart_waest(p):
    'waestart : wae SEMI'
    print p[1]

def p_wae_group(p):
    'wae : LBRACKET wae RBRACKET'
    p[0] = p[2]

def p_wae_assign(p):
    'wae : WITH assign wae'
    p[0] = p[3]

def p_assign(p):
    'assign : LBRACKET setid RBRACKET'
    
def p_setid_set(p):
    'setid : ID wae'
    ids[p[1]] = p[2]
    
def p_wae_op(p):
    ''' wae : PLUS wae wae 
            | MINUS wae wae'''
    if p[1] == '+' : p[0] = p[2] + p[3]
    if p[1] == '-' : p[0] = p[2] - p[3]

def p_wae_number(p):
    'wae : NUMBER'
    p[0] = p[1]

def p_wae_id(p):
    'wae : ID'
    try:
        p[0] = ids[p[1]]
    except LookupError:
        print "Semantic Error '%s' undefined" % p[1]
        p[0] = 0

def p_wae_exit(p):
    'wae : EXIT'
    print 'goodbye'
    exit()

def p_error(p):
    print "Syntax error at '%s'" % p.value

import ply.yacc as yacc
yacc.yacc()

while True:
    try:
        s = raw_input('wae > ')
    except EOFError:
        break
    yacc.parse(s)
