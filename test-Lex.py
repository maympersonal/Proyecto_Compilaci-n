from Lexer.Parser_lex.regex import build_regex


# test
from pprint import pprint
regex = "a*"
dfa, errors = build_regex(regex, verbose=True)
pprint(dfa.transitions)

print("\n ------------------------------------------ \n")
regexoldLex = "[a-zA-Z_][a-zA-Z0-9_]*"
regex = "([a..z]|[A..Z]|_)([a..z]|[A..Z]|_|[0..9])*"
dfa, errors = build_regex(regex, verbose=True)
pprint(dfa.transitions)