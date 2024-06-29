import cmp.visitor as visitor


import inspect


def print_nested_list(lst, visitor):

    result = []

    for element in lst:
        if isinstance(element, list):
            result.append(print_nested_list(element, visitor))
        else:
            result.append(element)
        print(result)

    return "[" + " , ".join([visitor.visit(pdl) for pdl in result]) + "]"


class Node:

    def evaluate(self):
        raise NotImplementedError()


class Program(Node):

    def __init__(self, program_decl_list):
        super().__init__()
        self.program_decl_list = program_decl_list

    def print_visitor(self, visitor):
        decls = " , ".join([
            visitor.visit(pr) for pr in self.program_decl_list
        ]) if isinstance(self.program_decl_list, list) else visitor.visit(
            self.program_decl_list)
        return f'{self.__class__.__name__} ({decls})'


class DeclList(Node):

    def __init__(self, decls):
        super().__init__()
        self.decls = decls

    def print_visitor(self, visitor):
        decls = visitor.visit(self.decls)
        return f'{self.__class__.__name__} ({decls})'


class ProgramLevelDecl(Node):

    def __init__(self, decl):
        super().__init__()
        self.decl = decl

    def print_visitor(self, visitor):
        decl = visitor.visit(self.decl)
        return f'{self.__class__.__name__} ({decl})'


class TypeDeclaration(Node):

    def __init__(self, identifier, body):
        super().__init__()
        self.identifier = identifier
        self.body = body

    def print_visitor(self, visitor):
        identifier = visitor.visit(self.identifier)
        body = visitor.visit(self.body)
        return f'{self.__class__.__name__} ({identifier} {body})'


class FunctionDeclaration(Node):

    def __init__(self, identifier, body, type_anotation = None, parameters=[]):
        super().__init__()
        self.identifier = identifier
        self.type_anotation = type_anotation
        self.parameters = parameters
        self.body = body
    
    def print_visitor(self, visitor):
        #type_anotation = visitor.visit(self.type_anotation)
        parameters = " , ".join([visitor.visit(pr) for pr in self.parameters])
        body = visitor.visit(self.body)
        return f'{self.__class__.__name__} ({self.identifier} {self.type_anotation} {parameters} {body})'



class Parameter(Node):

    def __init__(self, identifier, type_annotation):
        super().__init__()
        self.identifier = identifier
        self.type_annotation = type_annotation

    def print_visitor(self, visitor):
        identifier = visitor.visit(self.identifier)
        type_annotation = visitor.visit(self.type_annotation)
        return f'{self.__class__.__name__} ({identifier} {type_annotation})'


class VarDeclaration(Node):

    def __init__(self, var_init_list, body):
        super().__init__()
        self.var_init_list = var_init_list
        self.body = body

    def print_visitor(self, visitor):
        var_init_list = " , ".join(
            [visitor.visit(pr) for pr in self.var_init_list])
        body = visitor.visit(self.body)
        return f'{self.__class__.__name__} ({var_init_list} {body})'


class TypeDowncast(Node):

    def __init__(self, identifier=None):
        super().__init__()
        self.identifier = identifier

    def print_visitor(self, visitor):
        identifier = visitor.visit(self.identifier) if isinstance(self.identifier, VarUse) else self.identifier
        return f'{self.__class__.__name__} ({identifier})'

class TypeConforming(Node):

    def __init__(self, identifier=None):
        super().__init__()
        self.identifier = identifier

    def print_visitor(self, visitor):
        return f'{self.__class__.__name__} ({self.identifier})'

class VarInit(Node):

    def __init__(self, identifier, expression, type_downcast=TypeDowncast()):
        super().__init__()
        self.identifier = identifier
        self.expression = expression
        self.type_downcast = type_downcast

    def print_visitor(self, visitor):
        identifier = visitor.visit(self.identifier)
        expression = visitor.visit(self.expression)
        type_downcast = visitor.visit(self.type_downcast)
        return f'{self.__class__.__name__} ({identifier} {expression} {type_downcast})'


class VarUse(Node):

    def __init__(self, identifier, type=None):
        super().__init__()
        self.type = type
        self.identifier = identifier

    def print_visitor(self, visitor):
        identifier = self.identifier if isinstance(self.identifier, str) else visitor.visit(self.identifier)
        return f'{self.__class__.__name__} ({identifier} {self.type})'

class VectorVarUse(Node):

    def __init__(self, identifier, index):
        super().__init__()
        self.index = index
        self.identifier = identifier

    def print_visitor(self, visitor):
        index = visitor.visit(self.index)
        identifier = self.identifier if isinstance(self.identifier, str) else visitor.visit(self.identifier)
        return f'{self.__class__.__name__} ({identifier} {index})'

