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
        obj = self.context.create_type("Object")
        self.context.create_type("Void")
        self.context.create_type("Number")
        self.context.create_type("Boolean")
        self.context.create_type("String")
        iter = self.context.create_type("Iterable")
        iter.define_method(Method("current",[],[], obj,[]))
        iter.define_method(Method("next",[],[], obj,[]))
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
    def visit(self,node):
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
            print("******** AQUI **********")
            print(declaration)
            self.visit(declaration, scope)
        return scope

    @visitor.when(BinaryBuildInFunction)
    def visit(self,node,scope):
        print('Calculando el logaritmo')
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
        print('Calculando la suma')
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
        print('Calculando la resta')
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
        print('Calculando la multiplicación')
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
        
        print('Calculando la división')
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
        
        print('Calculando el módulo')
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
        print('Calculando una potencia')
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
        print('Printeando un valor')
        print('0000000000000000000'+str(node.argument))
        argType = self.visit(node.argument,scope)
        print('0000000000000000000'+str(node))
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
        print('Obteniendo un valor random')
        return Type('Number')

    @visitor.when(BuildInConst)
    def visit(self,node,scope):
        print('Obteniendo una constante')
        return Type('Number')

    @visitor.when(FunctionCall)
    def visit(self,node,scope):
        
        param_types = [self.visit(argument) for argument in node.arguments]
        method = self.context.semantic_get_method(node.identifier,param_types)
        if method is None:
            self.errors.append('The method is not defined')

    # @visitor.when(VectorRangeDeclaration)
    # def visit(self,node,scope):
    #     elemType = self.visit(node.range[0],scope)
    #     if elemType != None or not(elemType is ErrorType):
    #         for i in range(1,node)

    # @visitor.when(VectorRangeDeclaration)
    # def visit(self,node,scope):
    #     elemType = self.visit(node.range[0],scope)
    #     if elemType != None or not(elemType is ErrorType):
    #         for i in range(1,node)
                 
    
        
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
        child = scope.create_child()

        for st in node.statements:
            result = self.visit(st,child)
        return result
    

    @visitor.when(ForLoop)#comprobar
    def visit(self,node,scope):

        child = scope.create_child()
        expType = self.visit(node.expression,child)
        varType = self.visit(node.identifier,child)
        var = child.find_variable(node.identifier.identifier)
        var.type = expType
        node.identifier.type = expType
        return self.visit(node.body,child)
   
    @visitor.when(VarDeclaration)
    def visit(self,node,scope):
        child = scope.create_child()
        for var in node.var_init_list:
            self.visit(var,child)
        return self.visit(node.body,child)

    @visitor.when(InlineConditional)
    def visit(self,node,scope):#arreglar

        conType = self.visit(node.conditional_expression,scope)

        if conType.name != 'Boolean':
            self.errors.append('The conditional expression is not evaluable')
            return TypeError()
        self.visit(node.else_elif_statement,scope)

        return self.visit(node.expression,scope)
        
    
    @visitor.when(Not)
    def visit(self,node,scope):
        conType = self.visit(node.condition,scope)
        if conType.name == 'Boolean':
            return conType
        else:
            scope.errors.append(SemanticError('The type in not Boolean'))
            return ErrorType()

    ''' def __init__(self, condition, conditional_expression):'''

    @visitor.when(And)
    def visit(self,node,scope):
        con1Type = self.visit(node.condition,scope)
        con2Type = self.visit(node.conditional_expression,scope)
        if con1Type.name != 'Boolean':
            scope.errors.append(SemanticError('The first parameter\'s type in not Boolean'))
        if con2Type.name != 'Boolean':
            scope.errors.append(SemanticError('The second parameter\'s type in not Boolean'))   
        if  con1Type.name != 'Boolean' or con2Type.name != 'Boolean':
            return ErrorType()
        return con1Type

    @visitor.when(Or)
    def visit(self,node,scope):
        con1Type = self.visit(node.condition,scope)
        con2Type = self.visit(node.conditional_expression,scope)
        if con1Type.name != 'Boolean':
            scope.errors.append(SemanticError('The first parameter\'s type in not Boolean'))
        if con2Type.name != 'Boolean':
            scope.errors.append(SemanticError('The second parameter\'s type in not Boolean'))   
        if  con1Type.name != 'Boolean' or con2Type.name != 'Boolean':
            return ErrorType()
        return con1Type
    
    @visitor.when(Is)
    def visit(self,node,scope):
        con1Type = self.visit(node.condition,scope)
        con2Type = self.visit(node.conditional_expression,scope)

    @visitor.when(Equal)
    def visit(self,node,scope):
        con1Type = self.visit(node.expr1,scope)
        con2Type = self.visit(node.expr2,scope)

        eval1 = con1Type.name != 'Number' or con1Type.name != 'String'
        eval2 = con2Type.name != 'Number' or con1Type.name != 'String'
        if  eval1 :
            scope.errors.append(SemanticError('The first parameter\'s type in not Number'))
        if  eval2 :
            scope.errors.append(SemanticError('The second parameter\'s type in not Number'))   
        if  eval1 or eval2 :
            return ErrorType()

        return self.context.get_type('Boolean',self.errors)
    

    @visitor.when(NotEqual)
    def visit(self,node,scope):
        con1Type = self.visit(node.expr1,scope)
        con2Type = self.visit(node.expr2,scope)

        eval1 = con1Type.name != 'Number' or con1Type.name != 'String'
        eval2 = con2Type.name != 'Number' or con1Type.name != 'String'
        if  eval1 :
            scope.errors.append(SemanticError('The first parameter\'s type in not Number'))
        if  eval2 :
            scope.errors.append(SemanticError('The second parameter\'s type in not Number'))   
        if  eval1 or eval2 :
            return ErrorType()

        return self.context.get_type('Boolean',self.errors)
    
    @visitor.when(LessEqual)
    def visit(self,node,scope):
        con1Type = self.visit(node.expr1,scope)
        con2Type = self.visit(node.expr2,scope)
        if con1Type.name != 'Number':
            scope.errors.append(SemanticError('The first parameter\'s type in not Number'))
        if con2Type.name != 'Number':
            scope.errors.append(SemanticError('The second parameter\'s type in not Number'))   
        if  con1Type.name != 'Number' or con2Type.name != 'Number':
            return ErrorType()
        return con1Type

    @visitor.when(GreaterEqual)
    def visit(self,node,scope):
        con1Type = self.visit(node.expr1,scope)
        con2Type = self.visit(node.expr2,scope)
        if con1Type.name != 'Number':
            scope.errors.append(SemanticError('The first parameter\'s type in not Number'))
        if con2Type.name != 'Number':
            scope.errors.append(SemanticError('The second parameter\'s type in not Number'))   
        if  con1Type.name != 'Number' or con2Type.name != 'Number':
            return ErrorType()
        return con1Type

    @visitor.when(LessThan)
    def visit(self,node,scope):
        con1Type = self.visit(node.expr1,scope)
        con2Type = self.visit(node.expr2,scope)
        if con1Type.name != 'Number':
            scope.errors.append(SemanticError('The first parameter\'s type in not Number'))
        if con2Type.name != 'Number':
            scope.errors.append(SemanticError('The second parameter\'s type in not Number'))   
        if  con1Type.name != 'Number' or con2Type.name != 'Number':
            return ErrorType()
        return con1Type

    @visitor.when(GreaterThan)
    def visit(self,node,scope):
        con1Type = self.visit(node.expr1,scope)
        con2Type = self.visit(node.expr2,scope)
        if con1Type.name != 'Number':
            scope.errors.append(SemanticError('The first parameter\'s type in not Number'))
        if con2Type.name != 'Number':
            scope.errors.append(SemanticError('The second parameter\'s type in not Number'))   
        if  con1Type.name != 'Number' or con2Type.name != 'Number':
            return ErrorType()
        return con1Type

    @visitor.when(TypeInstanciation)
    def visit(self,node,scope):
        return self.context.get_type(node.identifier,self.errors)

    @visitor.when(VarInit)
    def visit(self,node,scope):
        print('inicializando una variable')
        varType1 = self.visit(node.identifier,scope)
        varType2 = self.visit(node.expression,scope)
        print(varType2) 
        print("************")
        print(varType1.name)
        print(node.identifier.type)
        
        print("tipo de 2:" + str(varType2))
        # print(node.type_downcast)
        # print(node)
        # print("************")
        if node.type_downcast == None:
            if (varType1.name == "Object"):
                node.type_downcast = self.context.get_type(varType2.name,self.errors)
                print(node.identifier.identifier)   
                var = scope.find_variable(node.identifier.identifier)
                var.type = self.context.get_type(varType2.name,self.errors)
                print(f'"*********{var.name}" ----"{var.type}"')
                return varType2
            elif (varType2.conforms_to(varType1)):
                node.type_downcast = self.context.get_type(varType2.name,self.errors)
                return varType1
            else: 
                self.errors(f'The value\'s type in not "{varType1.name}" ')
                return ErrorType()

        elif not(varType2.conforms_to(self.context.get_type(node.type_downcast,self.errors))):
            self.errors(f'The value\'s type in not "{node.type_downcast}" ')
            return ErrorType()
        else:
            var = scope.find_variable(node.identifier.identifier)
            node.type_downcast = self.context.get_type(node.type_downcast,self.errors)
            var.type = node.type_downcast
            return node.type_downcast

        '''if node.type_downcast == None:
            node.identifier.type = varType
            #node.identifier.type = node.expression
            node.type_downcast = varType
            var = scope.define_variable(node.identifier.identifier,varType)
            print(f'"{var.name}" ----"{var.type}"')
            for a in scope.locals:
                print("****" + a.name)
        elif not(varType.conforms_to(node.type_downcast)):
            self.errors.append(f'The type of the value of the parameter "{node.identifier.identifier}" is not "{node.type_downcast}"')
            newType = ErrorType()
            scope.define_variable(node.identifier.identifier,newType)
            return newType
        node.type_downcast = varType
        scope.define_variable(node.identifier.identifier,node.type_downcast)
        return node.type_downcast'''

    @visitor.when(VarUse)
    def visit(self,node,scope):
        print("***** VARUSE ******")
        print(node.identifier)
        # print(node.type)
        print("*****Buscando variables ******")
        for vari in scope.parent.locals:
            print("padre: " + vari.name)
        for vari in scope.locals:
            print("hijo: " +vari.name)
        print("******************************")
        var = scope.find_variable(node.identifier)
        
        if var != None:
            print("encontrada: " + var.name)
        if var == None:
            node.type = self.context.get_type("Object",self.errors)
            scope.define_variable(node.identifier, node.type)
            print("agregada: " + node.identifier)
            return node.type
            '''self.errors.append(f'The variable "{node.identifier}" is not defined')
            return ErrorType()'''
        else:    
            node.type = var.type
            return var.type  

    @visitor.when(Concat)
    def visit(self,node,scope):
        arg1Type = self.visit(node.atom,scope)
        arg2Type = self.visit(node.expression,scope)


        print("****** CONCAT *******")
        print(arg1Type)
        print(arg2Type)

        if (arg1Type.name == 'Number' or  arg1Type.name == 'String')  and not(arg2Type.name == 'Number' or  arg2Type.name == 'String'):
                self.errors.append(SemanticError('The type second parameter in not string or number'))
                return ErrorType()
        elif arg1Type.name == 'Number'  and not(arg2Type.name == 'String') :
                self.errors.append(SemanticError('You can not concat two numbers'))
                return ErrorType()
        elif not(arg1Type.name == 'Number' or  arg1Type.name == 'String') and  (arg2Type.name == 'Number' or  arg2Type.name == 'String') : 
                self.errors.append(SemanticError('The type first parameter in not string or number'))
                return ErrorType()
        else:
            return self.context.get_type('String',self.errors)
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
        node.type_downcast = self.context.get_type('Number',self.errors)
        return node.type_downcast
    @visitor.when(String)
    def visit(self,node,scope):
        print('La variable es un string')
        node.type_downcast = self.context.get_type('String',self.errors)
        return node.type_downcast

    @visitor.when(Boolean)
    def visit(self,node,scope):
        print('La variable es un booleano')
        node.type_downcast = self.context.get_type('Boolean',self.errors)
        return node.type_downcast


  #Herramientas
    def Method_Validation(method,visitor):
        Scope



