from cmp_lex import visitor
class Node:
    def evaluate(self):
        raise NotImplementedError()
        
class AtomicNode(Node):
    def __init__(self, lex):
        self.lex = lex

class UnaryNode(Node):
    def __init__(self, node):
        self.node = node
    
class BinaryNode(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right
        

class VocabularyNode(Node):
    pass

class ClausureNode(UnaryNode):
    pass

class PositiveClausureNode(UnaryNode):
    pass

# operador ? acepta 0 o 1 ocurrencias
class OptionalNode(UnaryNode):
    pass

class ConcatenationNode(BinaryNode):
    pass

class UnionNode(BinaryNode):
    pass

# operador ! niega la expresión
class NotNode(UnaryNode):
    pass

# rango de caracteres de left a right
class EllipsisNode(BinaryNode):
    pass
    
    
        
def get_printer(AtomicNode=AtomicNode, UnaryNode=UnaryNode, BinaryNode=BinaryNode, ):

    class PrintVisitor(object):
        @visitor.on('node')
        def visit(self, node, tabs):
            pass

        @visitor.when(UnaryNode)
        def visit(self, node, tabs=0):
            ans = '\t' * tabs + f'\\__<expr> {node.__class__.__name__}'
            child = self.visit(node.node, tabs + 1)
            return f'{ans}\n{child}'

        @visitor.when(BinaryNode)
        def visit(self, node, tabs=0):
            ans = '\t' * tabs + f'\\__<expr> {node.__class__.__name__} <expr>'
            left = self.visit(node.left, tabs + 1)
            right = self.visit(node.right, tabs + 1)
            return f'{ans}\n{left}\n{right}'

        @visitor.when(AtomicNode)
        def visit(self, node, tabs=0):
            return '\t' * tabs + f'\\__ {node.__class__.__name__}: {node.lex}'
        
        @visitor.when(VocabularyNode)
        def visit(self, node, tabs=0):
            return '\t' * tabs + f'\\__ {node.__class__.__name__}: {node.lex}'
        
        @visitor.when(ClausureNode)
        def visit(self, node, tabs=0):
            return '\t' * tabs + f'\\__ {node.__class__.__name__}: {node.lex}'

        @visitor.when(PositiveClausureNode)
        def visit(self, node, tabs=0):
            return '\t' * tabs + f'\\__ {node.__class__.__name__}: {node.lex}'
        
        @visitor.when(OptionalNode)
        def visit(self, node, tabs=0):
            return '\t' * tabs + f'\\__ {node.__class__.__name__}: {node.lex}'
        
        @visitor.when(ConcatenationNode)
        def visit(self, node, tabs=0):
            return '\t' * tabs + f'\\__ {node.__class__.__name__}: {node.lex}'
        
        @visitor.when(UnionNode)
        def visit(self, node, tabs=0):
            return '\t' * tabs + f'\\__ {node.__class__.__name__}: {node.lex}'
        
        @visitor.when(NotNode)
        def visit(self, node, tabs=0):
            return '\t' * tabs + f'\\__ {node.__class__.__name__}: {node.lex}'
        
        @visitor.when(EllipsisNode)
        def visit(self, node, tabs=0):
            return '\t' * tabs + f'\\__ {node.__class__.__name__}: {node.lex}'
        
        
        
    printer = PrintVisitor()
    return (lambda ast: printer.visit(ast))
printer = get_printer(AtomicNode=AtomicNode, UnaryNode=UnaryNode, BinaryNode=BinaryNode)