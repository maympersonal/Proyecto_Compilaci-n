import cmp.visitor as visitor 

class Node:
    pass

class ProgramNode(Node):
    def __init__(self, dottypes, dotdata, dotcode):
        self.dottypes = dottypes
        self.dotdata = dotdata
        self.dotcode = dotcode

class TypeNode(Node):
    def __init__(self, name):
        self.name = name
        self.attributes = []
        self.methods = []

class DataNode(Node):
    def __init__(self, vname, value):
        self.name = vname
        self.value = value

class FunctionNode(Node):
    def __init__(self, fname, params, localvars, instructions):
        self.name = fname
        self.params = params
        self.localvars = localvars
        self.instructions = instructions

class ParamNode(Node):
    def __init__(self, name):
        self.name = name

class LocalNode(Node):
    def __init__(self, name):
        self.name = name

class InstructionNode(Node):
    pass

class AssignNode(InstructionNode):
    def __init__(self, dest, source):
        self.dest = dest
        self.source = source

class ArithmeticNode(InstructionNode):
    def __init__(self, dest, left, right):
        self.dest = dest
        self.left = left
        self.right = right

class PlusNode(ArithmeticNode):
    pass

class MinusNode(ArithmeticNode):
    pass

class StarNode(ArithmeticNode):
    pass

class DivNode(ArithmeticNode):
    pass

class LessNode(ArithmeticNode):
    pass

class LessEqualNode(ArithmeticNode):
    pass

class EqualNode(ArithmeticNode):
    pass

class NotEqualNode(ArithmeticNode):
    pass

class StrEqualNode(ArithmeticNode):
    pass

class StrNotEqualNode(ArithmeticNode):
    pass

class GreaterNode(ArithmeticNode):
    pass

class GreaterEqualNode(ArithmeticNode):
    pass

class UnaryNode(InstructionNode):
    def __init__(self, dest, expr):
        self.dest = dest
        self.expr = expr
        
class NotNode(UnaryNode):
    pass

class GetAttribNode(InstructionNode):
    def __init__(self, dest, instance, attr, typex):
        self.dest = dest
        self.instance = instance
        self.attr = attr
        self.type_id = typex

class SetAttribNode(InstructionNode):
    def __init__(self, instance, attr, value, typex):
        self.instance = instance
        self.attr = attr
        self.value = value
        self.type = typex

class GetIndexNode(InstructionNode):
    pass

class SetIndexNode(InstructionNode):
    pass

class AllocateNode(InstructionNode):
    def __init__(self, itype, dest):
        self.type = itype
        self.dest = dest

class ArrayNode(InstructionNode):
    pass

class TypeOfNode(InstructionNode):
    def __init__(self, obj, dest):
        self.obj = obj
        self.dest = dest

class LabelNode(InstructionNode):
    def __init__(self, name: str):
        self.name = name

class GotoNode(InstructionNode):
    def __init__(self, label: str):
        self.label = label

class GotoIfNode(InstructionNode):
    def __init__(self, condition, label: str):
        self.condition = condition
        self.label = label

class StaticCallNode(InstructionNode):
    def __init__(self, function, dest):
        self.function = function
        self.dest = dest

class DynamicCallNode(InstructionNode):
    def __init__(self, xtype, method, dest):
        self.type = xtype
        self.method = method
        self.dest = dest

class ArgNode(InstructionNode):
    def __init__(self, name):
        self.name = name

class ReturnNode(InstructionNode):
    def __init__(self, value=None):
        self.value = value

class LoadNode(InstructionNode):
    def __init__(self, dest, msg):
        self.dest = dest
        self.msg = msg

class LengthNode(InstructionNode):
    def __init__(self, dest, source):
        self.dest = dest
        self.source = source

class ConcatNode(InstructionNode):
    def __init__(self, dest, left, right):
        self.dest = dest
        self.left = left
        self.right = right

class PrefixNode(InstructionNode):
    pass
# ? es necesario?

class SubstringNode(InstructionNode):
    def __init__(self, dest, surce, index, length):
        self.dest = dest
        self.source = surce
        self.index = index
        self.length = length

class ToStrNode(InstructionNode):
    def __init__(self, dest, ivalue):
        self.dest = dest
        self.ivalue = ivalue

