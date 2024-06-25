import cmp.visitor as visitor

import inspect



class Node:
    def evaluate(self):
        raise NotImplementedError()
    
        
class Program(Node):
    def __init__(self, program_decl_list):
        super().__init__()
        self.program_decl_list = program_decl_list
    
    def print_visitor(self, visitor):
        decls = visitor.visit(self.program_decl_list)
        return f'({self.__class__.__name__} {decls})'

class DeclList(Node):
    def __init__(self, decls):
        super().__init__()
        self.decls = decls
        
    def print_visitor(self, visitor):
        decls = visitor.visit(self.decls)
        return f'({self.__class__.__name__} {decls})'
        

class ProgramLevelDecl(Node):
    def __init__(self, decl):
        super().__init__()
        self.decl = decl

    def print_visitor(self, visitor):
        decl = visitor.visit(self.decl)
        return f'({self.__class__.__name__} {decl})'

class TypeDeclaration(Node):
    def __init__(self, identifier, body):
        super().__init__()
        self.identifier = identifier
        self.body = body

    def print_visitor(self, visitor):
        identifier = visitor.visit(self.identifier)
        body = visitor.visit(self.body)
        return f'({self.__class__.__name__} {identifier} {body})'
        
class FunctionDeclaration(Node):
    def __init__(self, identifier, parameters, body):
        super().__init__()
        self.identifier = identifier
        self.parameters = parameters
        self.body = body

    def print_visitor(self, visitor):
        identifier = visitor.visit(self.identifier)
        parameters = visitor.visit(self.parameters)
        body = visitor.visit(self.body)
        return f'({self.__class__.__name__} {identifier} {parameters} {body})'
        
        
class Parameter(Node):
    def __init__(self, identifier, type_annotation):
        super().__init__()
        self.identifier = identifier
        self.type_annotation = type_annotation

    def print_visitor(self, visitor):
        identifier = visitor.visit(self.identifier)
        type_annotation = visitor.visit(self.type_annotation)
        return f'({self.__class__.__name__} {identifier} {type_annotation})'

class VarDeclaration(Node):
    def __init__(self, var_init_list, body):
        super().__init__()
        self.var_init_list = var_init_list
        self.body = body

    def print_visitor(self, visitor):
        var_init_list = visitor.visit(self.var_init_list)
        body = visitor.visit(self.body)
        return f'({self.__class__.__name__} {var_init_list} {body})'
        
class VarInit(Node):
    def __init__(self, type, identifier, expression, type_downcast=None):
        super().__init__()
        self.type = type
        self.identifier = identifier
        self.expression = expression
        self.type_downcast = type_downcast

    def print_visitor(self, visitor):
        identifier = visitor.visit(self.identifier)
        expression = visitor.visit(self.expression)
        type_downcast = visitor.visit(self.type_downcast)
        return f'({self.__class__.__name__} {identifier} {self.type} {expression} {type_downcast})'
        
class Conditional(Node):
    def __init__(self, condition, true_branch, false_branch=None):
        super().__init__()
        self.condition = condition
        self.true_branch = true_branch
        self.false_branch = false_branch

    def print_visitor(self, visitor):
        condition = visitor.visit(self.condition)
        true_branch = visitor.visit(self.true_branch)
        false_branch = visitor.visit(self.false_branch)
        return f'({self.__class__.__name__} {condition} {true_branch} {false_branch})'

class Loop(Node):
    def __init__(self, condition, body):
        super().__init__()
        self.condition = condition
        self.body = body

    def print_visitor(self, visitor):
        condition = visitor.visit(self.condition)
        body = visitor.visit(self.body)
        return f'({self.__class__.__name__} {condition} {body})'
        

class WhileLoop(Loop):
    pass
    
class ForLoop(Loop):
    def __init__(self, init, condition, increment, body):
        super().__init__(condition, body)
        self.init = init
        self.increment = increment
            
class FunctionCall(Node):
    def __init__(self, identifier, arguments):
        super().__init__()
        self.identifier = identifier
        self.arguments = arguments

    def print_visitor(self, visitor):
        identifier = visitor.visit(self.identifier)
        arguments = visitor.visit(self.arguments)
        return f'({self.__class__.__name__} {identifier} {arguments})'

class Scope(Node):
    def __init__(self, statements):
        super().__init__()
        self.statements = statements

    def print_visitor(self, visitor):
        statements = visitor.visit(self.statements)
        return f'({self.__class__.__name__} {statements})'
            
class Assignment(Node):
    def __init__(self, identifier, expression):
        super().__init__()
        self.identifier = identifier
        self.expression = expression
        
    def print_visitor(self, visitor):
        identifier = visitor.visit(self.identifier)
        expression = visitor.visit(self.expression)
        return f'({self.__class__.__name__} {identifier} {expression})'
        
class Argument(Node):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def print_visitor(self, visitor):
        value = visitor.visit(self.value)
        return f'({self.__class__.__name__} {value})'
        
class Instruction(Node):
    def print_visitor(self, visitor):
        return f'({self.__class__.__name__} {self})'

class Expression(Instruction):
    def print_visitor(self, visitor):
        return f'({self.__class__.__name__} {self})' 

class Aritmetic_operation(Expression):
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

class Term(Node):
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



class HulkPrintVisitor(object):
    def __init__(self):
        super().__init__()

    @visitor.on('node')
    def visit(self, node, tabs):
        pass
    
    @visitor.when(Node)
    def visit(self, node):
        return node.print_visitor(self)
  