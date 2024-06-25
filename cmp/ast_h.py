import cmp.visitor as visitor 
import inspect
import cmp.semantic as semantic

class Node:
    def evaluate(self):
        raise NotImplementedError()

class BinaryNode:
    def evaluate(self):
        raise NotImplementedError()
          
class Program(Node):
    def __init__(self, program_decl_list):
        super().__init__()
        self.program_decl_list = program_decl_list
    
    def print_visitor(self, visitor):
        decls = visitor.visit(self.program_decl_list)
        return f'({self.__class__.__name__} {decls})'


class ProgramLevelDecl(Node):
    def __init__(self, decl):
        super().__init__()
        self.decl = decl

    def print_visitor(self, visitor):
        decl = visitor.visit(self.decl)
        return f'({self.__class__.__name__} {decl})'
        
class Instruction(Node):
    def print_visitor(self, visitor):
        return f'({self.__class__.__name__} {self})'

class Expression(Instruction):
    def print_visitor(self, visitor):
        return f'({self.__class__.__name__} {self})' 

class Aritmetic_operation(Expression,BinaryNode):#ver
    def __init__(self, term, aritmetic_operation):
        super().__init__()
        self.term = term
        self.aritmetic_operation = aritmetic_operation

    def print_visitor(self, visitor):
        return f'({self.__class__.__name__} {self})'
        
class Concat(Expression):
    def __init__(self, operation, atom, expression):
        super().__init__()
        self.operation = operation
        self.atom = atom
        self.expression = expression

    def print_visitor(self, visitor):
        atom = visitor.visit(self.atom)
        expression = visitor.visit(self.expression)
        return f'({self.__class__.__name__} {atom} {self.operation} {expression})'


class Add(Aritmetic_operation):
    def print_visitor(self, visitor):
        term = visitor.visit(self.term)
        arith_op = visitor.visit(self.aritmetic_operation)
        return f'({self.__class__.__name__} {term} {arith_op})'

class Sub(Aritmetic_operation):
    def print_visitor(self, visitor):
        term = visitor.visit(self.term)
        arith_op = visitor.visit(self.aritmetic_operation)
        return f'({self.__class__.__name__} {term} {arith_op})'

class Term(Node,BinaryNode):
    def __init__(self, factor, term):
        super().__init__()
        self.factor = factor
        self.term = term 

class Mod(Term):
    def print_visitor(self, visitor):
        factor = visitor.visit(self.factor)
        term = visitor.visit(self.term) if self.term else ''
        return f'({self.__class__.__name__} {factor} {term})'

class Div(Term):
    def print_visitor(self, visitor):
        factor = visitor.visit(self.factor)
        term = visitor.visit(self.term) if self.term else ''
        return f'({self.__class__.__name__} {factor} {term})'

class Mult(Term):
    def print_visitor(self, visitor):
        factor = visitor.visit(self.factor)
        term = visitor.visit(self.term) if self.term else ''
        return f'({self.__class__.__name__} {factor} {term})'

class Factor(Node):
    def __init__(self, base_exponent):
        super().__init__()
        self.base_exponent = base_exponent

class Power(Factor):
    def __init__(self, factor, base_exponent):
        super().__init__(base_exponent)
        self.factor = factor

    def print_visitor(self, visitor):
        factor = visitor.visit(self.factor)
        base_exponent = visitor.visit(self.base_exponent)
        return f'({self.__class__.__name__} {factor} {base_exponent}'
        
class Base_exponent(Node):
    def __init__(self, value):
        super().__init__()
        self.value = value

class Atom(Node):
    def __init__(self, value):
        super().__init__()
        self.value = value

class String(Atom):
    def __init__(self, value):
        super().__init__(value)
        self.value = value

    def print_visitor(self, visitor):
        return f'"{self.value}"'

class Number(Atom):
    def __init__(self, value):
        super().__init__(value)
        self.value = value
        
    def print_visitor(self, visitor):
        return f'{self.value}'

class Boolean(Atom):
    def __init__(self, value):
        super().__init__(value)
        self.value = value

    def print_visitor(self, visitor):
        return f'{self.value}'

