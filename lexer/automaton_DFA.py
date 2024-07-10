from automaton_NFA import NFA
from typing import Dict, Tuple

class DFA(NFA):
    
    def __init__(self, states, finals:list[int], transitions:Dict[Tuple[int,str],int], start=0):
        assert all(isinstance(value, int) for value in transitions.values())
        assert all(len(symbol) > 0 for origin, symbol in transitions)
        
        transitions = { key: [value] for key, value in transitions.items() }
        NFA.__init__(self, states, finals, transitions, start)
        self.current = start
        
    def _move(self, symbol):
        current = self.current
        
        if symbol not in self.transitions[current]:
            raise ValueError(f'Invalid symbol {symbol} at state {current}')
        
        self.current = self.transitions[current][symbol][0]
        
    def _reset(self):
        self.current = self.start
        
    def recognize(self, string):
        self._reset()
        
        try:
            for symbol in string:
                self._move(symbol)
        except Exception:
            return False
        
        return self.current in self.finals