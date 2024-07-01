import cmp.cil_h as cil
from cmp.semantic import VariableInfo
from cmp.ast_h import *
import math

class BaseHulkToCil:
    def __init__(self, context) -> None:
        self.dottypes = []
        self.dotdata = []
        self.dotcode = []
        self.current_type = None
        self.current_method = None
        self.current_function = None
        self.context = context
    
    @property
    def params(self):
        return self.current_function.params
    
    @property
    def localvars(self):
        return self.current_function.localvars
    
    @property
    def instructions(self):
        return self.current_function.instructions
    
    def register_local(self, vinfo: VariableInfo):
        print('!!!!!!!!!!!!!!AQUIIII')
        print(self.current_function)
        print(vinfo.name)
        vinfo.name = f'local_{self.current_function.name[9:]}_{vinfo.name}_{len(self.localvars)}'
        local_node = cil.LocalNode(vinfo.name)
        self.localvars.append(local_node)
        return vinfo.name

    def define_internal_local(self):
        vinfo = VariableInfo('internal', None)
        return self.register_local(vinfo)

    def register_instruction(self, instruction):
        self.instructions.append(instruction)
        return instruction
    
    def to_function_name(self, method_name, type_name):
        return f'function_{method_name}_at_{type_name}'
    
    def register_function(self, function_name):
        function_node = cil.FunctionNode(function_name, [], [], [])
        self.dotcode.append(function_node)
        return function_node
    
    def register_type(self, name):
        type_node = cil.TypeNode(name)
        self.dottypes.append(type_node)
        return type_node

    def register_data(self, value):
        vname = f'data_{len(self.dotdata)}'
        data_node = cil.DataNode(vname, value)
        self.dotdata.append(data_node)
        return data_node


class HulkToCil(BaseHulkToCil):
    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(Program)
    def visit (self, node, scope):
        self.dotdata.append(cil.DataNode('pi', math.pi))
        self.current_function = self.register_function('entry')
        
        instance = self.define_internal_local()
        result = self.define_internal_local()
        
        main_method_name = self.to_function_name('main', 'Main')
        
        self.register_instruction(cil.AllocateNode('Main', instance))
        self.register_instruction(cil.ArgNode(instance))
        self.register_instruction(cil.StaticCallNode(main_method_name, result))
        self.register_instruction(cil.ReturnNode(0))
        self.current_function = self.register_function('main') #? dudoso esto
        # self.current_type = self.context.get_type('Global')

        for decl in node.program_decl_list:
            self.visit(decl, scope)
        return cil.ProgramNode(self.dottypes, self.dotdata, self.dotcode)
    
    @visitor.when(VarInit)
    def visit(self, node, scope):
        # self.current_function = self.register_function("var_init_function") # ? hace falta esto?
        var = self.register_local(VariableInfo(node.identifier, self.context.get_type(node.type_downcast)))
        self.current_vars[node.id] = var
        value = self.visit(node.expr, scope)
        self.register_instruction(cil.AssignNode(var, value))
        return var
    
    @visitor.when(VarDeclaration)
    def visit(self, node, scope):
        new_scope = Scope(scope)
        for var_init in node.var_init_list:
            self.visit(var_init, new_scope)
        return self.visit(node.body, new_scope)
    
    @visitor.when(VarUse)
    def visit(self, node, scope):
        return self.current_vars[node.id]

    @visitor.when(Add)
    def visit(self, node, scope):
        # self.current_function = self.register_function("add_function")
        left = self.visit(node.term, scope)
        right = self.visit(node.aritmetic_operation, scope)
        var = self.define_internal_local()   # aquiii
        self.register_instruction(cil.PlusNode(var, left, right))
        return var
    
    @visitor.when(Sub)
    def visit(self, node, scope):
        # self.current_function = self.register_function("sub_function")
        left = self.visit(node.term, scope)
        right = self.visit(node.aritmetic_operation, scope)
        var = self.define_internal_local()
        self.register_instruction(cil.MinusNode(var, left, right))
        return var
    
    @visitor.when(Mult)
    def visit(self, node, scope):
        # self.current_function = self.register_function("mult_function")
        left = self.visit(node.factor, scope)
        right = self.visit(node.term, scope)
        var = self.define_internal_local()
        self.register_instruction(cil.StarNode(var, left, right))
        return var
    
    @visitor.when(Div)
    def visit(self, node, scope):
        # self.current_function = self.register_function("div_function")
        left = self.visit(node.factor, scope)
        right = self.visit(node.term, scope)
        var = self.define_internal_local()
        self.register_instruction(cil.DivNode(var, left, right))
        return var
    
    @visitor.when(Number)
    def visit(self, node, scope):
        return node.value
    @visitor.when(Atom)
    def visit(self, node, scope):
        return node.value
    
    @visitor.when(Power)
    def visit(self, node, scope):
        # self.current_function = self.register_function("pow_function")
        base = self.visit(node.base_exponent, scope)
        exp = self.visit(node.factor, scope)
        var = self.define_internal_local()
        self.register_instruction(cil.PowNode(var, base, exp))
        return var
    
    @visitor.when(UnaryBuildInFunction)
    def visit(self, node, scope):
        arg = self.visit(node.argument, scope)
        if node.func == 'sen':
            var = self.define_internal_local()
            self.register_instruction(cil.SenNode(var, arg))
            return var
        elif node.func == 'cos':
            var = self.define_internal_local()
            self.register_instruction(cil.CosNode(var, arg))
            return var
        elif node.func == 'tan':
            var = self.define_internal_local()
            self.register_instruction(cil.TanNode(var, arg))
            return var
        elif node.func == 'str':
            var = self.define_internal_local()
            self.register_instruction(cil.ToStrNode(var, arg))
            return var
        elif node.func == 'print':
            self.register_instruction(cil.PrintNode(arg))
            return arg       
        
    