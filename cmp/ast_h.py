from sly.ast import *

#S' -> program
class S:
    def __init__(self,program):
        self.program = program
# program -> program_decl_list 
# program_decl_list -> empty
# program_decl_list -> program_level_decl program_decl_list
# program_decl_list -> inst_wrapper
class Program(AST):
    def __init__(self,declarations):
        self.declarations = declarations
class Declaration(AST):
    pass

# inst_wrapper -> inst SEMICOLON
# inst_wrapper -> inst
class Inst_Wrapper(Declaration):
    def _init_(self,instrucion):
        self.instrucion = instrucion

class Instruction(AST):
    pass
#inst -> expression
class Expression(Instruction):
    pass        

#expression -> aritmetic_operation
# aritmetic_operation -> term
class Aritmetic_Op(Expression):
    def _init_(self,term,aritmetic_op):
        self.term = term
        self.aritmetic_op = aritmetic_op
# aritmetic_operation -> term MINUS aritmetic_operation  
class Sub(Aritmetic_Op):
    def _init_(self,term,aritmetic_op):
        super()._init_(term,aritmetic_op)
# aritmetic_operation -> term PLUS aritmetic_operation 
class Add(Aritmetic_Op):
    def _init_(self,term,aritmetic_op):
        super()._init_(term,aritmetic_op)
# term -> factor
class Term(AST):
    def _init_(self,factor):
        self.factor = factor
# term -> factor MODULE term 
class Mod(Term):
    def _init_(self,factor,term):
        super()._init_(factor)
        self.term = term 
# term -> factor DIVIDE term  
class Div(Term):
    def _init_(self,factor,term):
        super()._init_(factor)
        self.term = term  
# term -> factor MULTIPLY term  
class Mult(Term):
    def _init_(self,factor,term):
        super()._init_(factor)
        self.term = term
# factor -> base_exponent
class Factor(AST):
    def _init_(self,base_exponent):
        self.base_exponent = base_exponent
# factor -> factor ASTERPOWER base_exponent 
# factor -> factor POWER base_exponent  
class Power(Factor):
    def _init_(self,factor,base_exponent):
        self.factor = factor
        super()._init_(base_exponent)
# base_exponent -> LPAREN aritmetic_operation RPAREN
#  base_exponent -> atom
class Base_exponent(AST):#comprobar
    def _init_(self,value):
        self.value = value

class Atom(AST):
    pass
# atom -> boolean_value
class Boolean(Atom):
    def _init_(self,value: bool ):
        self.value = value
# atom -> STRING
class String(Atom):
    def _init_(self,value: str ):
        self.value = value
# atom -> NUMBER
class Number(Atom): 
    def _init_(self,value):
        self.value= value

class Variable(AST):
    def __init__(self,id:str,instruction,type):
        self.id= id
        if (type is null):
            self.instrucion= instruction#ver
        else : self.instrucion=type(instruction)  




# class Protocol_declaration(Declaration):
#     def __init__()
# class function_declaration(Declaration):
#     def __init__(self,id,arg,body):
#         self.id = id
#         self.arg = arg
#         self.body = body



# class VarDec(Expression):
#     def __init__(self,instrucions,)   

# factor -> base_exponent
# factor -> factor ASTERPOWER base_exponent  
# factor -> factor POWER base_exponent 