from cmp.semantic import *
from cmp.visitor import *
from cmp.ast_h import *

class TypeCollector(object):
    def __init__(self, errors=[]):
        self.context = None
        self.errors = errors
    
    @visitor.on('node')
    def visit(self, node):
        pass
    
    @visitor.when(Program)
    def visit(self,node):
        self.context = Context()
        for declaration in node.program_decl_list:
            self.visit(declaration)
        self.context.create_type(Number)
        self.context.create_type(Boolean)
        self.context.create_type(String)
        return self.context  

    @visitor.when(TypeDeclaration)
    def visit(self, node):
        try :
            # self.context.get_type(node.identifier)
            # self.errors.append(f'You are trying to declarate Type "{node.identifier}" that is already defined.')
            self.context.create_type(node.identifier)
        except SemanticError as a:
            self.errors.append(a)
            

    
    
class TypeBuilder:
    def __init__(self, context, errors=[]):
        self.context = context
        self.current_type = None
        self.errors = errors
    
    @visitor.on('node')
    def visit(self, node):
        pass
    
    @visitor.when(Program)
    def visit(self, node):
        for declaration in node.program_decl_list:
            self.visit(declaration)
        
    @visitor.when(TypeDeclaration)
    def visit(self,node):#ver la parte de herencia
        try:
            newType = self.context.get_type(node.identifier)#ver

            if node.inherits_type != None:
                father = self.context.get_type(node.inherits_type.identifier)#ver
                newType.set_parent(father)

            for decl in node.body:
                declaration = self.visit(decl)
                if declaration is Attribute:
                    newType.define_attribute(declaration)
                else:
                    newType.define_method(declaration)

        except SemanticError as e:
            self.errors.append(e)

    @visitor.when(VarInit)
    def visit(self,node):
        try:
            self.context.get_type(node.type_downcast)
            return Attribute(node.name,node.type_downcast)
        except SemanticError as e:
            self.errors.append(e)
            
    @visitor.when(MethodDeclaration)
    def visit(self,node):#ver
        try:
            self.context.get_type(node.type_anotation)
            param_names,param_types = zip(*node.parameters)
            for param_type in param_types:
                self.context.get_type(param_type)
            return Method(node.name, param_names,param_types,node.type_anotation)
        except SemanticError as e:
            self.errors.append(e)

        
        

class TypeChecker:
    def __init__(self, context, errors=[]):
        self.context = context
        self.current_type = None
        self.current_method = None
        self.errors = errors

    @visitor.on('node')
    def visit(self, node, scope):
        pass

    @visitor.when(Program)
    def visit(self, node, scope=None):
        scope = Scope()
        for declaration in node.program_decl_list:
            self.visit(declaration, scope.create_child())
        return scope

    @visitor.when(FunctionCall)#terminar luego
    def visit(self,node,scope):
        try:
            method = self.context.get_method(node.identifier,node.arguments)
            for i in range(0,len(node.arguments)):
                if 
        except SemanticError as e:
            self.errors.append(e)

    @visitor.when(MethodDeclaration)
    def visit(self,node,scope):
        try:
            param_names, params_types = zip[*node.parameters]
            method = Method(node.identifier, param_names, params_types, node.type_anotation,node.body)
            self.context.create_method(node)
        except SemanticError as e:
            self.errors.append(e)
    
    # # @visitor.when(BinaryNode)
    # # def visit(self, node, scope):
    # #     attr = RetAttr(node)
    # #     var1= attr[0]
    # #     type1 =self.visit(var1[1],scope)
    # #     var2= attr[1]
    # #     type2 =self.visit(var1[1],scope)
    # #     if type1 is IntType:
    # #         if type1 == type2:
    # #             return type1
    # #         else:
    # #             self.errors.append()#duda
    # #             return ErrorType(IntType)
    # #     else:
    # #             self.errors.append()#duda
    # #             return ErrorType(IntType)
    
    # @visitor.when(Number)
    # def visit(self, node, scope):
    #     if node.value is float:
    #         return IntType()
    #     else:
    #             self.errors.append()#duda
    #             return ErrorType(IntType)

  
    