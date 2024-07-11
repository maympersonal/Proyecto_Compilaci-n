from typing import List, Tuple
from Lexer.Cmp_lex.utils import Token
from Lexer.Parser_lex.parser import evaluate_reverse_parse
from Lexer.Parser_lex.ast_lex import get_printer
from Lexer.Parser_lex.ast_eval_visitor import EvaluateVisitor
from Lexer.Parser_lex.grammar import RegexGrammar
from Lexer.automaton_common import nfa_to_dfa, automata_minimization    
from Lexer.Parser_lex.parser import SLR1Parser
from Lexer.automaton_DFA import DFA

def build_regex(regex: str, verbose = False) -> Tuple[DFA, List[str]]:
    tokens = []
    errors = []
    grammar = RegexGrammar()
    parser = SLR1Parser(grammar)
    
    for i, c in enumerate(regex):
        token = [x for x in grammar.terminals if x.Name == c]
        if len(token) > 0:
            tokens.append(token[0])
        else:
            errors.append(f"Invalid character {c} on column {i}")
            
    tokens.append(grammar.EOF)
    derivation, operations = parser(tokens)
    tokens = [Token(x.Name, x, 0) for x in tokens]
    ast = evaluate_reverse_parse(derivation, operations, tokens)
    evaluator = EvaluateVisitor()
    if verbose:
        printer = get_printer()
        print(printer(ast))
    nfa = evaluator.visit(ast)
    dfa = nfa_to_dfa(nfa)
    dfa = automata_minimization(dfa)
    return dfa, errors
