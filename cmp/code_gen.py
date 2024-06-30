from cmp import visitor
from cmp import ast_h

class MIPSTranslator:
    def op_abs(src, dest):
        return f"abs {dest}, {src}"
    
    def op_add(r1, r2, dest):
        return f"add {dest}, {r1}, {r2}"
    
    def op_addu(r1, r2, dest):
        return f"addu {dest}, {r1}, {r2}"
    
    def op_and(r1, r2, dest):
        return f"and {dest}, {r1}, {r2}"

    def op_div(r1, r2, dest):
        return f"div {dest}, {r1}, {r2}"
    
    def op_divu(r1, r2, dest):
        return f"divu {dest}, {r1}, {r2}"

    def op_mult(r1, r2, dest):
        return f"mult {dest}, {r1}, {r2}"
    
    def op_multu(r1, r2, dest):
        return f"multu {dest}, {r1}, {r2}"
    
    def op_nor(r1, r2, dest):
        return f"nor {dest}, {r1}, {r2}"
    
    def op_not(src, dest):
        return f"not {dest}, {src}"
    
    def op_or(r1, r2, dest):
        return f"or {dest}, {r1}, {r2}"
    
    def op_rem(r1, r2, dest):
        return f"rem {dest}, {r1}, {r2}"
    
    def op_remu(r1, r2, dest):
        return f"remu {dest}, {r1}, {r2}"


class HulkCodeGenerator:
    def __init__(self):
        super().__init__()

    @visitor.on('node')
    def visit(self, node, tabs):
        pass
    
    @visitor.when(ast_h.Node)
    def visit(self, node):
        return node.print_visitor(self)     
    
    @visitor.when(ast_h.Add)
    def visit(self, node):
        term = self.visit(node.term)
        op = self.visit(node.aritmetic_operation)
        res = float(term)+float(op)
        print(res)
        return res