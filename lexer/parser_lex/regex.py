from typing import List, Tuple
from cmp_lex.utils import Token
from parser import evaluate_reverse_parse
from ast_lex import get_printer
from automaton_common import nfa_to_dfa, automata_minimization
from automaton_DFA import DFA

def build_regex(self, regex: str, verbose = False) -> Tuple[DFA, List[str]]:
    
    ast = ...
    if verbose:
        printer = get_printer()
        print(printer(ast))
    pass