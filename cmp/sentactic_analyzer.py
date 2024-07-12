from cmp.semantic import *
from cmp.visitor import *
from cmp.ast_h import *

shownode = HulkPrintVisitor()

class TypeCollector(object):
    def __init__(self, code, errors=[]):
        self.context = None
        self.errors = errors
        self.code = code

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
        '''String.define_attribute(Attribute("name","String"))
        String.define_method(Method('length',[],[],Number,[]))
        String.define_method(Method('concat',["other"],[String],String,[]))
        String.define_method(Method('substr',["from","to"],[Number,Number],String,[]))'''
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
    def __init__(self, code, context, errors=[]):
        self.context = context
        self.current_type = None
        self.errors = errors
        self.code = code

    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(Program)
    def visit(self, node):
        if isinstance(node.program_decl_list, list):
            for program_decl in node.program_decl_list:
                if isinstance(program_decl, list):
                    for program_decl_item in program_decl:
                        self.visit(program_decl_item)
                else:                
                    self.visit(program_decl)
        else:
            self.visit(node.program_decl_list)

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
        try:
            type_node = self.context.get_type(node.name,self.errors)
            if prohibit := node.extends == 'String' or node.extends == 'String' or node.extends == 'String':
                self.errors.append(f'Error in line {node.lineno} index {node.index}. \n {self.code[node.lineno]}\n.  The protcol {node.name} can not inherit from String,Number or Boolean')

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
    def __init__(self, code, context, errors=[]):
        self.context = context
        self.current_type = None
        self.current_method = None
        self.errors = errors
        self.code = code

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
        if arg == None or isinstance(arg, TypeError) or isinstance(arg, list):
            return False
        if isinstance(arg, str):
            arg = self.context.get_type(arg,self.errors)
        return(arg.conforms_to(self.context.get_type(type,self.errors)))  

    @visitor.on('node')
    def visit(self, node, scope):
        pass

    @visitor.when(Program)
    def visit(self, node, scope=None):
        try: 

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
                    scope.children.remove(newScope)'''

            #Comprobando correctitud de los métodos en el contexto

            for key in self.context.methods:
                method = self.context.methods[key]
                print(method)
                child = scope.create_child()
                for i in range(0,len(method.param_names)):
                    child.define_variable(method.param_names[i],method.param_types[i])
                if method.body != None:      
                    retType = self.visit(method.body,child)
                    if not self.toconforms_to(retType,method.return_type.name):
                        self.errors.append(f'The function "{method.name}" does not return the type "{method.return_type.name}"')
                        
            child = scope.create_child()
            if isinstance(node.program_decl_list, list):
                for program_decl in node.program_decl_list:
                    if isinstance(program_decl, list):
                        for program_decl_item in program_decl:
                            self.visit(program_decl_item, child)
                    else:  
                        self.visit(program_decl, child)
            else:
                self.visit(node.program_decl_list, child)

            #scope.children.remove(child)

            return scope
        except SemanticError as e:
            self.errors.append(e)

    @visitor.when(BinaryBuildInFunction)
    def visit(self,node,scope):
        try:
            arg1Type = self.visit(node.argument1,scope)
            if arg1:= not(self.toconforms_to(arg1Type,'Number')):
                self.errors.append(f'Error in line {node.lineno} index {node.index}. \n {self.code[node.lineno]}\n.  The type of the base is not Number')
            arg2Type = self.visit(node.argument2,scope)
            if arg2 := not(self.toconforms_to(arg2Type,'Number')):
                self.errors.append(f'Error in line {node.lineno} index {node.index}. \n {self.code[node.lineno]}\n.  The type of x is not Number')
            if arg1 or arg2:
                return ErrorType()
            return self.context.methods[node.func].return_type 
        except SemanticError as e:
            self.errors.append(e)


    @visitor.when(Add)
    def visit(self,node,scope):
        try:
            arg1Type = self.visit(node.term,scope)
            arg2Type = self.visit(node.aritmetic_operation,scope)

            if arg1:= not(self.toconforms_to(arg1Type,'Number')):
                self.errors.append(f'Error in line {node.lineno} index {node.index}. \n {self.code[node.lineno]}\n.  The type of the right member is not Number')

            if arg2 := not(self.toconforms_to(arg2Type,'Number')):
                self.errors.append(f'Error in line {node.lineno} index {node.index}. \n {self.code[node.lineno]}\n.  The type of left member is not Number')

            if arg1 or arg2:
                return ErrorType()

            return arg1Type  
        except SemanticError as e:
            self.errors.append(e)

    @visitor.when(Sub)
    def visit(self,node,scope):
        try:
            arg1Type = self.visit(node.term,scope)
            
            arg2Type = self.visit(node.aritmetic_operation,scope)
            
            if arg1:= not(self.toconforms_to(arg1Type,'Number')):
                self.errors.append(f'Error in line {node.lineno} index {node.index}. \n {self.code[node.lineno]}\n. The type of the right member is not Number')

            if arg2 := not(self.toconforms_to(arg2Type,'Number')):
                self.errors.append(f'Error in line {node.lineno} index {node.index}. \n {self.code[node.lineno]}\n. The type of left member is not Number')

            if arg1 or arg2:
                return ErrorType()

            return arg1Type 
        except SemanticError as e:
            self.errors.append(e)

    @visitor.when(Mult)
    def visit(self,node,scope):
        try:
            arg1Type = self.visit(node.factor,scope)
            
            arg2Type = self.visit(node.term,scope)
            
            if arg1:= not(self.toconforms_to(arg1Type,'Number')):
                self.errors.append(f'Error in line {node.lineno} index {node.index}. \n {self.code[node.lineno]}\n. The type of the right member is not Number')

            if arg2 := not(self.toconforms_to(arg2Type,'Number')):
                self.errors.append(f'Error in line {node.lineno} index {node.index}. \n {self.code[node.lineno]}\n. The type of left member is not Number')

            if arg1 or arg2:
                return ErrorType()

            return arg1Type 
        except SemanticError as e:
            self.errors.append(e)


    @visitor.when(Div)
    def visit(self,node,scope):
        try:
            arg1Type = self.visit(node.factor,scope)
            
            arg2Type = self.visit(node.term,scope)
            
            if arg1:= not(self.toconforms_to(arg1Type,'Number')):
                self.errors.append(f'Error in line {{{node.lineno} index {node.index}. \n {self.code[node.lineno]}\n. The type of the right member is not Number')

            if arg2 := not(self.toconforms_to(arg2Type,'Number')):
                self.errors.append(f'Error in line {node.lineno} index {node.index}. \n {self.code[node.lineno]}\n. The type of left member is not Number')

            if arg1 or arg2:
                return ErrorType()

            return arg1Type 

        except SemanticError as e:
            self.errors.append(e)


    @visitor.when(Mod)
    def visit(self,node,scope):
        try:
            arg1Type = self.visit(node.factor,scope)
            arg2Type = self.visit(node.term,scope) 
            

            if arg1:= not(self.toconforms_to(arg1Type,'Number')):
                self.errors.append(f'Error in line {{{node.lineno} index {node.index}. \n {self.code[node.lineno]}\n. The type of the right member is not Number')

            if arg2 := not(self.toconforms_to(arg2Type,'Number')):
                self.errors.append(f'Error in line {node.lineno} index {node.index}. \n {self.code[node.lineno]}\n. The type of left member is not Number')

            if arg1 or arg2:
                return ErrorType()

            return arg1Type 
        except SemanticError as e:
            self.errors.append(e)

    @visitor.when(Power)
    def visit(self,node,scope):
        try:
            arg1Type = self.visit(node.factor,scope)
            
            arg2Type = self.visit(node.base_exponent,scope)
            
            if arg1:= not(self.toconforms_to(arg1Type,'Number')):
                self.errors.append(f'Error in line {node.lineno} index {node.index}. \n {self.code[node.lineno]}\n. The type of the right member is not Number')

            if arg2 := not(self.toconforms_to(arg2Type,'Number')):
                self.errors.append(f'Error in line {node.lineno} index {node.index}. \n {self.code[node.lineno]}\n. The type of left member is not Number')

            if arg1 or arg2:
                return ErrorType()

            return arg1Type 
        except SemanticError as e:
            self.errors.append(e)

    @visitor.when(UnaryBuildInFunction)
    def visit(self,node,scope):
        try:
            argType = self.visit(node.argument,scope)
            
            if node.func =='print':
                if self.toconforms_to(argType, 'Number') or self.toconforms_to(argType, 'String') or self.toconforms_to(argType, 'Boolean') :
                    return self.context.get_type('Void',self.errors)
                self.errors.append(f'Error in line {node.lineno} index {node.index}. \n {self.code[node.lineno]}\n. The argument is not valid')
            else:
                if self.toconforms_to(argType, 'Number'):
                    return self.context.get_type('Number',self.errors)
                self.errors.append(f'Error in line {node.lineno} index {node.index}. \n {self.code[node.lineno]}\n. The argument is not a Number')
                return ErrorType()
        except SemanticError as e:
            self.errors.append(e)

    @visitor.when(NoParamBuildInFunction)
    def visit(self,node,scope):
        try:
            return self.context.get_type('Number',self.errors)
        except SemanticError as e:
            self.errors.append(e)

    @visitor.when(BuildInConst)
    def visit(self,node,scope):
        try:
            return self.context.get_type('Number',self.errors)
        except SemanticError as e:
            self.errors.append(e)

    @visitor.when(FunctionCall)
    def visit(self,node,scope):
        try:
            param_types = [self.visit(argument,scope) for argument in node.arguments]
            methods = filter_by_name(self.context.methods,node.identifier)
            if len(methods) == 0:
                self.errors.append(f'Error in line {node.lineno} index {node.index}. \n {self.code[node.lineno-1]}\n. The method is not defined')
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
            self.errors.append(f'Error in line {node.lineno} index {node.index}. \n {self.code[node.lineno]}\n. There is no method compatible with those parameters')
            return ErrorType()
        except SemanticError as e:
            self.errors.append(e)

    @visitor.when(VectorVarUse)
    def visit(self,node,scope):
        try:
            self.visit(node.identifier,scope)
            return self.visit(node.index,scope)
        except SemanticError as e:
            self.errors.append(e)



    @visitor.when(VectorExpressionDeclaration)
    def visit(self,node,scope):
        try:
            range = self.visit(node.rangeexpression,scope)
            self.visit(node.identifier,scope)
            node.identifier.type = range
            var = scope.find_variable(node.identifier.identifier)
            var.type = range
            self.visit(node.expression,scope)
            return range
        except SemanticError as e:
            self.errors.append(e)

    @visitor.when(VectorRangeDeclaration)
    def visit(self,node,scope):
        try:
            elem1Type = self.visit(node.range[0],scope)  
            error = False
            if elem1Type != None:
                for i in range(1,len(node.range)):
                    elemType = self.visit(node.range[i],scope)
                    if not(elemType.conforms_to(elem1Type)):
                        error = True
                        self.errors.append(f'Error in line {node.lineno} index {node.index}. \n {self.code[node.lineno]}\n. The type of element {i} is not {elem1Type.name} ')
            if error:
                return ErrorType()
            return elem1Type
        except SemanticError as e:
            self.errors.append(e)




    @visitor.when(Scope)
    def visit(self,node,scope):
        try:
            child = scope.create_child()

            for st in node.statements:
                result = self.visit(st,child)

            return result
        except SemanticError as e:
            self.errors.append(e)

    @visitor.when(ForLoop)#comprobar
    def visit(self,node,scope):
        try:
            child = scope.create_child()
            expType = self.visit(node.expression,child)
            varType = self.visit(node.identifier,child)
            var = child.find_variable(node.identifier.identifier)
            var.type = expType
            node.identifier.type = expType
            return self.visit(node.body,child)
        except SemanticError as e:
            self.errors.append(e)

    @visitor.when(VarDeclaration)
    def visit(self,node,scope):
        try:
            child = scope.create_child()
            for var in node.var_init_list:
                type = self.context.get_type("Object" if var.identifier.type == None else var.identifier.type,self.errors) 
                scope.define_variable(var.identifier.identifier, type)
            for var in node.var_init_list:
                self.visit(var,child)
            return self.visit(node.body,child)
        except SemanticError as e:
            self.errors.append(e)

    @visitor.when(InlineConditional)
    def visit(self,node,scope):#arreglar
        try:
            conType = self.visit(node.conditional_expression,scope)
            if self.toconforms_to(conType,'Boolean'):
                self.errors.append(f'Error in line {node.lineno} index {node.index}. \n {self.code[node.lineno]}\n. The conditional expression is not evaluable')
                return TypeError()
            self.visit(node.else_elif_statement,scope)

            return self.visit(node.expression,scope)
        except SemanticError as e:
            self.errors.append(e)

    @visitor.when(FullConditional)
    def visit(self,node,scope):#arreglar
        try:
            conType = self.visit(node.conditional_expression,scope)

            if self.toconforms_to(conType.name,'Boolean'):
                self.errors.append(f'Error in line {node.lineno} index {node.index}. \n {self.code[node.lineno]}\n. The conditional expression is not evaluable')
                return TypeError()
            self.visit(node.else_elif_statement,scope)

            for st in node.scope_list:
                result = self.visit(st,scope)   

            return result  
        except SemanticError as e:
            self.errors.append(e)

    @visitor.when(Not)
    def visit(self,node,scope):
        try:
            conType = self.visit(node.condition,scope)
            if self.toconforms_to(conType.name,'Boolean'):
                return conType
            else:
                scope.errors.append(f'Error in line {node.lineno} index {node.index}. \n {self.code[node.lineno]}\n. The type in not Boolean')
                return ErrorType()
        except SemanticError as e:
            self.errors.append(e)

    @visitor.when(And)
    def visit(self,node,scope):
        try:
            con1Type = self.visit(node.condition,scope)
            con2Type = self.visit(node.conditional_expression,scope)
            if con1 := self.toconforms_to(con1Type.name, 'Boolean'):
                self.errors.append(f'Error in line {node.lineno} index {node.index}. \n {self.code[node.lineno]}\n. The first parameter\'s type in not Boolean')
            if con2 := self.toconforms_to(con2Type.name, 'Boolean'):
                self.errors.append(f'Error in line {node.lineno} index {node.index}.   {self.code[node.lineno-1]} . The second parameter\'s type in not Boolean') 
            if  con1 or con2:
                return ErrorType()
            return con1Type
        except SemanticError as e:
            self.errors.append(e)

    @visitor.when(Or)
    def visit(self,node,scope):
        con1Type = self.visit(node.condition,scope)
        con2Type = self.visit(node.conditional_expression,scope)
        if con1 := self.toconforms_to(con1Type.name, 'Boolean'):
            self.errors.append(f'Error in line {node.lineno} index {node.index}.   {self.code[node.lineno-1]} . The first parameter\'s type in not Boolean')
        if con2 := self.toconforms_to(con2Type.name, 'Boolean'):
            self.errors.append(f'Error in line {node.lineno} index {node.index}.   {self.code[node.lineno-1]} . The second parameter\'s type in not Boolean')
        if  con1 or con2:
            return ErrorType()
        return con1Type

    @visitor.when(Is)
    def visit(self,node,scope):
        try:
            con1Type = self.visit(node.condition,scope)
            con2Type = self.visit(node.conditional_expression,scope)
            if not(isinstance(con2Type,Type)):
                self.errors.append(f'Error in line {node.lineno} index {node.index}.   {self.code[node.lineno-1]} .  The parameter in not a type')
                return ErrorType()
            return self.context.get_type('Boolean',self.errors)
        except SemanticError as e:
            self.errors.append(e)

    @visitor.when(Equal)
    def visit(self,node,scope):
        try:
            con1Type = self.visit(node.expr1,scope)
            con2Type = self.visit(node.expr2,scope)
            if  eval1 := self.toconforms_to(con1Type.name,'Number') or self.toconforms_to(con1Type.name,'String') :
                self.errors.append(f'Error in line {node.lineno} index {node.index}.   {self.code[node.lineno-1]} . The first parameter\'s type in not Number or String')
            if  eval2 := self.toconforms_to(con2Type.name,'Number') or self.toconforms_to(con2Type.name,'String') :
                self.errors.append(f'Error in line {node.lineno} index {node.index}.   {self.code[node.lineno-1]} .  The second parameter\'s type in not Number or String')  
            if  eval1 or eval2 :
                return ErrorType()

            return self.context.get_type('Boolean',self.errors)
        except SemanticError as e:
            self.errors.append(e)

    @visitor.when(NotEqual)
    def visit(self,node,scope):
        try:
            con1Type = self.visit(node.expr1,scope)
            con2Type = self.visit(node.expr2,scope)

            if  eval1 := self.toconforms_to(con1Type.name,'Number') or self.toconforms_to(con1Type.name,'String') :
                self.errors.append(f'Error in line {node.lineno} index {node.index}.   {self.code[node.lineno-1]} . The first parameter\'s type in not Number or String')
            if  eval2 := self.toconforms_to(con2Type.name,'Number') or self.toconforms_to(con2Type.name,'String') :
                self.errors.append(f'Error in line {node.lineno} index {node.index}.   {self.code[node.lineno-1]} . The second parameter\'s type in not Number or String') 
            if  eval1 or eval2 :
                return ErrorType()

            return self.context.get_type('Boolean',self.errors)
        except SemanticError as e:
            self.errors.append(e)

    @visitor.when(LessEqual)
    def visit(self,node,scope):
        try:
            con1Type = self.visit(node.expr1,scope)
            con2Type = self.visit(node.expr2,scope)
            if con1 := not(self.toconforms_to(con1Type,'Number')):
                self.errors.append(f'Error in line {node.lineno} index {node.index}.   {self.code[node.lineno-1]} . The first parameter\'s type in not Number')
            if con2 := not(self.toconforms_to(con2Type,'Number')):
                self.errors.append(f'Error in line {node.lineno} index {node.index}.   {self.code[node.lineno-1]} . The second parameter\'s type in not Number')  
            if  con1 or con2:
                return ErrorType()
            return con1Type
        except SemanticError as e:
            self.errors.append(e)

    @visitor.when(GreaterEqual)
    def visit(self,node,scope):
        try:
            con1Type = self.visit(node.expr1,scope)
            con2Type = self.visit(node.expr2,scope)
            if con1 := not(self.toconforms_to(con1Type,'Number')):
                self.errors.append(f'Error in line {node.lineno} index {node.index}.   {self.code[node.lineno-1]} . The first parameter\'s type in not Number')
            if con2 := not(self.toconforms_to(con2Type,'Number')):
                self.errors.append(f'Error in line {node.lineno} index {node.index}.   {self.code[node.lineno-1]} . The second parameter\'s type in not Number')  
            if  con1 or con2:
                return ErrorType()
            return con1Type
        except SemanticError as e:
            self.errors.append(e)

    @visitor.when(LessThan)
    def visit(self,node,scope):
        try:
            con1Type = self.visit(node.expr1,scope)
            con2Type = self.visit(node.expr2,scope)
            if con1 := not(self.toconforms_to(con1Type,'Number')):
                self.errors.append(f'Error in line {node.lineno} index {node.index}.   {self.code[node.lineno-1]} . The first parameter\'s type in not Number')
            if con2 := not(self.toconforms_to(con2Type,'Number')):
                self.errors.append(f'Error in line {node.lineno} index {node.index}.   {self.code[node.lineno-1]} . The second parameter\'s type in not Number')  
            if  con1 or con2:
                return ErrorType()
            return con1Type
        except SemanticError as e:
            self.errors.append(e)

    @visitor.when(GreaterThan)
    def visit(self,node,scope):
        try:
            con1Type = self.visit(node.expr1,scope)
            con2Type = self.visit(node.expr2,scope)
            if con1 := not(self.toconforms_to(con1Type,'Number')):
                self.errors.append(f'Error in line {node.lineno} index {node.index}. \n {self.code[node.lineno]}\n. The first parameter\'s type in not Number')
            if con2 := not(self.toconforms_to(con2Type,'Number')):
                self.errors.append(f'Error in line {node.lineno} index {node.index}.   {self.code[node.lineno-1]} . The second parameter\'s type in not Number')   
            if  con1 or con2:
                return ErrorType()
            return con1Type
        except SemanticError as e:
            self.errors.append(e)


    @visitor.when(VarInit)
    def visit(self,node,scope):
        try:
            varType1 = self.visit(node.identifier,scope)
            if isinstance(varType1,ErrorType):
                return ErrorType()
            varType2 = self.visit(node.expression,scope)
            if isinstance(varType2,ErrorType):
                return ErrorType()
            if node.type_downcast == None:
                if self.context.get_type("Object",self.errors).conforms_to(varType1):
                    node.type_downcast = self.context.get_type(varType2.name,self.errors)
                    if isinstance(node.identifier.identifier, VarAttr):
                        var = scope.find_variable(node.identifier.identifier.identifier + "."+node.identifier.identifier.attr)
                    else:
                        var = scope.find_variable(node.identifier.identifier)

                    var.type = self.context.get_type(varType2.name,self.errors)
                    return varType2
                elif (varType2.conforms_to(varType1)):
                    node.type_downcast = self.context.get_type(varType2.name,self.errors)
                    return varType1
                else: 
                    return ErrorType()

            elif not(varType2.conforms_to(self.context.get_type(node.type_downcast,self.errors))):
                self.errors(f'Error in line {node.lineno} index {node.index}. \n {self.code[node.lineno]}\n. The value\'s type in not "{node.type_downcast}" ')
                return ErrorType()
            else:
                var = scope.find_variable(node.identifier.identifier)
                node.type_downcast = self.context.get_type(node.type_downcast,self.errors)
                var.type = node.type_downcast
                return node.type_downcast
        except SemanticError as e:
            self.errors.append(e)




    @visitor.when(VarUse)
    def visit(self,node,scope):
        try:
            if isinstance(node.identifier, VarAttr):
                node.type = self.visit(node.identifier,scope)
                return node.type
            else:
                var = scope.find_variable(node.identifier)
                if var == None:
                    node.type = self.context.get_type("Object" if node.type == None else node.type if isinstance(node.type,str) else node.type.name,self.errors) 
                    scope.define_variable(node.identifier, node.type)
                    return node.type
                else:    
                    node.type = var.type
                    return var.type  
        except SemanticError as e:
            self.errors.append(e)

    @visitor.when(Concat)
    def visit(self,node,scope):
        try:
            arg1Type = self.visit(node.atom,scope)
            arg2Type = self.visit(node.expression,scope)
            if arg1Type == None or arg2Type == None:
                return ErrorType()
            if self.toconforms_to(arg1Type,'Number') or self.toconforms_to(arg1Type,'String')  and not(self.toconforms_to(arg2Type.name,'Number') or  self.toconforms_to(arg2Type,'String')):
                    self.errors.append(f'Error in line {node.lineno} index {node.index}. \n {code[node.lineno]}\n. The type second parameter in not string or number')
                    return ErrorType()
            elif self.toconforms_to(arg1Type,'Number')  and not(self.toconforms_to(arg2Type,'String')) :
                    self.errors.append(f'Error in line {node.lineno} index {node.index}.   {self.code[node.lineno-1]} . You can not concat two numbers')
                    return ErrorType()
            elif not(self.toconforms_to(arg1Type,'Number') or  self.toconforms_to(arg1Type,'String')) and self.toconforms_to(arg2Type.name,'Number') or self.toconforms_to(arg2Type,'String') : 
                    self.errors.append(f'Error in line {node.lineno} index {node.index}.   {self.code[node.lineno-1]} . The type first parameter in not string or number')
                    return ErrorType()
            else:
                return self.context.get_type('String',self.errors)
        except SemanticError as e:
            self.errors.append(e)

    @visitor.when(WhileLoop)#comprobar
    def visit(self,node,scope):
        try:
            child = scope.create_child()
            value = self.visit(node.condition,child)
            return self.visit(node.body,child)
        except SemanticError as e:
            self.errors.append(e)

    @visitor.when(Number)
    def visit(self,node,scope):
        try:
            node.type_downcast = self.context.get_type('Number',self.errors)
            return node.type_downcast
        except SemanticError as e:
            self.errors.append(e)

    @visitor.when(String)
    def visit(self,node,scope):
        try:
            node.type_downcast = self.context.get_type('String',self.errors)
            return node.type_downcast
        except SemanticError as e:
            self.errors.append(e)

    @visitor.when(Boolean)
    def visit(self,node,scope):
        try:
            node.type_downcast = self.context.get_type('Boolean',self.errors)
            return node.type_downcast
        except SemanticError as e:
            self.errors.append(e)

    @visitor.when(TypeDeclaration)
    def visit(self,node, scope):#ver la parte de herencia
        try:
            type = self.context.get_type(node.identifier,self.errors)
            child = scope.create_child()
            parent = type
            while parent != None:
                for attr in parent.attributes:
                    child.define_variable("self."+attr.name,attr.type)
                parent = parent.parent
                if parent == self.context.get_type("Object",self.errors):
                    break

            if ( node.parameters != None):
                for parameter in node.parameters:
                    parameter.type = self.visit(parameter,child)


            self.visit(node.decl_body,child)
            for attr in type.attributes:
                attr.type = child.find_variable("self."+attr.name).type

            #scope.children.remove(child)
            return type
        except SemanticError as e:
            self.errors.append(e)


    @visitor.when(TypeInstanciation)
    def visit(self,node,scope):
        try:
            typearg = self.context.get_type(node.identifier,self.errors)
            if (typearg  == None or isinstance(typearg , ErrorType)):
                return ErrorType()
            return typearg 
        except SemanticError as e:
            self.errors.append(e)

    @visitor.when(VarMethod)
    def visit(self,node,scope):
        try:
            self.visit(node.identifier,scope)
            return self.visit(node.function_call,scope) 
        except SemanticError as e:
            self.errors.append(e)

    @visitor.when(VarAttr)
    def visit(self,node,scope):
        try:
            var_name = node.identifier+"."+node.attr
            var = scope.find_variable(var_name)
            if var == None:
                type = self.context.get_type("Object",self.errors)
                scope.define_variable(var_name, type)
                return type
            else:   
                return var.type  
        except SemanticError as e:
            self.errors.append(e)


    @visitor.when(DeclarationScope)
    def visit(self,node,scope):
        try:
            result = None
            for statement in node.statements:
                result = self.visit(statement,scope)
            return result
        except SemanticError as e:
            self.errors.append(e)

    @visitor.when(TypeMethodDeclaration)
    def visit(self,node,scope):
        try:
            child = scope.create_child()
            for parameter in node.parameters:
                parameter.type = self.visit(parameter,child)

            result = self.visit(node.body,child)
            #scope.children.remove(child)
            return result
        except SemanticError as e:
            self.errors.append(e)

    @visitor.when(TypeVarInit)
    def visit(self,node, scope):
        try:
            node.identifier.identifier = "self."+node.identifier.identifier
            varType1 = self.visit(node.identifier,scope)
            varType2 = self.visit(node.expression,scope)
            if node.type_downcast == None:
                if self.context.get_type("Object",self.errors).conforms_to(varType1):
                    node.type_downcast = self.context.get_type(varType2.name,self.errors)
                    var = scope.find_variable(node.identifier.identifier)
                    var.type = self.context.get_type(varType2.name,self.errors)
                    return varType2
                elif (varType2.conforms_to(varType1)):
                    node.type_downcast = self.context.get_type(varType2.name,self.errors)
                    return varType1
                else: 
                    self.errors(f'Error in line {node.lineno} index {node.index}.   {self.code[node.lineno-1]} . The value\'s type in not "{varType1.name}" ')
                    return ErrorType()

            elif not(varType2.conforms_to(self.context.get_type(node.type_downcast,self.errors))):
                self.errors(f'Error in line {node.lineno} index {node.index}.   {self.code[node.lineno-1]} . The value\'s type in not "{node.type_downcast}" ')
                return ErrorType()
            else:
                var = scope.find_variable(node.identifier.identifier)
                node.type_downcast = self.context.get_type(node.type_downcast,self.errors)
                var.type = node.type_downcast
                return node.type_downcast
        except SemanticError as e:
            self.errors.append(e)

    '''@visitor.when(FunctionDeclaration)
    def visit(self,node,scope):
        try:
            child = scope.create_child()
            for parameter in node.parameters:
                parameter.type = self.visit(parameter,child)
            result = self.visit(node.body,child)
            #scope.children.remove(child)
            return result
        except SemanticError as e:
            self.errors.append(e)'''