class InlineConditional(Node):

    def __init__(self, conditional_expression, expression,
                 else_elif_statement):
        self.conditional_expression = conditional_expression
        self.expression = expression
        self.else_elif_statement = else_elif_statement

    def print_visitor(self, visitor):
        conditional_expression = visitor.visit(self.conditional_expression)
        true_branch = visitor.visit(self.expression)
        false_branch = visitor.visit(self.else_elif_statement)
        return f'{self.__class__.__name__} ({conditional_expression} {true_branch} {false_branch})'


class FullConditional(Node):

    def __init__(self, conditional_expression, scope_list,
                 else_elif_statement):
        self.conditional_expression = conditional_expression
        self.scope_list = scope_list
        self.else_elif_statement = else_elif_statement

    def print_visitor(self, visitor):
        conditional_expression = visitor.visit(self.conditional_expression)
        scope_list = " , ".join([visitor.visit(pr) for pr in self.scope_list])
        else_elif_statement = visitor.visit(self.else_elif_statement)
        return f'{self.__class__.__name__} ({conditional_expression} {scope_list} {else_elif_statement})'


class WhileLoop(Node):

    def __init__(self, condition, body):
        super().__init__()
        self.condition = condition
        self.body = body

    def print_visitor(self, visitor):
        condition = visitor.visit(self.condition)
        body = visitor.visit(self.body)
        return f'{self.__class__.__name__} ({condition} {body})'


class ForLoop(Node):

    def __init__(self, identifier, expression, body):
        super().__init__()
        self.identifier = identifier
        self.expression = expression
        self.body = body

    def print_visitor(self, visitor):
        identifier = visitor.visit(self.identifier)
        expression = visitor.visit(self.expression)
        body = visitor.visit(self.body)
        return f'{self.__class__.__name__} ({identifier} {expression} {body})'


class FunctionCall(Node):

    def __init__(self, identifier, arguments=[]):
        super().__init__()
        self.identifier = identifier
        self.arguments = arguments

    def print_visitor(self, visitor):
        arguments = " , ".join([visitor.visit(pr) for pr in self.arguments])
        return f'{self.__class__.__name__} ({self.identifier} {arguments})'


class Scope(Node):

    def __init__(self, statements):
        super().__init__()
        self.statements = statements
        print(self.statements)

    def print_visitor(self, visitor):
        statements = [visitor.visit(st) for st in self.statements]
        return f'{self.__class__.__name__} ({" , ".join(statements)})'


class ScopeList(Node):

    def __init__(self, scopes):
        super().__init__()
        self.scopes = scopes

    def print_visitor(self, visitor):
        scopes = [visitor.visit(sc) for sc in self.scopes]
        return f'{self.__class__.__name__} ({scopes})'


class Assignment(Node):

    def __init__(self, identifier, expression):
        super().__init__()
        self.identifier = identifier
        self.expression = expression

    def print_visitor(self, visitor):
        identifier = visitor.visit(self.identifier)
        expression = visitor.visit(self.expression)
        return f'{self.__class__.__name__} ({identifier} {expression})'


class Argument(Node):

    def __init__(self, value):
        super().__init__()
        self.value = value

    def print_visitor(self, visitor):
        value = visitor.visit(self.value)
        return f'{self.__class__.__name__} ({value})'


class Instruction(Node):

    def print_visitor(self, visitor):
        return f'{self.__class__.__name__} ({self})'


class Expression(Instruction):

    def print_visitor(self, visitor):
        return f'{self.__class__.__name__} ({self})'


class Aritmetic_operation(Expression):

    def __init__(self, term, aritmetic_operation):
        super().__init__()
        self.term = term
        self.aritmetic_operation = aritmetic_operation

    def print_visitor(self, visitor):
        return f'{self.__class__.__name__} ({self})'


class Concat(Expression):

    def __init__(self, operation, atom, expression):
        super().__init__()
        self.operation = operation
        self.atom = atom
        self.expression = expression

    def print_visitor(self, visitor):
        atom = visitor.visit(self.atom)
        expression = visitor.visit(self.expression)
        return f'{self.__class__.__name__} ({atom} {self.operation} {expression})'


class Add(Aritmetic_operation):

    def print_visitor(self, visitor):
        term = visitor.visit(self.term)
        arith_op = visitor.visit(self.aritmetic_operation)
        return f'{self.__class__.__name__} ({term} {arith_op})'


class Sub(Aritmetic_operation):

    def print_visitor(self, visitor):
        term = visitor.visit(self.term)
        arith_op = visitor.visit(self.aritmetic_operation)
        return f'{self.__class__.__name__} ({term} {arith_op})'


