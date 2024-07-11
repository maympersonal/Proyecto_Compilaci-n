from typing import Dict, Tuple, Set
class NFA:
    def __init__(self, states, finals, transitions: Dict[Tuple[int,str],Set[int]], start=0):
        self.states = states
        self.start = start
        self.finals = set(finals)
        self.map = transitions
        self.vocabulary = set()
        self.transitions = { state: {} for state in range(states) }
        
        for (origin, symbol), destinations in transitions.items():
            assert hasattr(destinations, '__iter__'), 'Invalid collection of states'
            self.transitions[origin][symbol] = destinations
            self.vocabulary.add(symbol)
            
        self.vocabulary.discard('')
        
    def epsilon_transitions(self, state):
        assert state in self.transitions, 'Invalid state'
        try:
            return self.transitions[state]['']
        except KeyError:
            return ()

    def __str__(self) -> str:
        return f'NFA( states={self.states}, finals={self.finals}, transitions={self.map}, start={self.start} )'