class ReadStringNode(InstructionNode):
    def __init__(self, dest):
        self.dest = dest

class ReadIntNode(InstructionNode):
    def __init__(self, dest):
        self.dest = dest

class VoidNode(InstructionNode):
    def __init__(self, dest, value):
        self.dest = dest
        self.value = value

class PrintStrNode(InstructionNode):
    def __init__(self, str_addr):
        self.str_addr = str_addr

class PrintIntNode(InstructionNode):
    def __init__(self, int_addr):
        self.int_addr = int_addr
        

class SenNode(InstructionNode):
    def __init__(self, dest, x):
        self.x = x
        self.dest = dest

class CosNode(InstructionNode):
    def __init__(self, dest, x):
        self.x = x
        self.dest = dest

class TanNode(InstructionNode):
    def __init__(self, dest, x):
        self.x = x
        self.dest = dest

class SqrtNode(InstructionNode):
    def __init__(self, dest, x):
        self.x = x
        self.dest = dest

class LogNode(InstructionNode):
    def __init__(self, dest, base, x):
        self.base = base
        self.x = x
        self.dest = dest

class PowNode(InstructionNode):
    def __init__(self, dest, base, x):
        self.base = base
        self.x = x
        self.dest = dest

class ExpNode(InstructionNode):
    def __init__(self, dest, x):
        self.x = x
        self.dest = dest

class ValueNode(Node):
    def __init__(self, value) -> None:
        self.value = value
        
class CompareTypesNode(InstructionNode):
    def __init__(self, dest, typeof, typex: str):
        self.dest = dest
        self.typeof = typeof
        self.type = typex

class RunTimeErrorNode(InstructionNode):
    def __init__(self, msg):
        self.msg = msg        

class ExitNode(InstructionNode):
    pass

