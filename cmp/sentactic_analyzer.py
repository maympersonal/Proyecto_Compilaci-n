import cmp.semantic as semantic
import cmp.visitor as visitor
import cmp.ast_h as ast
class TypeCollector(object):
    def __init__(self, errors=[]):
        self.context = None
        self.errors = errors
    
    @visitor.on('node')
    def visit(self, node):
        pass
    
    @visitor.when(Program)
    def visit(self,errors):
        self.context = Context()
        for declaration in node.program_decl_list:
            self.visit(declaration,errors)
        return self.context  

    @visit.when(Type_declaration)#ver
    def visit(self, node):
        try :
            self.context.get_type(node.identifier)
        except SemanticError:
            self.context.create_type(node.identifier)
    
    
class TypeBuilder:#duda
    def __init__(self, context, errors=[]):
        self.context = context
        self.current_type = None
        self.errors = errors
    
    @visitor.on('node')
    def visit(self, node):
        pass
    
    @visitor.when(Program)
    def visit(self, context, errors):
        for declaration in node.program_decl_list:
            self.visit(declaration,context,errors)
        return errors 

class TypeChecker:
    def __init__(self, context, errors=[]):
        self.context = context
        self.current_type = None
        self.current_method = None
        self.errors = errors

    @visitor.on('node')
    def visit(self, node, scope):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node, scope=None):
        scope = Scope()
        for declaration in node.declarations:
            self.visit(declaration, scope.create_child())
        return self.errors

    @visitor.when(ClassDeclarationNode)
    def visit(self, node, scope):
        pass
        
    @visitor.when(AttrDeclarationNode)
    def visit(self, node, scope):
        pass

    @visitor.when(FuncDeclarationNode)
    def visit(self, node, scope):
        pass
    
    @visitor.when(VarDeclarationNode)
    def visit(self, node, scope):
        pass
            
    @visitor.when(AssignNode)
    def visit(self, node, scope):
        pass
    
    @visitor.when(CallNode)
    def visit(self, node, scope):
        pass
    
    @visitor.when(BinaryNode)
    def visit(self, node, scope):
        attr = RetAttr(node)
        var1= attr[0]
        type1 =self.visit(var1[1],scope)
        var2= attr[1]
        type2 =self.visit(var1[1],scope)
        if type1 is IntType:
            if type1 == type2:
                return type1
            else:
                self.errors.append()#duda
                return ErrorType(IntType)
        else:
                self.errors.append()#duda
                return ErrorType(IntType)
    
    @visitor.when(Number)
    def visit(self, node, scope):
        if node.value is float:
            return IntType()
        else:
                self.errors.append()#duda
                return ErrorType(IntType)

    @visitor.when(VariableNode)
    def visit(self, node, scope):
        pass

    @visitor.when(InstantiateNode)
    def visit(self, node, scope):
        pass

    #Métodos Auxiliares
    def RetAttr(object):
        return list(object.__dict__.items())


    