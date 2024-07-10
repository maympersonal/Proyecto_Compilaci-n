from automaton_NFA import NFA

def automata_union(a1, a2):
    transitions = {}
    
    start = 0
    d1 = 1
    d2 = a1.states + d1
    final = a2.states + d2
    
    for (origin, symbol), destinations in a1.map.items():
        ## Relocate a1 transitions ...  
        new_origins = [origin + d1] if origin != a1.start else [0, origin + d1]
        for new_origin in new_origins:
            new_destinations = [dest + d1 for dest in destinations]
            transitions.update({(new_origin, symbol): new_destinations})


    for (origin, symbol), destinations in a2.map.items():
        ## Relocate a2 transitions ...
        new_origins = [origin + d2] if origin != a2.start else [0, origin + d2]
        for new_origin in new_origins:
            new_destinations = [dest + d2 for dest in destinations]
            transitions.update({(new_origin, symbol): new_destinations})
    
    ## Add transitions from start state ...
    transitions[(start, '')] = [a1.start + d1, a2.start + d2]
    
    ## Add transitions to final state ...
    for final_state in a1.finals:
        transitions[(final_state + d1, '')] = [final]
    for final_state in a2.finals:
        transitions[(final_state + d2, '')] = [final]
            
    states = a1.states + a2.states + 2
    finals = { final }
    
    return NFA(states, finals, transitions, start)