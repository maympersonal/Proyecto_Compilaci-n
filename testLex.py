from Lexer.Lexer import Lexer
from Lexer.Cmp_lex.grammarTest import tokens
from Lexer.Parser_lex.regex import build_regex
# test
from pprint import pprint
# regex = "a*"
# dfa, errors = build_regex(regex, verbose=True)
# # pprint(dfa.transitions)

# print("\n ------------------------------------------ \n")
# regexoldLex = "[a-zA-Z_][a-zA-Z0-9_]*"
# regex = "([a..z]|[A..Z]|_)([a..z]|[A..Z]|_|[0..9])*"
# dfa, errors = build_regex(regex, verbose=True)
# pprint(dfa.transitions)
def hacer_lex(archivo, stop = False):
    # Abrir el archivo en modo lectura    
    with open(archivo, 'r') as f:
        # Leer el contenido del archivo
        
        contenido = f.read()

        lexer = Lexer(tokens)
        tokenCreat, errors = lexer.Tokenize(contenido) 
        for token in tokenCreat:
            print(token) 
            
hacer_lex("programs/shorts/test0.hulk")
    
    