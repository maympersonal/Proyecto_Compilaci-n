from cmp.semantic import *
from cmp.visitor import *
from cmp.ast_h import *

shownode = HulkPrintVisitor()

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
        self.context.create_type("Object")
        self.context.create_type("Void")
        self.context.create_type("Number")
        self.context.create_type("Boolean")
        self.context.create_type("String")
        return self.context  

    @visitor.when(TypeDeclaration)
    def visit(self, node):
        try :
            # self.context.get_type(node.identifier)
            # self.errors.append(f'You are trying to declarate Type "{node.identifier}" that is already defined.')
            self.context.create_type(node.identifier)
        except SemanticError as e:
            self.errors.append(e)
            
    @visitor.when(ProtocolDeclaration)
    def visit(self, node):
        try :
            # self.context.get_type(node.identifier)
            # self.errors.append(f'You are trying to declarate Type "{node.identifier}" that is already defined.')
            self.context.create_type(node.name)
        except SemanticError as e:
            self.errors.append(e)
    
    
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
            type_node = self.context.get_type(node.identifier)#ver
            type_node.set_parent(self.context.get_type(node.inherits_type.identifier) if node.inherits_type != None else self.context.get_type("Object"))
            for decl in node.decl_body.statements:
                if decl is TypeMethodDeclaration:
                    type_node.define_method(self.visit(decl))    
                else:
                    type_node.define_attribute(self.visit(decl))
                
        except SemanticError as e:
            self.errors.append(e)   

    @visitor.when(TypeVarInit)
    def visit(self,node):
            try:
                type_node = self.context.get_type(node.identifier.type if node.type_downcast != None else "Object")
                return Attribute(node.identifier.identifier,type_node)
            except SemanticError as e:
                self.errors.append(e)
            
    @visitor.when(TypeMethodDeclaration)
    def visit(self,node):#ver
        try:
            param_names = []
            param_types = []
            for param in node.parameters:
                param_names.append(param.identifier)
                param_types.append(self.context.get_type(param.type if param.type != None else "Object"))

            return_type = self.context.get_type(node.type_anotation if node.type_anotation != None else "Object")

            return Method(node.identifier, param_names,param_types,return_type , node.body)
        except SemanticError as e:
            self.errors.append(e)    

    @visitor.when(ProtocolDeclaration)
    def visit(self,node):#ver
        try:
            type_node = self.context.get_type(node.name)#ver
            type_node.set_parent(self.context.get_type(node.extends) if node.extends != None else self.context.get_type("Object"))
            for decl in node.body:
                type_node.define_method(self.visit(decl))
                
        except SemanticError as e:
            self.errors.append(e)    
    
    @visitor.when(ProtocolMethodDeclaration)
    def visit(self,node):#ver
        try:
            param_names = []
            param_types = []
            for param in node.parameters:
                param_names.append(param.identifier)
                param_types.append(self.context.get_type(param.type if param.type != None else "Object"))

            return_type = self.context.get_type(node.type_annotation if node.type_annotation != None else "Object")

            return Method(node.method_name, param_names,param_types,return_type , None)
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
        self.context.create_type('Global')
        self.context.create_method(Method('print',['x'],['String'],'Void',[]))
        self.context.create_method(Method('sin',['x'],['Number'],'Number',[]))
        self.context.create_method(Method('cos',['x'],['Number'],'Number',[]))
        self.context.create_method(Method('exp',['x'],['Number'],'Number',[]))#ver si hay que ponerle cuerpo
        self.context.create_method(Method('log',['base','x'],['Number','Number'],'Number',[]))
        self.context.create_method(Method('rand',[],[],'Number',[]))

        scope = SemanticScope()
        scope.define_variable('E','Number')
        scope.define_variable('PI','Number')

        for declaration in node.program_decl_list:
            self.visit(declaration, scope)
        return scope

    @visitor.when(BinaryBuildInFunction)
    def visit(self,node,scope):
        arg1Type = self.visit(node.argument1,scope)
        if arg1Type.name != 'Number':
            self.errors.append(SemanticError(f'The type of the base is not Number')) 
        arg2Type = self.visit(node.argument2,scope)
        if arg2Type.name != 'Number':
            self.errors.append(SemanticError(f'The type of x is not Number')) 
        if arg1Type.name == 'Number' and arg2Type.name == 'Number':
            return arg1Type 

    @visitor.when(Add)
    def visit(self,node,scope):
        arg1Type = self.visit(node.term,scope)
        print( arg1Type)
        if arg1Type.name != 'Number':
            self.errors.append(SemanticError('The type of the right member is not Number')) 
        arg2Type = self.visit(node.aritmetic_operation,scope)
        print( arg2Type)
        if arg2Type.name != 'Number':
            self.errors.append(SemanticError('The type of left member is not Number')) 
        if arg1Type.name == 'Number' and arg2Type.name == 'Number':
            return arg1Type 

    @visitor.when(Sub)
    def visit(self,node,scope):
        arg1Type = self.visit(node.term,scope)
        if arg1Type.name != 'Number':
            self.errors.append(SemanticError('The type of the right member is not Number')) 
        arg2Type = self.visit(node.aritmetic_operation,scope)
        if arg2Type.name != 'Number':
            self.errors.append(SemanticError('The type of left member is not Number')) 
        if arg1Type.name == 'Number' and arg2Type.name == 'Number':
            return arg1Type 

    @visitor.when(Mult)
    def visit(self,node,scope):
        arg1Type = self.visit(node.factor,scope)
        if arg1Type.name != 'Number':
            self.errors.append(SemanticError('The type of the right member is not Number')) 
        arg2Type = self.visit(node.term,scope)
        if arg2Type.name != 'Number':
            self.errors.append(SemanticError('The type of left member is not Number')) 
        if arg1Type.name == 'Number' and arg2Type.name == 'Number':
            return arg1Type 
    
    @visitor.when(Div)
    def visit(self,node,scope):
        arg1Type = self.visit(node.factor,scope)
        if arg1Type.name != 'Number':
            self.errors.append(SemanticError('The type of the right member is not Number')) 
        arg2Type = self.visit(node.term,scope)
        if arg2Type.name != 'Number':
            self.errors.append(SemanticError('The type of left member is not Number')) 
        if arg1Type.name == 'Number' and arg2Type.name == 'Number':
            return arg1Type 

    @visitor.when(Mod)
    def visit(self,node,scope):
        arg1Type = self.visit(node.factor,scope)
        if arg1Type.name != 'Number':
            self.errors.append(SemanticError('The type of the right member is not Number')) 
        arg2Type = self.visit(node.term,scope)
        if arg2Type.name != 'Number':
            self.errors.append(SemanticError('The type of left member is not Number')) 
        if arg1Type.name == 'Number' and arg2Type.name == 'Number':
            return arg1Type 

    @visitor.when(Power)
    def visit(self,node,scope): 
        arg1Type = self.visit(node.factor,scope)
        if arg1Type.name != 'Number':
            self.errors.append(SemanticError('The type of the base is not Number')) 
        arg2Type = self.visit(node.base_exponent,scope)
        if arg2Type.name != 'Number':
            self.errors.append(SemanticError('The type of the exponent is not Number')) 
        if arg1Type.name == 'Number' and arg2Type.name == 'Number':
            return arg1Type 
    
    @visitor.when(UnaryBuildInFunction)
    def visit(self,node,scope):
        print(node)
        argType = self.visit(node.argument,scope)
        if node.func =='print':
            if argType.name == 'Number' or argType.name == 'String' or argType.name == 'Boolean' :
                return Type('Void')
            self.errors.append(SemanticError('The argument is not valid')) #ver que pongo XD
        else:
            if argType.name == 'Number':
                return argType
            self.errors.append(SemanticError('The argument is not a Number')) 

    @visitor.when(NoParamBuildInFunction)
    def visit(self,node,scope):
        return Type('Number')

    @visitor.when(Number)
    def visit(self,node,scope):
        return Type('Number')
    @visitor.when(String)
    def visit(self,node,scope):
        return Type('String')


    @visitor.when(FunctionCall)#terminar luego
    def visit(self,node,scope):
        try:
            param_types = [self.visit(argument) for argument in node.arguments]#arreglar
            method = self.context.get_method(node.identifier,param_types)
            child = scope.create_child()
            for i in range(0,len(param_types)):
                child.define_variable(method.param_names[i],param_types[i])
            if self.visit(method.body,child).conforms_to(Type(method.return_type)):
                return Type(method.return_type)
            else:
                self.errors.append(f'The body don\'t retur the correct return_type')
        except SemanticError as e:
            self.errors.append(e)

    @visitor.when(TypeMethodDeclaration)
    def visit(self,node,scope):
        try:
            param_names, params_types = zip[node.parameters] #ver si hace falta *node.parameters o sirve sin *
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

  
    