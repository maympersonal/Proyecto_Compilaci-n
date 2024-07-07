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
        obj = self.context.create_type("Object")
        Void = self.context.create_type("Void")
        Number = self.context.create_type("Number")
        Boolean = self.context.create_type("Boolean")
        String = self.context.create_type("String")
        self_type = self.context.create_type("Self")
        
        iter = self.context.create_type("Iterable")
        iter.define_method(Method("current",[],[], obj,[]))
        iter.define_method(Method("next",[],[], Boolean,[]))
        
        # object
        obj.define_method(Method('abort',[],[],obj,[]))
        obj.define_method(Method('copy',[],[],self_type,[]))
        obj.define_method(Method('type_name',[],[],String,[]))
        # string
        String.define_method(Method('length',[],[],Number,[]))
        String.define_method(Method('concat',["other"],[String],String,[]))
        String.define_method(Method('substr',["from","to"],[Number,Number],String,[]))
        
        
        Number.set_parent(obj)
        Boolean.set_parent(obj)
        String.set_parent(obj)
        iter.set_parent(obj)
        Void.set_parent(obj)
        self_type.set_parent(obj)
        
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
            type_node = self.context.get_type(node.identifier,self.errors)
            print("*********TypeDeclaration****************")
            print(node.inherits_type)
            type_node.set_parent(self.context.get_type("Object" if node.inherits_type == None else node.inherits_type.identifier ,self.errors))
            print(node.inherits_type)
            for decl in node.decl_body.statements:
                if isinstance(decl,TypeMethodDeclaration):
                    type_node.define_method(self.visit(decl))    
                else:
                    type_node.define_attribute(self.visit(decl))
                
        except SemanticError as e:
            self.errors.append(e)   

            
    @visitor.when(VarUse)
    def visit(self,node):
        print("******* VAR USE ********")
        node.type = self.context.get_type("Object" if node.type == None else node.type,self.errors)

    @visitor.when(TypeVarInit)
    def visit(self,node):
        try:
            type_node = self.context.get_type("Object" if node.type_downcast == None else node.identifier.type,self.errors)
            return Attribute(node.identifier.identifier,type_node)
        except SemanticError as e:
            self.errors.append(e)
            
    @visitor.when(TypeMethodDeclaration)
    def visit(self,node):#ver
        try:
            param_names = []
            param_types = []
            for param in node.parameters:
                print("******* PARAMS ********")
                print(param.identifier)
                param.type = self.context.get_type("Object" if param.type == None else param.type,self.errors)
                param_names.append(param.identifier)
                param_types.append(param.type)
            print("******* type_anotatio ********")
            print(node.type_anotation)
            return_type = self.context.get_type("Object" if node.type_anotation == None else node.type_anotation,self.errors)

            return Method(node.identifier, param_names,param_types, return_type , node.body)
        except SemanticError as e:
            self.errors.append(e)    

    @visitor.when(FunctionDeclaration)
    def visit(self,node):#ver
        try:
            print("++++ FunctionDeclaration ******")
            print("++++ type_anotation ******")
            print( node.type_anotation)
            node.type_anotation = self.context.get_type("Object" if node.type_anotation == None else node.type_anotation,self.errors)
            
            print("++++ Seeing params ******")
            param_names = []
            param_types = []
            if node.parameters != None:
                for param in node.parameters:
                    print(f'++++ Seeing param {param.identifier} ******')
                    print(param.identifier)
                    print(param.type)
                    param.type = self.context.get_type("Object" if param.type == None else param.type,self.errors)
                    print("************DSVSDFVDFSVDFSVDSFVDF")
                    print(param.type)
                    param_names.append(param.identifier)
                    param_types.append(param.type)

            #return_type = node.type_anotation
            print("++++ NODE BODY ******")
            print(node.identifier)
            #self.visit(node.body)
            self.context.create_method(Method(node.identifier, param_names,param_types,node.type_anotation, node.body))
            print("hola,ta pasé por aquí")
        except SemanticError as e:
            self.errors.append(e)    
    
    @visitor.when(ProtocolDeclaration)
    def visit(self,node):#ver
        # try:
        #     type_node = self.context.get_type(node.name,self.errors)
        #     node.extends = self.context.get_type("Object" if param.type == None else param.type,self.errors) 
        #     type_node.set_parent(node.extends)
        #     for decl in node.body:
        #         type_node.define_method(self.visit(decl))
                
        # except SemanticError as e:
        #     self.errors.append(e)    
        try:
            type_node = self.context.get_type(node.name,self.errors)
            print("*********Protocol****************")
            print(node.extends)
            if prohibit := node.extends == 'String' or node.extends == 'String' or node.extends == 'String':
                self.errors.append(f' The protcol {node.name} can not inherit from String,Number or Boolean')

            type_node.set_parent(self.context.get_type("Object" if node.extends == None or prohibit else node.extends ,self.errors))
            for decl in node.body:
                type_node.define_method(self.visit(decl))    

                
        except SemanticError as e:
            self.errors.append(e)   
    
    @visitor.when(ProtocolMethodDeclaration)
    def visit(self,node):
    
        try:
            param_names = []
            param_types = []
            if node.parameters != None:
                for param in node.parameters:
                    print("******* PARAMS ********")
                    print(param.identifier)
                    param.type = self.context.get_type("Object" if param.type == None else param.type,self.errors)
                    param_names.append(param.identifier)
                    param_types.append(param.type)
            print("******* type_anotation ********")
            print(node.type_annotation)
            return_type = self.context.get_type("Object" if node.type_annotation == None else node.type_annotation,self.errors)
            return Method(node.method_name, param_names,param_types, return_type , None)
        except SemanticError as e:
            self.errors.append(e)

