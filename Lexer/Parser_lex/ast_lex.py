from Lexer.Cmp_lex import visitor
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
    
    
        
def get_printer():

    class PrintVisitor(object):
        @visitor.on('node')
        def visit(self, node, tabs):
            pass

        @visitor.when(ConcatenationNode)
        def visit(self, node, tabs=0):
            ans = '\t' * tabs + f'\\__<expr> Concat <expr>'
            left = self.visit(node.left, tabs + 1)
            right = self.visit(node.right, tabs + 1)
            return f'{ans}\n{left}\n{right}'

        @visitor.when(UnionNode)
        def visit(self, node, tabs=0):
            ans = '\t' * tabs + f'\\__<expr> Union <expr>'
            left = self.visit(node.left, tabs + 1)
            right = self.visit(node.right, tabs + 1)
            return f'{ans}\n{left}\n{right}'

        @visitor.when(ClausureNode)
        def visit(self, node, tabs=0):
            ans = '\t' * tabs + f'\\__ClausureNode: <expr>*'
            expr = self.visit(node.node, tabs + 1)
            return f'{ans}\n{expr}'

        @visitor.when(PositiveClausureNode)
        def visit(self, node, tabs=0):
            ans = '\t' * tabs + f'\\__PositiveClausureNode: <expr>+'
            body = self.visit(node.node, tabs + 1)
            return f'{ans}\n{body}'

        @visitor.when(BinaryNode)
        def visit(self, node, tabs=0):
            ans = '\t' * tabs + f'\\__<expr> {node.__class__.__name__} <expr>'
            left = self.visit(node.left, tabs + 1)
            right = self.visit(node.right, tabs + 1)
            return f'{ans}\n{left}\n{right}'

        @visitor.when(OptionalNode)
        def visit(self, node, tabs=0):
            ans = '\t' * tabs + f'\\__OptionalNode: <expr>?'
            body = self.visit(node.node, tabs + 1)
            return f'{ans}\n{body}'

        @visitor.when(NotNode)
        def visit(self, node, tabs=0):
            ans = '\t' * tabs + f'\\__NotNode: <expr>?'
            body = self.visit(node.node, tabs + 1)
            return f'{ans}\n{body}'

        @visitor.when(AtomicNode)
        def visit(self, node, tabs=0):
            return '\t' * tabs + f'\\__AtomicNode: {node.lex}'

        @visitor.when(EllipsisNode)
        def visit(self, node, tabs=0):
            ans = '\t' * tabs + f'\\__EllipsisNode: <expr>...<expr>'
            left = self.visit(node.left, tabs + 1)
            right = self.visit(node.right, tabs + 1)
            return f'{ans}\n{left}\n{right}'

        @visitor.when(VocabularyNode)
        def visit(self, node, tabs=0):
            ans = '\t' * tabs + f'\\__VocabularyNode: <-|->'
            return f'{ans}'

        
        
        
    printer = PrintVisitor()
    return (lambda ast: printer.visit(ast))
