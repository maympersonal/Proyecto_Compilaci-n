class Node():
    pass 

class Program(Node):
    def __init__(self, program_decl_list):
        self.program_decl_list = program_decl_list

class ProgramLevelDecl(Node):
    def __init__(self, decl):
        self.decl = decl


class Intruction(Node):
    pass
class Expression(Intruction):
    pass 
#expression -> aritmetic_operation
class Aritmetic_operation(Expression):
    def __init__(self,term,aritmetic_operation):
        self.term = term
        self.aritmetic_operation = aritmetic_operation


class Add(Aritmetic_operation):
    pass
class Sub(Aritmetic_operation):
    pass


# term -> factor
class Term(Node):
    def __init__(self,factor,term):
        self.factor = factor
        self.term = term 
# term -> factor MODULE term 
class Mod(Term):
    pass
# term -> factor DIVIDE term  
class Div(Term):
    pass 
# term -> factor MULTIPLY term  
class Mult(Term):
    pass
# factor -> base_exponent
class Factor(Node):
    def __init__(self, base_exponent):
        self.base_exponent = base_exponent

# factor -> factor ASTERPOWER base_exponent 
# factor -> factor POWER base_exponent  
class Power(Factor):
    def __init__(self, factor, base_exponent):
        super().__init__(base_exponent)
        self.factor = factor
        
# base_exponent -> LPAREN aritmetic_operation RPAREN
#  base_exponent -> atom
class Base_exponent(Node):
    def __init__(self,value):
        self.value = value


class Declaration(Node):
    pass


class Variable(Node):
    def __init__(self,id:str,instruction,type):
        self.id= id
        if (type is null):
            self.instrucion= instruction#ver
        else : 
            self.instrucion=type(instruction)  


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