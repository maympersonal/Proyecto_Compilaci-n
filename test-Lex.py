from Lexer.Parser_lex.regex import build_regex
from Lexer.Lexer import Lexer
from Lexer.Cmp_lex.utils import Grammar

# test
from pprint import pprint
regex = "a*"
dfa, errors = build_regex(regex, verbose=True)
# pprint(dfa.transitions)

print("\n ------------------------------------------ \n")
regexoldLex = "[a-zA-Z_][a-zA-Z0-9_]*"
regex = "([a..z]|[A..Z]|_)([a..z]|[A..Z]|_|[0..9])*"
dfa, errors = build_regex(regex, verbose=True)
# pprint(dfa.transitions)


G = Grammar()
string, identifier, number = G.Terminals("<string> <id> <number>")

keywords = [string, identifier, number]

regex_table_test = [
    (identifier, "([a..z]|[A..Z]|_)([a..z]|[A..Z]|_|[0..9])*"),
    (number, "([0..9]+\.)?[0..9]+"),
    (string, "\"((\\\\\")|(\\A))*\"")
]

lexer = Lexer(regex_table_test)
tokens, errors = lexer.Tokenize("a 5 3.14 \"Hello World\"") 
for token in tokens:
    print(token)