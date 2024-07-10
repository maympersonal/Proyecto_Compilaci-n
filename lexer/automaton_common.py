from automaton_NFA import NFA
from automaton_DFA import DFA
from typing import Dict, Tuple, Set
from cmp_lex.utils import ContainerSet

""" 
Conjunto de estados del NFA para los cuales hay una transición sobre el
símbolo de entrada a, a partir de cierto estado s en T.
"""
def move(automaton, states, symbol):
    moves = set()
    for state in states:
        try:
            moves.update(automaton.transitions[state][symbol])
        except KeyError:
            pass
    return moves

def epsilon_closure(automaton, states):
    pending = [ s for s in states ] # equivalente a list(states) pero me gusta así :p
    closure = { s for s in states } # equivalente a  set(states) pero me gusta así :p
    
    while pending:
        state = pending.pop()
        for dest in automaton.epsilon_transitions(state):
            if dest not in closure:
                closure.add(dest)
                pending.append(dest)
                
    return ContainerSet(*closure)

def nfa_to_dfa(automaton):
    transitions = {}
    
    start = epsilon_closure(automaton, [automaton.start])
    start.id = 0
    start.is_final = any(s in automaton.finals for s in start)
    states = [ start ]

    pending = [ start ]
    while pending:
        state = pending.pop()
        
        for symbol in automaton.vocabulary:
            dest = epsilon_closure(automaton, move(automaton, state, symbol))
            if not dest:
                continue
            
            try:
                transitions[state.id, symbol]
                assert False, 'Invalid DFA!!!'
            except KeyError:
                if dest not in states:
                    dest.id = len(states)
                    dest.is_final = any(s in automaton.finals for s in dest)
                    states.append(dest)
                    pending.append(dest)
                else:
                    dest = states[states.index(dest)]
                
                if len(dest) > 0:
                    transitions[state.id, symbol] = dest.id
    
    finals = [ state.id for state in states if state.is_final ]
    dfa = DFA(len(states), finals, transitions)
    return dfa