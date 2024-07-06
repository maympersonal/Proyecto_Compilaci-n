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
        object_type = self.context.create_type("Object")
        void_type = self.context.create_type("Void")
        number_type = self.context.create_type("Number")
        boolean_type = self.context.create_type("Boolean")
        string_type = self.context.create_type("String")
        self_type = self.context.create_type("Self")
        
        # métodos de los tipos
        # object
        object_type.define_method(Method('abort',[],[],object_type,[]))
        object_type.define_method(Method('copy',[],[],self_type,[]))
        object_type.define_method(Method('type_name',[],[],string_type,[]))
        # string
        string_type.define_method(Method('length',[],[],number_type,[]))
        string_type.define_method(Method('concat',["other"],[string_type],string_type,[]))
        string_type.define_method(Method('substr',["from","to"],[number_type,number_type],string_type,[]))
        
        # fin métodos
                
        # jerarquia de tipos 
        for typex in self.context.types.values():
            if typex != object_type:
                typex.set_parent(object_type)
        # fin jerarquia de tipos
        
        for declaration in node.program_decl_list:
            self.visit(declaration)
            
        return self.context  

    @visitor.when(TypeDeclaration)
    def visit(self, node):
        try :
            self.context.create_type(node.identifier)
        except SemanticError as e:
            self.errors.append(e)
            
    @visitor.when(ProtocolDeclaration)
    def visit(self, node):
        try :
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
            type_node = self.context.get_type(node.identifier,self.errors)#ver
            type_node.set_parent(self.context.get_type(node.inherits_type.identifier,self.errors) if node.inherits_type != None else self.context.get_type("Object",self.errors))
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
                type_node = self.context.get_type(node.identifier.type if node.type_downcast != None else "Object",self.errors)
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
                param_types.append(self.context.get_type(param.type if param.type != None else "Object",self.errors))

            return_type = self.context.get_type(node.type_anotation if node.type_anotation != None else "Object",self.errors)

            return Method(node.identifier, param_names,param_types,return_type , node.body)
        except SemanticError as e:
            self.errors.append(e)    

    @visitor.when(ProtocolDeclaration)
    def visit(self,node):#ver
        try:
            type_node = self.context.get_type(node.name,self.errors)#ver
            type_node.set_parent(self.context.get_type(node.extends,self.errors) if node.extends != None else self.context.get_type("Object"),self.errors)
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
                param_types.append(self.context.get_type(param.type if param.type != None else "Object",self.errors))

            return_type = self.context.get_type(node.type_annotation if node.type_annotation != None else "Object",self.errors)

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

        #Agregando las funciones built_in
        self.context.create_type('Global')
        self.context.create_method(Method('print',['x'],[self.context.get_type('String',self.errors)],[self.context.get_type('Void',self.errors)],[]))
        self.context.create_method(Method('sin',['x'],[self.context.get_type('Number',self.errors)],[self.context.get_type('Number',self.errors)],[]))
        self.context.create_method(Method('cos',['x'],[self.context.get_type('Number',self.errors)],[self.context.get_type('Number',self.errors)],[]))
        self.context.create_method(Method('exp',['x'],[self.context.get_type('Number',self.errors)],[self.context.get_type('Number',self.errors)],[]))#ver si hay que ponerle cuerpo
        self.context.create_method(Method('log',['base','x'],self.context.get_types(['Number','Number'],self.errors),[self.context.get_type('Number',self.errors)],[]))
        self.context.create_method(Method('rand',[],[],[self.context.get_type('Number',self.errors)],[]))

        #agregando las constantes
        scope = SemanticScope()
        scope.define_variable('E','Number')
        scope.define_variable('PI','Number')

        # Comprobando correctitud de los métodos de una clase
        for key in self.context.types:

            tYpe = self.context.types[key]
            for method in tYpe.methods:
                newScope = scope.create_child()
                for i in range(0,len(method.param_names)):
                    newScope.define_variable(method.param_names[i],method.param_types[i])
                self.visit(method.body,newScope)
                scope.children.remove(newScope)


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


    @visitor.when(FunctionCall)
    def visit(self,node,scope):
        
        param_types = [self.visit(argument) for argument in node.arguments]
        method = self.context.semantic_get_method(node.identifier,param_types)
        if method is None:
            self.errors.append('The method is not defined')
        
    # @visitor.when(TypeMethodDeclaration)
    # def visit(self,node,scope):
    #     try:
    #         param_names, param_types = zip[node.parameters] #ver si hace falta *node.parameters o sirve sin *
    #         method = Method(node.identifier, param_names, param_types, node.type_anotation,node.body)
    #         self.context.create_method(node)
    #     except SemanticError as e:
    #         self.errors.append(e)
    # newScope = scope.create_child()
    #             for i in range(0,len(method.param_names)):
    #                 newScope.define_variable(method.param_names[i],method.param_types[i])
    #             self.visit(method.body,newScope)
    #             scope.children.remove(newScope)

    @visitor.when(Scope)
    def visit(self,node,scope):
        for i in (0,len(node.statements)-1):
            self.visit(node.statements[i],scope)
        return self.visit(node.statements[len(node.statements)],scope)

    @visitor.when(VarDeclaration)#comprobar
    def visit(self,node,scope):
        for var in node.var_init_list:
            expType = self.visit(var.expression,scope)
            if var.type_downcast ==None:
                scope.define_variable(var.identifier,expType)
            else:
                downcast = self.context.get_type(var.type_downcast)
                if expType.conforms_to(downcast):
                    scope.define_variable(var.identifier,downcast)
                else:
                    self.errors.append(f'The param "{var.identifier}" can not downcast as "{downcast.name}"')
                    scope.define_variable(var.identifier,ErrorType(downcast.name))
        return self.visit(node.body)

    @visitor.when(ForLoop)#comprobar
    def visit(self,node,scope):
        varType = self.visit(node.expression)
        child = scope.create_child()
        child.define_variable(node.identifier,varType)
        return self.visit(node.body)

    # @visitor.when(WhileLoop)#comprobar
    # def visit(self,node,scope):
    #     child = scope.create_child()
    #     value = self.visit(node.condition,child)
    #     if value[0]:
    #         return self.visit(node.body,child)
    #     else:
    #         return None # ver que ponemos

    @visitor.when(Number)
    def visit(self,node,scope):
        return Type('Number'),node.value

    @visitor.when(String)
    def visit(self,node,scope):
        return Type('String'),node.value

    @visitor.when(Boolean)
    def visit(self,node,scope):
        return Type('Boolean')


  #Herramientas
    def Method_Validation(method,visitor):
        Scope