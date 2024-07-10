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
        #print(f'{node.__class__.__name__}' + str([f"{key}: {value}" for key, value in vars(node).items()]))
        self.context = Context()
        obj = self.context.create_type("Object")
        Void = self.context.create_type("Void")
        Number = self.context.create_type("Number")
        Boolean = self.context.create_type("Boolean")
        String = self.context.create_type("String")
        iter = self.context.create_type("Iterable")
        iter.define_attribute(Attribute("start",obj))
        iter.define_attribute(Attribute("end",obj))
        iter.define_method(Method("current",[],[], obj,[]))
        iter.define_method(Method("next",[],[], Boolean,[]))
        Number.set_parent(obj)
        Boolean.set_parent(obj)
        String.set_parent(obj)
        iter.set_parent(obj)
        for declaration in node.program_decl_list:
            self.visit(declaration)
        
        # object
        obj.define_method(Method('abort',[],[],obj,[]))
        #obj.define_method(Method('copy',[],[],self_type,[]))
        obj.define_method(Method('type_name',[],[],String,[]))

        # string
        String.define_method(Method('length',[],[],Number,[]))
        String.define_method(Method('concat',["other"],[String],String,[]))
        String.define_method(Method('substr',["from","to"],[Number,Number],String,[]))
        return self.context  

    @visitor.when(TypeDeclaration)
    def visit(self, node):
        #print(f'{node.__class__.__name__}' + str([f"{key}: {value}" for key, value in vars(node).items()]))
        try :
            self.context.create_type(node.identifier)
        except SemanticError as e:
            self.errors.append(e)
            
    @visitor.when(ProtocolDeclaration)
    def visit(self, node):
        #print(f'{node.__class__.__name__}' + str([f"{key}: {value}" for key, value in vars(node).items()]))
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
            type_node.set_parent(self.context.get_type("Object" if node.inherits_type == None else node.inherits_type.identifier ,self.errors))
            for decl in node.decl_body.statements:
                if isinstance(decl,TypeMethodDeclaration):
                    type_node.define_method(self.visit(decl))    
                else:
                    type_node.define_attribute(self.visit(decl))
                
        except SemanticError as e:
            self.errors.append(e)   

            
    @visitor.when(VarUse)
    def visit(self,node):
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
                param.type = self.context.get_type("Object" if param.type == None else param.type,self.errors)
                param_names.append(param.identifier)
                param_types.append(param.type)
            return_type = self.context.get_type("Object" if node.type_anotation == None else node.type_anotation,self.errors)

            return Method(node.identifier, param_names,param_types, return_type , node.body)
        except SemanticError as e:
            self.errors.append(e)    

    @visitor.when(FunctionDeclaration)
    def visit(self,node):#ver
        try:
            node.type_anotation = self.context.get_type("Object" if node.type_anotation == None else node.type_anotation,self.errors)
            param_names = []
            param_types = []
            if node.parameters != None:
                for param in node.parameters:
                    param.type = self.context.get_type("Object" if param.type == None else param.type,self.errors)
                    param_names.append(param.identifier)
                    param_types.append(param.type)

            #return_type = node.type_anotation
            self.visit(node.body)
            self.context.create_method(Method(node.identifier, param_names,param_types,node.type_anotation, node.body))
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
                    param.type = self.context.get_type("Object" if param.type == None else param.type,self.errors)
                    param_names.append(param.identifier)
                    param_types.append(param.type)
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
        self.context.create_method(Method('print',['x'],[self.context.get_type('String',self.errors)],self.context.get_type('Void',self.errors),None))
        self.context.create_method(Method('sin',['x'],[self.context.get_type('Number',self.errors)],self.context.get_type('Number',self.errors),None))
        self.context.create_method(Method('cos',['x'],[self.context.get_type('Number',self.errors)],self.context.get_type('Number',self.errors),None))
        self.context.create_method(Method('exp',['x'],[self.context.get_type('Number',self.errors)],self.context.get_type('Number',self.errors),None))#ver si hay que ponerle cuerpo
        self.context.create_method(Method('log',['base','x'],self.context.get_types(['Number','Number'],self.errors),self.context.get_type('Number',self.errors),None))
        self.context.create_method(Method('rand',[],[],self.context.get_type('Number',self.errors),None))
        self.context.create_method(Method('range',['x','y'],self.context.get_types(['Number','Number'],self.errors),self.context.get_type('Iterable',self.errors),None))
        #self.context.create_method(Method('current',[],[],self.context.get_type('Number',self.errors),None))
        #self.context.create_method(Method('next',[],[],self.context.get_type('Boolean',self.errors),None))

        


        self.context.create_type("Main")
    
    def toconforms_to(self, arg, type):
        return(arg.conforms_to(self.context.get_type(type,self.errors)))  

    @visitor.on('node')
    def visit(self, node, scope):
        pass

    @visitor.when(Program)
    def visit(self, node, scope=None):
        print("***** Program *********")
        
        #agregando las constantes
        scope = SemanticScope()
        scope.define_variable('E',self.context.get_type('Number',self.errors))
        scope.define_variable('PI',self.context.get_type('Number',self.errors))

        
        '''# Comprobando correctitud de los métodos de una clase
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
            method = self.context.methods[key]
            child = scope.create_child()
            for i in range(0,len(method.param_names)):
                child.define_variable(method.param_names[i],method.param_types[i])
            if method.body != None:
    
                retType = self.visit(method.body,child)
                if retType.name != method.return_type.name:
                    self.errors.append(SemanticError(f'The function "{method.name}" does not return the type "{method.return_type.name}"'))
            scope.children.remove(child)'''

        for declaration in node.program_decl_list:
            print(declaration)
            self.visit(declaration, scope)
        return scope

    @visitor.when(BinaryBuildInFunction)
    def visit(self,node,scope):
        print("***** BinaryBuildInFunction *********")
        arg1Type = self.visit(node.argument1,scope)
        if arg1Type.name != 'Number':
            self.errors.append(SemanticError(f'The type of the base is not Number')) 
        arg2Type = self.visit(node.argument2,scope)
        if arg2Type.name != 'Number':
            self.errors.append(SemanticError(f'The type of x is not Number')) 
        if arg1Type.name != 'Number' or arg2Type.name != 'Number':
            return ErrorType()
        return self.context.methods[node.func].return_type 


    @visitor.when(Add)
    def visit(self,node,scope):
        print("***** Add *********")
        arg1Type = self.visit(node.term,scope)
        if arg1Type.name != 'Number':
            self.errors.append(SemanticError('The type of the right member is not Number')) 
        arg2Type = self.visit(node.aritmetic_operation,scope)
        if arg2Type.name != 'Number':
            self.errors.append(SemanticError('The type of left member is not Number')) 
        if arg1Type.name != 'Number' or arg2Type.name != 'Number':
            return ErrorType()
        return arg1Type  

    @visitor.when(Sub)
    def visit(self,node,scope):
        print("***** Sub *********")
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
        print("***** Mult *********")
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
        print("***** Div *********")
        arg1Type = self.visit(node.factor,scope)
        if arg1Type.name != 'Number':
            self.errors.append(SemanticError('The type of the right member is not Number')) 
        arg2Type = self.visit(node.term,scope)
        if arg2Type.name != 'Number':
            self.errors.append(SemanticError('The type of left member is not Number')) 
        if arg1Type.name != 'Number' or arg2Type.name != 'Number':
            return ErrorType()
        return arg1Type 


    @visitor.when(Mod)
    def visit(self,node,scope):
        print("***** Mod *********")
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
        print("***** Power *********")
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
        print("***** UnaryBuildInFunction *********")
        argType = self.visit(node.argument,scope)
        if node.func =='print':
            if self.toconforms_to(argType, 'Number') or self.toconforms_to(argType, 'String') or self.toconforms_to(argType, 'Boolean') :
                return self.context.get_type('Void',self.errors)
            self.errors.append(SemanticError('The argument is not valid'))
        else:
            if self.toconforms_to(argType, 'Number'):
                return self.context.get_type('Number',self.errors)
            self.errors.append(SemanticError('The argument is not a Number')) 
            return ErrorType()

    @visitor.when(NoParamBuildInFunction)
    def visit(self,node,scope):
        print("***** NoParamBuildInFunction *********")
        return self.context.get_type('Number',self.errors)

    @visitor.when(BuildInConst)
    def visit(self,node,scope):
        print("***** BuildInConst *********")
        return self.context.get_type('Number',self.errors)

    @visitor.when(FunctionCall)
    def visit(self,node,scope):
        print("***** FunctionCall *********")
        
        param_types = [self.visit(argument,scope) for argument in node.arguments]
        methods = filter_by_name(self.context.methods,node.identifier)
        if len(methods) == 0:
            self.errors.append('The method is not defined')
            return ErrorType()
        for key in methods:
            method = methods[key]
            if len(method.param_types) == len(param_types):
                return method.return_type
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
        print("***** VectorVarUse *********")
        self.visit(node.identifier,scope)
        return self.visit(node.index,scope)

    # class VectorExpressionDeclaration(Node):

    # def __init__(self, expression, identifier, rangeexpression):

    @visitor.when(VectorExpressionDeclaration)
    def visit(self,node,scope):
        print("***** VectorExpressionDeclaration *********")
        range = self.visit(node.rangeexpression,scope)
        self.visit(node.identifier,scope)
        node.identifier.type = range
        var = scope.find_variable(node.identifier.identifier)
        var.type = range
        self.visit(node.expression,scope)
        return range

    @visitor.when(VectorRangeDeclaration)
    def visit(self,node,scope):
        print("***** VectorRangeDeclaration *********")
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
        print("***** Scope *********")
        child = scope.create_child()

        for st in node.statements:
            result = self.visit(st,child)
        
        return result
    

    @visitor.when(ForLoop)#comprobar
    def visit(self,node,scope):
        print("***** ForLoop *********")
        child = scope.create_child()
        expType = self.visit(node.expression,child)
        varType = self.visit(node.identifier,child)
        var = child.find_variable(node.identifier.identifier)
        var.type = expType
        node.identifier.type = expType
        return self.visit(node.body,child)
   
    @visitor.when(VarDeclaration)
    def visit(self,node,scope):
        print("***** VarDeclaration *********")
        child = scope.create_child()
        #child = SemanticScope()
        for var in node.var_init_list:
            print("******AQUI*******")
            print(var.identifier.identifier)
            print(var.identifier.type)
            type = self.context.get_type("Object" if var.identifier.type == None else var.identifier.type,self.errors) 
            scope.define_variable(var.identifier.identifier, type)
        for var in node.var_init_list:
            self.visit(var,child)
        print("***** VarDeclaration despues*********")
        for key in child.locals:
            print(f"{key.name} -------- {key.type}")
        #scope.children.append(child)
        for var in node.var_init_list:
           print(var.type_downcast)
        for key in child.locals:
            print(f"{key.name} -------- {key.type}")
        print(node.body)
        return self.visit(node.body,child)

    @visitor.when(InlineConditional)
    def visit(self,node,scope):#arreglar
        print("***** InlineConditional *********")
        conType = self.visit(node.conditional_expression,scope)
        if conType.name != 'Boolean':
            self.errors.append('The conditional expression is not evaluable')
            return TypeError()
        self.visit(node.else_elif_statement,scope)

        return self.visit(node.expression,scope)

    @visitor.when(FullConditional)
    def visit(self,node,scope):#arreglar
        print("***** FullConditional *********")

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
        print("***** Not *********")
        conType = self.visit(node.condition,scope)
        if conType.name == 'Boolean':
            return conType
        else:
            scope.errors.append(SemanticError('The type in not Boolean'))
            return ErrorType()

    ''' def __init__(self, condition, conditional_expression):'''

    @visitor.when(And)
    def visit(self,node,scope):
        print("***** And *********")
        con1Type = self.visit(node.condition,scope)
        con2Type = self.visit(node.conditional_expression,scope)
        if con1Type.name != 'Boolean':
            self.errors.append(SemanticError('The first parameter\'s type in not Boolean'))
        if con2Type.name != 'Boolean':
            self.errors.append(SemanticError('The second parameter\'s type in not Boolean'))  
        if  con1Type.name != 'Boolean' or con2Type.name != 'Boolean':
            return ErrorType()
        return con1Type

    @visitor.when(Or)
    def visit(self,node,scope):
        print("***** Or *********")
        con1Type = self.visit(node.condition,scope)
        con2Type = self.visit(node.conditional_expression,scope)
        if con1Type.name != 'Boolean':
            self.errors.append(SemanticError('The first parameter\'s type in not Boolean'))
        if con2Type.name != 'Boolean':
            self.errors.append(SemanticError('The second parameter\'s type in not Boolean'))  
        if  con1Type.name != 'Boolean' or con2Type.name != 'Boolean':
            return ErrorType()
        return con1Type
    
    @visitor.when(Is)
    def visit(self,node,scope):
        print("***** Is *********")
        con1Type = self.visit(node.condition,scope)
        con2Type = self.visit(node.conditional_expression,scope)
        if not(isinstance(con2Type,Type)):
            self.errors.append(f'The parameter in not a type')
            return ErrorType()
        return self.context.get_type('Boolean',self.errors)

    @visitor.when(Equal)
    def visit(self,node,scope):
        print("***** Equal *********")
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
    

    @visitor.when(NotEqual)
    def visit(self,node,scope):
        print("***** NotEqual *********")
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
        print("***** LessEqual *********")
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
        print("***** GreaterEqual *********")
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
        print("***** LessThan *********")
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
        print("***** GreaterThan *********")
        con1Type = self.visit(node.expr1,scope)
        con2Type = self.visit(node.expr2,scope)
        if con1Type.name != 'Number':
            self.errors.append(SemanticError('The first parameter\'s type in not Number'))
        if con2Type.name != 'Number':
            self.errors.append(SemanticError('The second parameter\'s type in not Number'))   
        if  con1Type.name != 'Number' or con2Type.name != 'Number':
            return ErrorType()
        return con1Type

    

    @visitor.when(VarInit)
    def visit(self,node,scope):
        print("***** VarInit *********")
        print(node.identifier)
        print(node.expression)
        varType1 = self.visit(node.identifier,scope)
        varType2 = self.visit(node.expression,scope)
        print(varType1)
        print(varType2)
        if node.type_downcast == None:
            if (varType1.name == "Object"):
                node.type_downcast = self.context.get_type(varType2.name,self.errors)
                var = scope.find_variable(node.identifier.identifier)
                var.type = self.context.get_type(varType2.name,self.errors)
                return varType2
            elif (varType2.conforms_to(varType1)):
                node.type_downcast = self.context.get_type(varType2.name,self.errors)
                return varType1
            else: 
                print("varType1.name")
                print(varType1.name)
                #self.errors(f'The value\'s type in not "{str(varType1.name)}" ')
                return ErrorType()

        elif not(varType2.conforms_to(self.context.get_type(node.type_downcast,self.errors))):
            print("type downcast")
            print(node.type_downcast)
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
        print("***** VarUse *********")
        if isinstance(node.identifier, VarAttr):
            print("ENTRE POR VARATTR")
            node.type = self.visit(node.identifier,scope)
            print("retorno")
            print(node.type)
            return node.type
        else:
            var = scope.find_variable(node.identifier)
            print("****var****")
            print(var)
            if var == None:
                print("********")
                print(node.type)
                node.type = self.context.get_type("Object" if node.type == None else node.type if isinstance(node.type,str) else node.type.name,self.errors) 
                scope.define_variable(node.identifier, node.type)
                return node.type
            else:    
                node.type = var.type
                return var.type  

    @visitor.when(Concat)
    def visit(self,node,scope):
        print("***** Concat *********")
        arg1Type = self.visit(node.atom,scope)
        arg2Type = self.visit(node.expression,scope)
        print(arg1Type.name)
        print(arg2Type.name)
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
        print("***** WhileLoop *********")
        
        child = scope.create_child()
        value = self.visit(node.condition,child)
        return self.visit(node.body,child)

    @visitor.when(Number)
    def visit(self,node,scope):
        print("***** Number *********")
        node.type_downcast = self.context.get_type('Number',self.errors)
        return node.type_downcast
    
    @visitor.when(String)
    def visit(self,node,scope):
        print("***** String *********")
        node.type_downcast = self.context.get_type('String',self.errors)
        return node.type_downcast

    @visitor.when(Boolean)
    def visit(self,node,scope):
        print("***** Boolean *********")
        node.type_downcast = self.context.get_type('Boolean',self.errors)
        return node.type_downcast

    '''self.identifier = identifier
    self.parameters = parameters
    self.inherits_type = inherits_type
    self.decl_body = decl_body'''
    '''self.name = name
    self.attributes = []
    self.methods = []
    self.parent = None
    for method in tYpe.methods:
                newScope = scope.create_child()
                for i in range(0,len(method.param_names)):
                    newScope.define_variable(method.param_names[i],method.param_types[i])
                self.visit(method.body,newScope)
                scope.children.remove(newScope)'''
    @visitor.when(TypeDeclaration)
    def visit(self,node, scope):#ver la parte de herencia
        print("***** TypeDeclaration *********")
        type = self.context.get_type(node.identifier,self.errors)
        print(type)
        child = scope.create_child()
        parent = type
        while parent != None:
            for attr in parent.attributes:
                child.define_variable("self."+attr.name,attr.type)
            parent = parent.parent
            if parent == self.context.get_type("Object",self.errors):
                break
            print(parent)
        
        if ( node.parameters != None):
            for parameter in node.parameters:
                print("****** PARAMETROS********")
                parameter.type = self.visit(parameter,child)



        for key in child.locals:
            print(f"{key.name} -------- {key.type}")
                  
        self.visit(node.decl_body,child)
        print("ACTUALIZAR ATRIBUTOS")
        for attr in type.attributes:
            attr.type = child.find_variable("self."+attr.name).type
            print(attr)
            
        scope.children.remove(child)
        print("salida")
        print(type)
        '''child = scope.create_child()
        for parameter in node.parameters:
            self.visit(parameter,child)
        self.visit(node.decl_body,child)'''
        return type
        
        '''type = self.context.get_type(node.identifier,self.errors)
        print(type)
        parent = type
        while parent != None:
            for attr in parent.attributes:
                child.define_variable("self."+attr.name,attr.type)
            parent = parent.parent
        for key in child.locals:
            print(key.name)

        for method in type.methods:
            print(method)
            newScope = child.create_child()
            for i in range(0,len(method.param_names)):
                newScope.define_variable(method.param_names[i],method.param_types[i])
                self.visit(method.body,newScope)
                scope.children.remove(newScope)'''


        

    @visitor.when(TypeInstanciation)
    def visit(self,node,scope):
        print("***** TypeInstanciation *********")
        type = self.context.types[node.identifier]
        print("***** Mi tipo *********")
        print(type)
        if (type == None):
            self.errors(f'The type "{node.identifier}" not exist.')
            return ErrorType()
        return type

    @visitor.when(VarMethod)
    def visit(self,node,scope):
        try:
            print("***** VarMethod *********")
            print(node.identifier)

            var = scope.find_variable(node.identifier)
            if (var == None):
                self.errors(f'The variable "{node.identifier}" not exist.')
                return ErrorType()
            print(node.function_call.identifier)
            print(f"{var.name} -------- {var.type}")
            method = var.type.get_method(node.function_call.identifier)
            '''        if (method == None):
                self.errors(f'The method "{node.function_call.identifier}" not exist.')
                return ErrorType()'''
            print(method.return_type)
            '''self.identifier = identifier
            self.arguments = arguments'''
            
            return method.return_type
        except SemanticError as e:
            self.errors.append(e)
        
    @visitor.when(VarAttr)
    def visit(self,node,scope):
        print("***** VarAttr *********")
        print(node.attr)
        print(node.identifier)
        var_name = node.identifier+"."+node.attr
        var = scope.find_variable(var_name)
        if var == None:
            print("agrego: "+var_name)
            type = self.context.get_type("Object",self.errors)
            scope.define_variable(var_name, type)
            return type
        else:   
            print("encuentro: "+var_name)
            return var.type  
        pass

    @visitor.when(InheritsType)
    def visit(self,node,scope):
        print("***** InheritsType *********")
        pass

    @visitor.when(DeclarationScope)
    def visit(self,node,scope):
        for statement in node.statements:
            print(statement)
            result = self.visit(statement,scope)
        return result
        
    @visitor.when(TypeMethodDeclaration)
    def visit(self,node,scope):
        print("***** TypeMethodDeclaration *********")
        for key in scope.locals:
            print(f"{key.name} -------- {key.type}")
        child = scope.create_child()
        for parameter in node.parameters:
            parameter.type = self.visit(parameter,child)
        
        result = self.visit(node.body,child)
        scope.children.remove(child)
        return result
        
    '''self.type_anotation = type_anotation
    self.parameters = parameters
    self.body = body'''

    @visitor.when(TypeVarInit)
    def visit(self,node, scope):
        print("***** TypeVarInit *********")
        node.identifier.identifier = "self."+node.identifier.identifier
        print(node.identifier.identifier)
        print(node.expression)
        varType1 = self.visit(node.identifier,scope)
        varType2 = self.visit(node.expression,scope)
        print(varType1)
        print(varType2)
        if node.type_downcast == None:
            if (varType1.name == "Object"):
                node.type_downcast = self.context.get_type(varType2.name,self.errors)
                var = scope.find_variable(node.identifier.identifier)
                var.type = self.context.get_type(varType2.name,self.errors)
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