class TypeChecker:
    def __init__(self, context, errors=[]):
        self.context = context
        self.current_type = None
        self.current_method = None
        self.errors = errors

        #Agregando las funciones built_in
        self.context.create_type('Global')
        self.context.create_method(Method('print',['x'],[self.context.get_type('String',self.errors)],[self.context.get_type('Void',self.errors)],None))
        self.context.create_method(Method('sin',['x'],[self.context.get_type('Number',self.errors)],[self.context.get_type('Number',self.errors)],None))
        self.context.create_method(Method('cos',['x'],[self.context.get_type('Number',self.errors)],[self.context.get_type('Number',self.errors)],None))
        self.context.create_method(Method('exp',['x'],[self.context.get_type('Number',self.errors)],[self.context.get_type('Number',self.errors)],None))#ver si hay que ponerle cuerpo
        self.context.create_method(Method('log',['base','x'],self.context.get_types(['Number','Number'],self.errors),[self.context.get_type('Number',self.errors)],None))
        self.context.create_method(Method('rand',[],[],[self.context.get_type('Number',self.errors)],None))
       
    
    
    def conforms_to(self, arg, type):
        return(arg.conforms_to(self.context.get_type(type,self.errors)))  

    @visitor.on('node')
    def visit(self, node, scope):
        pass

    @visitor.when(Program)
    def visit(self, node, scope=None):

        
        #agregando las constantes
        scope = SemanticScope()
        scope.define_variable('E',self.context.get_type('Number',self.errors))#arreglar
        scope.define_variable('PI',self.context.get_type('Number',self.errors))#arreglar

        
        # Comprobando correctitud de los métodos de una clase
        for key in self.context.types:

            tYpe = self.context.types[key]
            for method in tYpe.methods:
                newScope = scope.create_child()
                for i in range(0,len(method.param_names)):
                    newScope.define_variable(method.param_names[i],method.param_types[i])
                self.visit(method.body,newScope)
                scope.children.remove(newScope)

        #Comprobando correctitud de los métodos en el contexto

        for key in self.context.methods:
            print("***********  for key in self.context.methods ***********")
            method = self.context.methods[key]
            print(method.name)
            child = scope.create_child()
            for i in range(0,len(method.param_names)):
                child.define_variable(method.param_names[i],method.param_types[i])
            for var in child.locals:
                print(f'{var.name} {var.type}')
            if method.body != None:
    
                retType = self.visit(method.body,child)
                print("******Terminar de evaluar******")
                print(retType)
                if retType.name != method.return_type.name:
                    self.errors.append(SemanticError(f'The function "{method.name}" does not return the type "{method.return_type.name}"'))
            scope.children.remove(child)

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
        if arg1Type.name != 'Number' or arg2Type.name != 'Number':
            return ErrorType()
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
        if arg1Type.name != 'Number' or arg2Type.name != 'Number':
            return ErrorType()
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
        if arg1Type.name != 'Number' or arg2Type.name != 'Number':
            return ErrorType()
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
        if arg1Type.name != 'Number' or arg2Type.name != 'Number':
            return ErrorType()
        return arg1Type 

    
    @visitor.when(Div)
    def visit(self,node,scope):
        
        print('Calculando la división')
        arg1Type = self.visit(node.factor,scope)
        print("arg1Type")
        print(arg1Type)
        if arg1Type.name != 'Number':
            print("hola1")
            self.errors.append(SemanticError('The type of the right member is not Number')) 
        arg2Type = self.visit(node.term,scope)
        print("arg2Type")
        print(node.term)
        print(arg2Type)
        if arg2Type.name != 'Number':
            print("hola2")
            self.errors.append(SemanticError('The type of left member is not Number')) 
        if arg1Type.name != 'Number' or arg2Type.name != 'Number':
            print("hola3")
            return ErrorType()
        print("Todobien")
        print(arg1Type)
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
        if arg1Type.name != 'Number' or arg2Type.name != 'Number':
            return ErrorType()
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
        if arg1Type.name != 'Number' or arg2Type.name != 'Number':
            return ErrorType()
        return arg1Type 

    
    @visitor.when(UnaryBuildInFunction)
    def visit(self,node,scope):
       # print('Printeando un valor')
        

        print('0000000000000000000'+str(node.argument))
        argType = self.visit(node.argument,scope)
        print('0000000000000000000'+str(node))
        if node.func =='print':
            print("****** EN PRINT*******")
            print(argType.name)
            if self.conforms_to(argType, 'Number') or self.conforms_to(argType, 'String') or self.conforms_to(argType, 'Boolean') :
                return self.context.get_type('Void',self.errors)
            self.errors.append(SemanticError('The argument is not valid'))
        else:
            if argType.conforms_to(Number):
                return argType
            self.errors.append(SemanticError('The argument is not a Number')) 
            return ErrorType()

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
        
        param_types = [self.visit(argument,scope) for argument in node.arguments]

        methods = filter_by_name(self.context.methods,node.identifier)
        print("ESTOY AQUI")
        print(param_types)
        print(methods)
        print(self.errors)
        if len(methods) == 0:
            self.errors.append('The method is not defined')
            return ErrorType()
        for key in methods:
            method = methods[key]
            if len(method.param_types) == len(param_types):
                is_not = False
                for i in range(0,len(param_types)):
                    if not(param_types[i].conforms_to(method.param_types[i])):
                        is_not = True   
                if not(is_not):
                    return method.return_type
        self.errors.append('There is no method compatible with those parameters')
        return ErrorType()
          
    @visitor.when(VectorVarUse)
    def visit(self,node,scope):
        self.visit(node.identifier,scope)
        return self.visit(node.index,scope)

    # class VectorExpressionDeclaration(Node):

    # def __init__(self, expression, identifier, rangeexpression):

    @visitor.when(VectorExpressionDeclaration)
    def visit(self,node,scope):
        range = self.visit(node.rangeexpression,scope)
        self.visit(node.identifier,scope)
        node.identifier.type = range
        var = scope.find_variable(node.identifier.identifier)
        var.type = range
        self.visit(node.expression,scope)
        return range

    @visitor.when(VectorRangeDeclaration)
    def visit(self,node,scope):
        elem1Type = self.visit(node.range[0],scope)  
        error = False
        if elem1Type != None:
            for i in range(1,len(node.range)):
                elemType = self.visit(node.range[i],scope)
                if not(elemType.conforms_to(elem1Type)):
                    error = True
                    self.errors.append(f'The type of element {i} is not {elem1Type.name} ')
        if error:
            return ErrorType()
        return elem1Type

    #VarMethod(p.IDENTIFIER, p.function_call)
    @visitor.when(VarMethod)
    def visit(self,node,scope):
        self.visit(node.identifier,scope)
        return self.visit(node.function_call,scope)   

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
        print("***********Scope***************")
        child = scope.create_child()

        for st in node.statements:
            print(st)
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

    @visitor.when(FullConditional)
    def visit(self,node,scope):#arreglar

        conType = self.visit(node.conditional_expression,scope)

        if conType.name != 'Boolean':
            self.errors.append('The conditional expression is not evaluable')
            return TypeError()
        self.visit(node.else_elif_statement,scope)

        for st in node.scope_list:
            result = self.visit(st,scope)   

        return result  
    
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
        print(con2Type)
        if not(isinstance(con2Type,Type)):
            self.errors.append(f'The parameter in not a type')
            return ErrorType()
        return self.context.get_type('Boolean',self.errors)

    @visitor.when(Equal)
    def visit(self,node,scope):
        con1Type = self.visit(node.expr1,scope)
        con2Type = self.visit(node.expr2,scope)
        print("**********Equal*********")
        print(con1Type.name)
        print(con2Type.name)
        eval1 = con1Type.name != 'Number' and con1Type.name != 'String'
        eval2 = con2Type.name != 'Number' and con1Type.name != 'String'
        if  eval1 :
            self.errors.append(SemanticError('The first parameter\'s type in not Number'))
        if  eval2 :
            self.errors.append(SemanticError('The second parameter\'s type in not Number'))   
        if  eval1 or eval2 :
            return ErrorType()

        return self.context.get_type('Boolean',self.errors)
    

    @visitor.when(NotEqual)
    def visit(self,node,scope):
        con1Type = self.visit(node.expr1,scope)
        con2Type = self.visit(node.expr2,scope)

        eval1 = con1Type.name != 'Number' and con1Type.name != 'String'
        eval2 = con2Type.name != 'Number' and con1Type.name != 'String'
        if  eval1 :
            self.errors.append(SemanticError('The first parameter\'s type in not Number'))
        if  eval2 :
            self.errors.append(SemanticError('The second parameter\'s type in not Number'))   
        if  eval1 or eval2 :
            return ErrorType()

        return self.context.get_type('Boolean',self.errors)
    
    @visitor.when(LessEqual)
    def visit(self,node,scope):
        con1Type = self.visit(node.expr1,scope)
        con2Type = self.visit(node.expr2,scope)
        if con1Type.name != 'Number':
            self.errors.append(SemanticError('The first parameter\'s type in not Number'))
        if con2Type.name != 'Number':
            self.errors.append(SemanticError('The second parameter\'s type in not Number'))   
        if  con1Type.name != 'Number' or con2Type.name != 'Number':
            return ErrorType()
        return con1Type

    @visitor.when(GreaterEqual)
    def visit(self,node,scope):
        con1Type = self.visit(node.expr1,scope)
        con2Type = self.visit(node.expr2,scope)
        if con1Type.name != 'Number':
            self.errors.append(SemanticError('The first parameter\'s type in not Number'))
        if con2Type.name != 'Number':
            self.errors.append(SemanticError('The second parameter\'s type in not Number'))   
        if  con1Type.name != 'Number' or con2Type.name != 'Number':
            return ErrorType()
        return con1Type

    @visitor.when(LessThan)
    def visit(self,node,scope):
        con1Type = self.visit(node.expr1,scope)
        con2Type = self.visit(node.expr2,scope)
        if con1Type.name != 'Number':
            self.errors.append(SemanticError('The first parameter\'s type in not Number'))
        if con2Type.name != 'Number':
            self.errors.append(SemanticError('The second parameter\'s type in not Number'))   
        if  con1Type.name != 'Number' or con2Type.name != 'Number':
            return ErrorType()
        return con1Type

    @visitor.when(GreaterThan)
    def visit(self,node,scope):
        con1Type = self.visit(node.expr1,scope)
        con2Type = self.visit(node.expr2,scope)
        if con1Type.name != 'Number':
            self.errors.append(SemanticError('The first parameter\'s type in not Number'))
        if con2Type.name != 'Number':
            self.errors.append(SemanticError('The second parameter\'s type in not Number'))   
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
                print("****** ERRROR ********")
                print(str(varType2))
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
        '''print("*****Buscando variables ******")
        for vari in scope.parent.locals:
            print("padre: " + vari.name)
        for vari in scope.locals:
            print("hijo: " +vari.name)
        print("******************************")'''
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

    @visitor.when(WhileLoop)#comprobar
    def visit(self,node,scope):
        
        child = scope.create_child()
        value = self.visit(node.condition,child)
        print("*******(WhileLoop************")
        print(value)
        return self.visit(node.body,child)

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





