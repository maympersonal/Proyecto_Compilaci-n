# convertir de AFN a AFD
from typing import Set, Dict

class AFN:
    def __init__(self, estados: Set, alfabeto: Set, transiciones: Dict[str, Dict[str, Set]], inicial: str, final: Set):
        self.estados = estados
        self.alfabeto = alfabeto
        self.transiciones = transiciones
        self.inicial = inicial
        self.final = final

    def __str__(self):
        return f'AFN(   Estados: {self.estados}, Alfabeto: {self.alfabeto}, Transiciones: {self.transiciones}, Inicial: {self.inicial}, Final: {self.final} )'

    def __repr__(self):
        return str(self)
    
    def epsilon_cerradura(self, estado: str):
        cerradura = {estado}
        pila = [estado]
        while pila:
            estado = pila.pop()
            for siguiente in self.transiciones[estado].get('', []):
                if siguiente not in cerradura:
                    cerradura.add(siguiente)
                    pila.append(siguiente)
        return cerradura
    def epsilon_cerradura_conjunto(self, estados: Set):
        cerradura = set()
        for estado in estados:
            cerradura |= self.epsilon_cerradura(estado) #union de conjuntos
        return cerradura
    
    def mover(self, estados: Set, simbolo: str):
        mover = set()
        for estado in estados:
            mover |= self.transiciones[estado].get(simbolo, set())
        return mover
    
    
class AFD:
    def __init__(self, estados: Set, alfabeto: Set, transiciones: Dict[str, Dict[str, str]], inicial: str, final: Set):
        self.estados = estados
        self.alfabeto = alfabeto
        self.transiciones = transiciones
        self.inicial = inicial
        self.final = final

    def __str__(self):
        return f'AFD(   Estados: {self.estados}, Alfabeto: {self.alfabeto}, Transiciones: {self.transiciones}, Inicial: {self.inicial}, Final: {self.final} )'
    
    def simular(self, cadena: str):
        estado_actual = self.inicial
        for caracter in cadena:
            estado_actual = self.transiciones[estado_actual][caracter]
        return estado_actual in self.final
    
# # test AFD llamado D
# #  afd que acepta (a|b)*abb
# estados = {'q0', 'q1', 'q2', 'q3'}
# alfabeto = {'a', 'b'}
# transiciones = {
#     'q0': {'a': 'q1', 'b': 'q0'},
#     'q1': {'a': 'q1', 'b': 'q2'},
#     'q2': {'a': 'q1', 'b': 'q3'},
#     'q3': {'a': 'q1', 'b': 'q0'}
# }
# inicial = 'q0'
# final = {'q3'}
# afd = AFD(estados, alfabeto, transiciones, inicial, final)
# print(afd.simular('ababababb')) # True


# TEST AFN CERRADURA:
# AFN PARA (a|b)*abb con 11 estados
estados = {'q0', 'q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7', 'q8', 'q9', 'q10'}
alfabeto = {'a', 'b'}
transiciones = {
    'q0': {'': {'q1', 'q7'}},
    'q1': {'': {'q2', 'q4'}},
    'q2': {'a': {'q3'}},
    'q3': {'': {'q6'}},
    'q4': {'b': {'q5'}},
    'q5': {'': {'q6'}},
    'q6': {'': {'q1', 'q7'}},
    'q7': {'a': {'q8'}},
    'q8': {'b': {'q9'}},
    'q9': {'b': {'q10'}},
    'q10': {}
}
inicial = 'q0'
final = {'q10'}
afn = AFN(estados, alfabeto, transiciones, inicial, final)
print(afn.epsilon_cerradura('q0')) # {'q0', 'q1', 'q2', 'q4', 'q7'}