def get_formatter():

    class PrintVisitor(object):
        @visitor.on('node')
        def visit(self, node):
            pass

        @visitor.when(ProgramNode)
        def visit(self, node):
            dottypes = '\n'.join(self.visit(t) for t in node.dottypes)
            dotdata = '\n'.join(self.visit(t) for t in node.dotdata)
            dotcode = '\n'.join(self.visit(t) for t in node.dotcode)

            return f'.TYPES\n{dottypes}\n\n.DATA\n{dotdata}\n\n.CODE\n{dotcode}'

        @visitor.when(DataNode)
        def visit(self, node):
            return f'{node.name} = {node.value}'

        @visitor.when(TypeNode)
        def visit(self, node):
            attributes = '\n\t'.join(f'attribute {x}' for x in node.attributes)
            methods = '\n\t'.join(f'method {x}: {y}' for x,y in node.methods)

            return f'type {node.name} {{\n\t{attributes}\n\n\t{methods}\n}}'

        @visitor.when(FunctionNode)
        def visit(self, node):
            params = '\n\t'.join(self.visit(x) for x in node.params)
            localvars = '\n\t'.join(self.visit(x) for x in node.localvars)
            # print(node.instructions)
            instructions = '\n\t'.join(self.visit(x) for x in node.instructions)

            return f'function {node.name} {{\n\t{params}\n\n\t{localvars}\n\n\t{instructions}\n}}'

        @visitor.when(DataNode)
        def visit(self, node: DataNode):
            return f'{node.name} = {node.value}'

        @visitor.when(ParamNode)
        def visit(self, node: ParamNode):
            return f'PARAM {node.name}'

        @visitor.when(LocalNode)
        def visit(self, node: LocalNode):
            return f'LOCAL {node.name}'

        @visitor.when(AssignNode)
        def visit(self, node: AssignNode):
            return f'{node.dest} = {node.source}'

        @visitor.when(PlusNode)
        def visit(self, node: PlusNode):
            return f'{node.dest} = {node.left} + {node.right}'

        @visitor.when(MinusNode)
        def visit(self, node: MinusNode):
            return f'{node.dest} = {node.left} - {node.right}'

        @visitor.when(StarNode)
        def visit(self, node: StarNode):
            return f'{node.dest} = {node.left} * {node.right}'

        @visitor.when(DivNode)
        def visit(self, node: DivNode):
            return f'{node.dest} = {node.left} / {node.right}'
        
        @visitor.when(LessNode)
        def visit(self, node: LessNode):
            return f'{node.dest} = {node.left} < {node.right}'
        
        @visitor.when(LessEqualNode)
        def visit(self, node: LessEqualNode):
            return f'{node.dest} = {node.left} <= {node.right}'
        
        @visitor.when(EqualNode)
        def visit(self, node: EqualNode):
            return f'{node.dest} = {node.left} == {node.right}'
        
        @visitor.when(NotEqualNode)
        def visit(self, node: NotEqualNode):
            return f'{node.dest} = {node.left} != {node.right}'
        
        @visitor.when(StrEqualNode)
        def visit(self, node: StrEqualNode):
            return f'{node.dest} = {node.left} == {node.right}'
        
        @visitor.when(StrNotEqualNode)
        def visit(self, node: StrNotEqualNode):
            return f'{node.dest} = {node.left} != {node.right}'
        
        @visitor.when(GreaterNode)
        def visit(self, node: GreaterNode):
            return f'{node.dest} = {node.left} > {node.right}'
        
        @visitor.when(GreaterEqualNode)
        def visit(self, node: GreaterEqualNode):
            return f'{node.dest} = {node.left} >= {node.right}'
        
        @visitor.when(NotNode)
        def visit(self, node: NotNode):
            return f'{node.dest} = NOT {node.expr}'
    
        @visitor.when(LabelNode)
        def visit(self, node: LabelNode):
            return f'LABEL {node.name}:'
        
        @visitor.when(GotoNode)
        def visit(self, node: GotoNode):
            return f'GOTO {node.label}'
        
        @visitor.when(GotoIfNode)
        def visit(self, node: GotoIfNode):
            return f'IF {node.condition} GOTO {node.label}'

        @visitor.when(AllocateNode)
        def visit(self, node: AllocateNode):
            return f'{node.dest} = ALLOCATE {node.type}'

        @visitor.when(TypeOfNode)
        def visit(self, node: TypeOfNode):
            return f'{node.dest} = TYPEOF {node.type}'

        @visitor.when(StaticCallNode)
        def visit(self, node: StaticCallNode):
            return f'{node.dest} = CALL {node.function}'

        @visitor.when(DynamicCallNode)
        def visit(self, node: DynamicCallNode):
            return f'{node.dest} = VCALL {node.type} {node.method}'
        
        @visitor.when(GetAttribNode)
        def visit(self, node: GetAttribNode):
            return f'{node.dest} = GETATTR {node.type_id} {node.attr}'
       
        @visitor.when(SetAttribNode)
        def visit(self, node: SetAttribNode):
            return f'SETATTR {node.attr} {node.value}'

        @visitor.when(ArgNode)
        def visit(self, node: ArgNode):
            return f'ARG {node.name}'
        
        @visitor.when(PrintIntNode)
        def visit(self, node: PrintIntNode):
            #  ? PRINT INT
            return f'PRINT {node.int_addr} '
        
        @visitor.when(PrintStrNode)
        def visit(self, node: PrintStrNode):
            print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
            # ? PRINT STR
            return f'PRINT {node.str_addr} '
        
        @visitor.when(SenNode)
        def visit(self, node: SenNode):
            return f'{node.dest} = SEN {node.x} '
        
        @visitor.when(CosNode)
        def visit(self, node: CosNode):
            return f'{node.dest} = COS {node.x} '
        
        @visitor.when(TanNode)
        def visit(self, node: TanNode):
            return f'{node.dest} = TAN {node.x} '
        
        @visitor.when(PowNode)
        def visit(self, node: PowNode):
            return f'{node.dest} = {node.base} ^ {node.x} '

        @visitor.when(ReturnNode)
        def visit(self, node: ReturnNode):
            return f'RETURN {node.value if node.value is not None else ""}'
        
        @visitor.when(LoadNode)
        def visit(self, node):
            return f"{node.dest} = LOAD {node.msg.name}"
        
        @visitor.when(LengthNode)
        def visit(self, node: LengthNode):
            return f'{node.dest} = LENGTH {node.source}'
        
        @visitor.when(ConcatNode)
        def visit(self, node: ConcatNode):
            return f'{node.dest} = CONCAT {node.left} {node.right}'
        
        @visitor.when(SubstringNode)
        def visit(self, node: SubstringNode):
            return f'{node.dest} = SUBSTRING {node.source} {node.index} {node.length}'
        
        @visitor.when(ToStrNode)
        def visit(self, node: ToStrNode):
            return f'{node.dest} = TOSTR {node.ivalue}'
        
        @visitor.when(VoidNode)
        def visit(self, node: VoidNode):
            return f'{node.dest} = VOID {node.value}'
        
        @visitor.when(CompareTypesNode)
        def visit(self, node: CompareTypesNode):
            return f'{node.dest} = {node.typeof} TYPE_EQUALS {node.type}'
        
        @visitor.when(RunTimeErrorNode)
        def visit(self, node: RunTimeErrorNode):
            return f'ABORT: {node.msg}'
        
        @visitor.when(ExitNode)
        def visit(self, node: ExitNode):
            return f'EXIT'
        
        @visitor.when(ValueNode)
        def visit(self, node: ValueNode):
            return ""

    printer = PrintVisitor()
    return (lambda ast: printer.visit(ast))


