from semantic import *
import visitor 

class TypeCollector(object):
    def __init__(self, errors=[]):
        self.context = None
        self.errors = errors
    
    @visitor.on('node')
    def visit(self, node):
        pass
    
    @visitor.when(Program)
    def visit(self, node):
        self.context = Context()
        for declaration in node.program_decl_list:
            self.visit(declaration)
        return self.context  

    @visit.when(Type_declaration)#ver
    def visit(self, node):
        try :
            self.context.get_type(node.identifier)
        except SemanticError:
            self.context.create_type(node.identifier)
    @visit.when(Type_declaration)  
   

class TypeBuilder:
    def __init__(self, context, errors=[]):
        self.context = context
        self.current_type = None
        self.errors = errors
    
    @visitor.on('node')
    def visit(self, node):
        pass
    
    # Your code here!!!
    # ????

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
        return scope

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
        pass
    
    @visitor.when(ConstantNumNode)
    def visit(self, node, scope):
        pass

    @visitor.when(VariableNode)
    def visit(self, node, scope):
        pass

    @visitor.when(InstantiateNode)
    def visit(self, node, scope):
        pass
