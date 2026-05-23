import re

# Keywords for C, C++, Java, Python, C#
keywords = [
    'int', 'float', 'double', 'char', 'if', 'else', 'while', 'for', 'return',
    'class', 'public', 'private', 'protected', 'void', 'static', 'import',
    'def', 'print', 'using', 'namespace', 'string', 'bool', 'true', 'false',
    'System', 'Console', 'out', 'println', 'Main', 'args', 'new', 'this'
]

# Token specification
# Add [] and <> to SYMBOL, :: to OP
token_specification = [
    ('NUMBER',   r'\b\d+(\.\d+)?\b'),                      
    ('ID',       r'[A-Za-z_][A-Za-z0-9_]*'),              
    ('OP',       r'(\+\+|--|==|!=|<=|>=|&&|\|\||::|[+\-*/=<>!])'),  
    ('STRING',   r'"([^"\\]|\\.)*"|\'([^\'\\]|\\.)*\''),  
    ('SYMBOL',   r'[;,\.\(\)\{\}\[\]<>]'),                
    ('NEWLINE',  r'\n'),                                  
    ('SKIP',     r'[ \t]+'),                              
    ('MISMATCH', r'.'),                                   
]

# Compile regex
tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)

def tokenize(code):
    tokens = []
    for mo in re.finditer(tok_regex, code, re.MULTILINE):
        kind = mo.lastgroup
        value = mo.group()
        
        # Convert identifiers that are keywords
        if kind == 'ID' and value in keywords:
            kind = 'KEYWORD'
        elif kind in ['SKIP', 'NEWLINE']:
            continue
        elif kind == 'MISMATCH':
            kind = 'UNKNOWN'
        
        tokens.append((kind, value))
    
    return tokens