def get_formatter2():

    class TreePrintVisitor(object):
        def __init__(self, indent=0, prefix=''):
            self.indent = indent
            self.prefix = prefix

        @visitor.on('node')
        def visit(self, node):
            pass

        def _print_node(self, node, name):
            print(f"{' ' * self.indent}{self.prefix}{name}")
            self.indent += 1

        def _visit_children(self, node, children_attr, prefix=''):
            for child in getattr(node, children_attr):
                self.visit(child, prefix=prefix)

        @visitor.when(ProgramNode)
        def visit(self, node, prefix=''):
            self._print_node(node, 'ProgramNode')
            self._visit_children(node, 'dottypes', prefix='TYPES:')
            self._visit_children(node, 'dotdata', prefix='DATA:')
            self._visit_children(node, 'dotcode', prefix='CODE:')
            self.indent -= 1

        @visitor.when(TypeNode)
        def visit(self, node, prefix=''):
            self._print_node(node, f'TypeNode: {node.name}')
            self._visit_children(node, 'attributes', prefix='\tAttributes:')
            self._visit_children(node, 'methods', prefix='\tMethods:')
            self.indent -= 1

        @visitor.when(FunctionNode)
        def visit(self, node, prefix=''):
            self._print_node(node, f'FunctionNode: {node.name}')
            self._visit_children(node, 'params', prefix='\tParams:')
            self._visit_children(node, 'localvars', prefix='\tLocalVars:')
            self._visit_children(node, 'instructions', prefix='\tInstructions:')
            self.indent -= 1

        # ... (Add similar visit methods for other node types) ...
        @visitor.when(ArithmeticNode)
        def visit(self, node, prefix=''):
            self._print_node(node, node.__class__.__name__)
            self.visit(node.dest, prefix='Dest:')
            self.visit(node.left, prefix='Left:')
            self.visit(node.right, prefix='Right:')
            self.indent -= 1
        
        @visitor.when(UnaryNode)
        def visit(self, node, prefix=''):
            self._print_node(node, node.__class__.__name__)
            self.visit(node.dest, prefix='Dest:')
            self.visit(node.expr, prefix='Expr:')
            self.indent -= 1
        
        @visitor.when(GetAttribNode)
        def visit(self, node, prefix=''):
            self._print_node(node, 'GetAttribNode')
            self.visit(node.dest, prefix='Dest:')
            self.visit(node.instance, prefix='Instance:')
            self.indent -= 1
        
        @visitor.when(SetAttribNode)
        def visit(self, node, prefix=''):
            self._print_node(node, 'SetAttribNode')
            self.visit(node.instance, prefix='Instance:')
            self.visit(node.value, prefix='Value:')
            self.indent -= 1
        
        @visitor.when(GetIndexNode)
        def visit(self, node, prefix=''):
            self._print_node(node, 'GetIndexNode')
            self.visit(node.dest, prefix='Dest:')
            self.visit(node.instance, prefix='Instance:')
            self.visit(node.index, prefix='Index:')
            self.indent -= 1
        
        @visitor.when(SetIndexNode)
        def visit(self, node, prefix=''):
            self._print_node(node, 'SetIndexNode')
            self.visit(node.instance, prefix='Instance:')
            self.visit(node.index, prefix='Index:')
            self.visit(node.value, prefix='Value:')
            self.indent -= 1
        
        @visitor.when(AllocateNode)
        def visit(self, node, prefix=''):
            self._print_node(node, 'AllocateNode')
            self.visit(node.dest, prefix='Dest:')
            self.indent -= 1
        
        @visitor.when(ArrayNode)
        def visit(self, node, prefix=''):
            self._print_node(node, 'ArrayNode')
            self.visit(node.dest, prefix='Dest:')
            self.visit(node.size, prefix='Size:')
            self.indent -= 1
        
        @visitor.when(TypeOfNode)
        def visit(self, node, prefix=''):
            self._print_node(node, 'TypeOfNode')
            self.visit(node.dest, prefix='Dest:')
            self.visit(node.obj, prefix='Obj:')
            self.indent -= 1
        
        @visitor.when(LabelNode)
        def visit(self, node, prefix=''):
            self._print_node(node, f'LabelNode: {node.name}')
        
        @visitor.when(GotoNode)
        def visit(self, node, prefix=''):
            self._print_node(node, f'GotoNode: {node.label}')
        
        @visitor.when(GotoIfNode)
        def visit(self, node, prefix=''):
            self._print_node(node, f'GotoIfNode: {node.condition} -> {node.label}')
        
        @visitor.when(StaticCallNode)
        def visit(self, node, prefix=''):
            self._print_node(node, f'StaticCallNode: {node.function}')
            self.visit(node.dest, prefix='Dest:')
            self.indent -= 1
        
        @visitor.when(DynamicCallNode)
        def visit(self, node, prefix=''):
            self._print_node(node, f'DynamicCallNode: {node.type} {node.method}')
            self.visit(node.dest, prefix='Dest:')
            self.indent -= 1
        
        @visitor.when(ArgNode)
        def visit(self, node, prefix=''):
            self._print_node(node, f'ArgNode: {node.name}')
        
        @visitor.when(ReturnNode)
        def visit(self, node, prefix=''):
            self._print_node(node, 'ReturnNode')
            self.visit(node.value, prefix='Value:')
            self.indent -= 1
        
        @visitor.when(LoadNode)
        def visit(self, node, prefix=''):
            self._print_node(node, 'LoadNode')
            self.visit(node.dest, prefix='Dest:')
            self.visit(node.msg, prefix='Msg:')
            self.indent -= 1
        
        @visitor.when(LengthNode)
        def visit(self, node, prefix=''):
            self._print_node(node, 'LengthNode')
            self.visit(node.dest, prefix='Dest:')
            self.visit(node.source, prefix='Source:')
            self.indent -= 1
        
        @visitor.when(ConcatNode)
        def visit(self, node, prefix=''):
            self._print_node(node, 'ConcatNode')
            self.visit(node.dest, prefix='Dest:')
            self.visit(node.left, prefix='Left:')
            self.visit(node.right, prefix='Right:')
            self.indent -= 1
        
        @visitor.when(SubstringNode)
        def visit(self, node, prefix=''):
            self._print_node(node, 'SubstringNode')
            self.visit(node.dest, prefix='Dest:')
            self.visit(node.source, prefix='Source:')
            self.visit(node.index, prefix='Index:')
            self.visit(node.length, prefix='Length:')
            self.indent -= 1
        
        @visitor.when(ToStrNode)
        def visit(self, node, prefix=''):
            self._print_node(node, 'ToStrNode')
            self.visit(node.dest, prefix='Dest:')
            self.visit(node.ivalue, prefix='Value:')
            self.indent -= 1
        
        @visitor.when(ReadStringNode)
        def visit(self, node, prefix=''):
            self._print_node(node, 'ReadStringNode')
            self.visit(node.dest, prefix='Dest:')
            self.indent -= 1
        
        @visitor.when(ReadIntNode)
        def visit(self, node, prefix=''):
            self._print_node(node, 'ReadIntNode')
            self.visit(node.dest, prefix='Dest:')
            self.indent -= 1
        
        @visitor.when(VoidNode)
        def visit(self, node, prefix=''):
            self._print_node(node, 'VoidNode')
            self.visit(node.dest, prefix='Dest:')
            self.visit(node.value, prefix='Value:')
            self.indent -= 1
        
        @visitor.when(PrintStrNode)
        def visit(self, node, prefix=''):
            self._print_node(node, 'PrintStrNode')
            self.visit(node.str_addr, prefix='StrAddr:')
            self.indent -= 1
        
        @visitor.when(PrintIntNode)
        def visit(self, node, prefix=''):
            self._print_node(node, 'PrintIntNode')
            self.visit(node.int_addr, prefix='IntAddr:')
            self.indent -= 1
        
        @visitor.when(SenNode)
        def visit(self, node, prefix=''):
            self._print_node(node, 'SenNode')
            self.visit(node.dest, prefix='Dest:')
            self.visit(node.x, prefix='X:')
            self.indent -= 1
        
        @visitor.when(CosNode)
        def visit(self, node, prefix=''):
            self._print_node(node, 'CosNode')
            self.visit(node.dest, prefix='Dest:')
            self.visit(node.x, prefix='X:')
            self.indent -= 1
        
        @visitor.when(TanNode)
        def visit(self, node, prefix=''):
            self._print_node(node, 'TanNode')
            self.visit(node.dest, prefix='Dest:')
            self.visit(node.x, prefix='X:')
            self.indent -= 1
        
        @visitor.when(SqrtNode)
        def visit(self, node, prefix=''):
            self._print_node(node, 'SqrtNode')
            self.visit(node.dest, prefix='Dest:')
            self.visit(node.x, prefix='X:')
            self.indent -= 1
        
        @visitor.when(LogNode)
        def visit(self, node, prefix=''):
            self._print_node(node, 'LogNode')
            self.visit(node.dest, prefix='Dest:')
            self.visit(node.base, prefix='Base:')
            self.visit(node.x, prefix='X:')
            self.indent -= 1
        
        @visitor.when(PowNode)
        def visit(self, node, prefix=''):
            self._print_node(node, 'PowNode')
            self.visit(node.dest, prefix='Dest:')
            self.visit(node.base, prefix='Base:')
            self.visit(node.x, prefix='X:')
            self.indent -= 1
        
        @visitor.when(ExpNode)
        def visit(self, node, prefix=''):
            self._print_node(node, 'ExpNode')
            self.visit(node.dest, prefix='Dest:')
            self.visit(node.x, prefix='X:')
            self.indent -= 1
        
        
        @visitor.when(CompareTypesNode)
        def visit(self, node, prefix=''):
            self._print_node(node, 'CompareTypesNode')
            self.visit(node.dest, prefix='Dest:')
            self.visit(node.typeof, prefix='TypeOf:')
            self.visit(node.type, prefix='Type:')
            self.indent -= 1
        
        @visitor.when(RunTimeErrorNode)
        def visit(self, node, prefix=''):
            self._print_node(node, f'RunTimeErrorNode: {node.msg}')
        
        @visitor.when(ExitNode)
        def visit(self, node, prefix=''):
            self._print_node(node, 'ExitNode')
        
        


        @visitor.when(DataNode)
        def visit(self, node, prefix=''):
            self._print_node(node, f'DataNode: {node.name} = {node.value}')

        @visitor.when(ParamNode)
        def visit(self, node, prefix=''):
            self._print_node(node, f'ParamNode: {node.name}')

        @visitor.when(LocalNode)
        def visit(self, node, prefix=''):
            self._print_node(node, f'LocalNode: {node.name}')

        # ... (Add similar visit methods for other node types) ...

        @visitor.when(InstructionNode)
        def visit(self, node, prefix=''):
            self._print_node(node, node.__class__.__name__)

        @visitor.when(AssignNode)
        def visit(self, node, prefix=''):
            self._print_node(node, 'AssignNode')
            self.visit(node.dest, prefix='Dest:')
            self.visit(node.source, prefix='Source:')
            self.indent -= 1

        # ... (Add similar visit methods for other node types) ...

        @visitor.when(ValueNode)
        def visit(self, node, prefix=''):
            self._print_node(node, f'ValueNode: {node.value}')

    printer = TreePrintVisitor()
    return (lambda ast: printer.visit(ast))