class Term(Node):

    def __init__(self, factor, term):
        super().__init__()
        self.factor = factor
        self.term = term


class Mod(Term):

    def print_visitor(self, visitor):
        factor = visitor.visit(self.factor)
        term = visitor.visit(self.term) if self.term else ''
        return f'{self.__class__.__name__} ({factor} {term})'


class Div(Term):

    def print_visitor(self, visitor):
        factor = visitor.visit(self.factor)
        term = visitor.visit(self.term) if self.term else ''
        return f'{self.__class__.__name__} ({factor} {term})'


class Mult(Term):

    def print_visitor(self, visitor):
        factor = visitor.visit(self.factor)
        term = visitor.visit(self.term) if self.term else ''
        return f'{self.__class__.__name__} ({factor} {term})'


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
        return f'{self.__class__.__name__} ({factor} {base_exponent})'


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

class Unary(Node):
    def __init__(self, sign, factor):
        super().__init__()
        self.sign = sign
        self.factor = factor
    
    def print_visitor(self, visitor):
        factor = visitor.visit(self.factor)
        return f'{self.__class__.__name__} ({self.sign} {factor})'
        
class UnaryBuildInFunction(Atom):

    def __init__(self, func, argument):
        super().__init__(argument)
        self.func = func
        self.argument = argument

    def print_visitor(self, visitor):
        argument = visitor.visit(self.argument)
        return f'{self.func} ({argument})'


class BinaryBuildInFunction(Atom):

    def __init__(self, func, argument1, argument2):
        self.func = func
        self.argument1 = argument1
        self.argument2 = argument2

    def print_visitor(self, visitor):
        argument1 = visitor.visit(self.argument1)
        argument2 = visitor.visit(self.argument2)
        return f'{self.func} ({argument1} {argument2})'


class NoParamBuildInFunction(Atom):

    def __init__(self, func):
        self.func = func

    
    def print_visitor(self, visitor):

        return f'{self.func}'
    
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

    def __init__(self, condition):
        super().__init__()
        self.condition = condition

    def print_visitor(self, visitor):
        condition = visitor.visit(self.condition)
        return f'{self.__class__.__name__} ({condition})'


class Or(Conditional_Expression):

    def __init__(self, condition, conditional_expression):
        super().__init__()
        self.condition = condition
        self.conditional_expression = conditional_expression

    def print_visitor(self, visitor):
        condition = visitor.visit(self.condition)
        conditional_expression = visitor.visit(self.conditional_expression)
        return f'{self.__class__.__name__} ({condition} {conditional_expression})'


class And(Conditional_Expression):

    def __init__(self, condition, conditional_expression):
        super().__init__()
        self.condition = condition
        self.conditional_expression = conditional_expression

    def print_visitor(self, visitor):
        condition = visitor.visit(self.condition)
        conditional_expression = visitor.visit(self.conditional_expression)
        return f'{self.__class__.__name__} ({condition} {conditional_expression})'

class Is(Conditional_Expression):

    def __init__(self, condition, conditional_expression):
        super().__init__()
        self.condition = condition
        self.conditional_expression = conditional_expression

    def print_visitor(self, visitor):
        conditional_expression = visitor.visit(self.conditional_expression)
        return f'{self.__class__.__name__} ({self.condition} {conditional_expression})'

class Comparation(Node):

    def __init__(self, expr1, expr2):
        super().__init__()
        self.expr1 = expr1
        self.expr2 = expr2

    def print_visitor(self, visitor):
        expr1 = visitor.visit(self.expr1)
        expr2 = visitor.visit(self.expr2)
        return f'{self.__class__.__name__} ({expr1} {expr2})'


class NotEqual(Comparation):

    def __init__(self, expr1, expr2):
        super().__init__(expr1, expr2)


class Equal(Comparation):

    def __init__(self, expr1, expr2):
        super().__init__(expr1, expr2)


class LessEqual(Comparation):

    def __init__(self, expr1, expr2):
        super().__init__(expr1, expr2)


class GreaterEqual(Comparation):

    def __init__(self, expr1, expr2):
        super().__init__(expr1, expr2)


class LessThan(Comparation):

    def __init__(self, expr1, expr2):
        super().__init__(expr1, expr2)


class GreaterThan(Comparation):

    def __init__(self, expr1, expr2):
        super().__init__(expr1, expr2)


class VarMethod(Node):

    def __init__(self, identifier, function_call):
        super().__init__()
        self.identifier = identifier
        self.function_call = function_call

    def print_visitor(self, visitor):
        function_call = visitor.visit(self.function_call)
        return f'{self.__class__.__name__} ({self.identifier} {function_call})'