class UnaryBuildInFunction(Atom):
    def __init__(self, func, argument):
        super().__init__(argument)
        self.func = func
        self.argument = argument

    def print_visitor(self, visitor):
        argument = visitor.visit(self.argument)
        return f'({self.func} {argument})'

class BinaryBuildInFunction(Atom):
    def __init__(self, func, argument1, argument2):
        self.func = func
        self.argument1 = argument1
        self.argument2 = argument2

    def print_visitor(self, visitor):
        argument1 = visitor.visit(self.argument1)
        argument2 = visitor.visit(self.argument2)
        return f'({self.func} {argument1} {argument2})'
        
class BuildInConst(Atom):
    def __init__(self, const):
        super().__init__(const)
        self.const = const

    def print_visitor(self, visitor):
        return f'{self.const}'
        
class Declaration(Node):
    pass

class Variable(Node):
    def __init__(self, id: str, instruction, type):
        super().__init__()
        self.id = id
        if type is None:
            self.instruction = instruction
        else: 
            self.instruction = type(instruction)

class Conditional_Expression(Node):
    pass
class Not(Conditional_Expression):
    def __init__(self,condition):
        super().__init__()
        self.condition = condition
    def print_visitor(self, visitor):
        condition = visitor.visit(self.condition) 
        return f'({self.__class__.__name__} {condition})'

class Or(Conditional_Expression):
    def __init__(self,condition,conditional_expression):
        super().__init__()
        self.condition = condition
        self.conditional_expression = conditional_expression
    def print_visitor(self, visitor):
        condition = visitor.visit(self.condition) 
        conditional_expression = visitor.visit(self.conditional_expression)
        return f'({self.__class__.__name__} {condition} {conditional_expression})'
class And(Conditional_Expression):
    def __init__(self,condition,conditional_expression):
        super().__init__()
        self.condition = condition
        self.conditional_expression = conditional_expression
    def print_visitor(self, visitor):
        condition = visitor.visit(self.condition) 
        conditional_expression = visitor.visit(self.conditional_expression)
        return f'({self.__class__.__name__} {condition} {conditional_expression})'

class Comparation(Node):
    def __init__(self,expr1,expr2):
        self.expr1 = expr1
        self.expr2 = expr2

    def print_visitor(self, visitor):
        argument1 = visitor.visit(self.expr1)
        argument2 = visitor.visit(self.expr2)
        return f'({expr1} {expr2})'

class Not_Equal(Comparation):
    def print_visitor(self, visitor):
        expr1 = visitor.visit(self.expr1)
        expr2 = visitor.visit(self.expr2) 
        return f'({self.__class__.__name__} {expr1} {expr2})'
 
class Equal(Comparation):
     def print_visitor(self, visitor):
        expr1 = visitor.visit(self.expr1)
        expr2 = visitor.visit(self.expr2) 
        return f'({self.__class__.__name__} {expr1} {expr2})'
class Less_Equal(Comparation):
     def print_visitor(self, visitor):
        expr1 = visitor.visit(self.expr1)
        expr2 = visitor.visit(self.expr2) 
        return f'({self.__class__.__name__} {expr1} {expr2})' 

class Greater_Equal(Comparation):
     def print_visitor(self, visitor):
        expr1 = visitor.visit(self.expr1)
        expr2 = visitor.visit(self.expr2) 
        return f'({self.__class__.__name__} {expr1} {expr2})'

class Less_Than(Comparation):
     def print_visitor(self, visitor):
        expr1 = visitor.visit(self.expr1)
        expr2 = visitor.visit(self.expr2) 
        return f'({self.__class__.__name__} {expr1} {expr2})'

class Greater_Than(Comparation):
     def print_visitor(self, visitor):
        expr1 = visitor.visit(self.expr1)
        expr2 = visitor.visit(self.expr2) 
        return f'({self.__class__.__name__} {expr1} {expr2})' 

class HulkPrintVisitor(object):
    def __init__(self):
        super().__init__()

    @visitor.on('node')
    def visit(self, node, tabs):
        pass
    
    @visitor.when(Node)
    def visit(self, node):
        return node.print_visitor(self)
  