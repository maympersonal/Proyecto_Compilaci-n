import cmp.visitor as visitor

import inspect



class Node:
    def evaluate(self):
        raise NotImplementedError()

class Program(Node):
    def __init__(self, program_decl_list):
        self.program_decl_list = program_decl_list

class ProgramLevelDecl(Node):
    def __init__(self, decl):
        self.decl = decl

class Instruction(Node):
    pass

class Expression(Instruction):
    pass 

class Aritmetic_operation(Expression):
    def __init__(self, term, aritmetic_operation):
        self.term = term
        self.aritmetic_operation = aritmetic_operation

class Add(Aritmetic_operation):
    pass

class Sub(Aritmetic_operation):
    pass

class Term(Node):
    def __init__(self, factor, term):
        self.factor = factor
        self.term = term 

class Mod(Term):
    pass

class Div(Term):
    pass 

class Mult(Term):
    pass

class Factor(Node):
    def __init__(self, base_exponent):
        self.base_exponent = base_exponent

class Power(Factor):
    def __init__(self, factor, base_exponent):
        super().__init__(base_exponent)
        self.factor = factor
        
class Base_exponent(Node):
    def __init__(self, value):
        self.value = value

class Atom(Node):
    def __init__(self, value):
        self.value = value
class String(Atom):
    def __init__(self, value):
        self.value = value
class Number(Atom):
    def __init__(self, value):
        self.value = value
class Declaration(Node):
    pass

class Variable(Node):
    def __init__(self, id: str, instruction, type):
        self.id = id
        if type is None:
            self.instruction = instruction
        else: 
            self.instruction = type(instruction)






class HulkPrintVisitor(object):
    @visitor.on('node')
    def visit(self, node, tabs):
        pass

    @visitor.when(Program)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'Program'
        decls = self.visit(node.program_decl_list, tabs + 1)
        #return f'{ans}\n' + '\n'.join(decls)
        return f'{ans}\n{decls}'

    @visitor.when(ProgramLevelDecl)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__ ProgramLevelDecl'
        decl = self.visit(node.decl, tabs + 1)
        return f'{ans}\n{decl}'

    @visitor.when(Instruction)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__ Instruction'
        return ans + f'{node}'

    @visitor.when(Expression)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__ Expression'
        return ans + f'{node}'
    
    @visitor.when(Aritmetic_operation)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__ Aritmetic_operation'
        return ans + f'{node}'
    
    
    @visitor.when(Add)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__ Add'
        term = self.visit(node.term, tabs + 1)
        arith_op = self.visit(node.aritmetic_operation, tabs + 1)
        return f'{ans}\n{term}\n{arith_op}'
    
    @visitor.when(Sub)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\___ Sub'
        term = self.visit(node.term, tabs + 1)
        arith_op = self.visit(node.aritmetic_operation, tabs + 1)
        return f'{ans}\n{term}\n{arith_op}'

    @visitor.when(Mod)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__ Mod'
        factor = self.visit(node.factor, tabs + 1)
        term = self.visit(node.term, tabs + 1) if node.term else ''
        return f'{ans}\n{factor}\n{term}'

    @visitor.when(Div)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__ Div'
        factor = self.visit(node.factor, tabs + 1)
        term = self.visit(node.term, tabs + 1) if node.term else ''
        return f'{ans}\n{factor}\n{term}'

    @visitor.when(Mult)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__ Mult'
        factor = self.visit(node.factor, tabs + 1)
        term = self.visit(node.term, tabs + 1) if node.term else ''
        return f'{ans}\n{factor}\n{term}'

    @visitor.when(Power)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__ Power'
        factor = self.visit(node.factor, tabs + 1)
        base_exponent = self.visit(node.base_exponent, tabs + 1)
        return f'{ans}\n{factor}\n{base_exponent}'

    @visitor.when(Atom)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'{node.value}'
        return ans
    
    