class VarAttr(Node):

    def __init__(self, identifier, attr):
        super().__init__()
        self.identifier = identifier
        self.attr = attr

    def print_visitor(self, visitor):
        attr = self.attr if isinstance(self.attr, str) else visitor.visit(self.attr)
        print(attr)
        return f'{self.__class__.__name__} ({self.identifier} {attr})'


class TypeDeclaration(Node):
    def __init__(self, identifier, parameters=None, inherits_type=None, decl_body=None):
        super().__init__()
        self.identifier = identifier
        self.parameters = parameters
        self.inherits_type = inherits_type
        self.decl_body = decl_body

    def print_visitor(self, visitor):
        parameters = [visitor.visit(pr) for pr in self.parameters] if self.parameters != None else None
        inherits_type = visitor.visit(self.inherits_type) if self.inherits_type != None else None
        decl_body = visitor.visit(self.decl_body)

        return f'{self.__class__.__name__} ({self.identifier} {parameters} {inherits_type} {decl_body})'

class InheritsType(Node):
    def __init__(self, identifier, parameters=None):
        super().__init__()
        self.identifier = identifier
        self.parameters = parameters
        
    def print_visitor(self, visitor):
       parameters = [visitor.visit(pr) for pr in self.parameters] if self.parameters != None else None
       return f'{self.__class__.__name__} ({self.identifier}, {parameters})'

class TypeInstanciation(Node):
    def __init__(self, identifier, arguments = []):
        super().__init__()
        self.identifier = identifier
        self.arguments = arguments
    
    def print_visitor(self, visitor):
       arguments = [visitor.visit(ar) for ar in self.arguments]
       return f'{self.__class__.__name__} ({self.identifier}, {arguments})'

class DeclarationScope(Node):
    def __init__(self, statements):
        super().__init__()
        self.statements = statements
    
    def print_visitor(self, visitor):
        statements = [visitor.visit(st) for st in self.statements]
        return f'{self.__class__.__name__} ({" , ".join(statements)})'
        
class MethodDeclaration(Node):
    def __init__(self, identifier, body, type_anotation = None, parameters=[]):
        super().__init__()
        self.identifier = identifier
        self.type_anotation = type_anotation
        self.parameters = parameters
        self.body = body
    
    def print_visitor(self, visitor):
        parameters = " , ".join([visitor.visit(pr) for pr in self.parameters])
        body = visitor.visit(self.body)
        return f'{self.__class__.__name__} ({self.identifier} {self.type_anotation} {parameters} {body})'

class ProtocolDeclaration(Node):
    def __init__(self, name, body, extends =None):
        super().__init__()
        self.name = name
        self.extends = extends
        self.body = body
        
    def print_visitor(self, visitor):
        body = " , ".join([visitor.visit(pr) for pr in self.body])
        return f'{self.__class__.__name__} ({self.name} {self.extends} {body})'

class VirtualMethod(Node):
    def __init__(self, method_name, type_annotation, parameters=None):
        super().__init__()
        self.method_name = method_name
        self.parameters = parameters
        self.type_annotation = type_annotation

    def print_visitor(self, visitor):
        parameters = None if self.parameters == None else " , ".join([visitor.visit(pr) for pr in self.parameters])
        return f'{self.__class__.__name__} ({self.method_name} {self.type_annotation} {parameters})'

class VectorRangeDeclaration(Node):

    def __init__(self, range):
        super().__init__()
        self.range = range

    def print_visitor(self, visitor):
        range = " , ".join(
            [visitor.visit(pr) for pr in self.range])
        return f'{self.__class__.__name__} ({range})'

class VectorExpressionDeclaration(Node):

    def __init__(self, expression, identifier, rangeexpression):
        super().__init__()
        self.expression = expression
        self.identifier = identifier
        self.rangeexpression = rangeexpression

    def print_visitor(self, visitor):
        expression = visitor.visit(self.expression)
        identifier = visitor.visit(self.identifier)
        rangeexpression = visitor.visit(self.rangeexpression)
        return f'{self.__class__.__name__} ({expression} {identifier} { rangeexpression})'

class HulkPrintVisitor(object):
    
    tabs = -1

    def __init__(self):
        super().__init__()

    @visitor.on('node')
    def visit(self, node, tabs):
        pass

    @visitor.when(Node)
    def visit(self, node):
        self.tabs = self.tabs + 1 
        inter = '\\__ ' if self.tabs > 0 else ''
        result = '\n' + '\t' * self.tabs + inter + node.print_visitor(self)
        self.tabs = self.tabs - 1
        return result

