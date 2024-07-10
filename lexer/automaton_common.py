from automaton_NFA import NFA
from automaton_DFA import DFA
from typing import Dict, Tuple, Set
from cmp_lex.utils import ContainerSet, DisjointSet

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

def distinguish_states(group: list, automaton: DFA, partition: DisjointSet):
    groups = {}
    vocabulary = tuple(automaton.vocabulary)

    for member in group:
        transitions = automaton.transitions[member.value]
        labels = ((transitions[symbol][0] if symbol in transitions else None) for symbol in vocabulary)
        key = tuple((partition[node].representative if node in partition.nodes else None) for node in labels)
        try:
            groups[key].append(member.value)
        except KeyError:
            groups[key] = [member.value]

    return [group for group in groups.values()]
            
def state_minimization(automaton: DFA):
    partition = DisjointSet(*range(automaton.states))
    partition.merge(set(automaton.finals))
    non_nifals = set(range(automaton.states)) - set(automaton.finals)
    partition.merge(non_nifals)

    while True:
        new_partition = DisjointSet(*range(automaton.states))
        for group in partition.groups:
            for subgroup in distinguish_states(group, automaton, partition):
                new_partition.merge(subgroup)
        if len(new_partition) == len(partition):
            break
        partition = new_partition

    return partition

def automata_minimization(automaton: DFA):
    partition = state_minimization(automaton)
    states = list(partition.representatives)
    transitions = {}

    for i, state in enumerate(states):
        origin = state.value
        for symbol, destinations in automaton.transitions[origin].items():
            representative = partition[destinations[0]].representative
            temp = states.index(representative)
            try:
                transitions[i, symbol]
                assert False
            except KeyError:
                transitions[i, symbol] = temp

    finals = [i for i, state in enumerate(states) if state.value in automaton.finals]
    start = states.index(partition[automaton.start].representative)

    return DFA(len(states), finals, transitions, start)