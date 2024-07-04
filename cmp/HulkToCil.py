import cmp.cil_h as cil
from cmp.semantic import VariableInfo, Context, Type
from cmp.ast_h import *
from typing import List, Dict
import math

class BaseHulkToCil:
    def __init__(self, context: Context) -> None:
        self.dottypes: List[cil.TypeNode] = []
        self.dotdata: List[cil.DataNode] = []
        self.dotcode: List[cil.FunctionNode] = []
        self.current_type: Type = None
        self.current_method : cil.MethodNode = None
        self.current_function: cil.FunctionNode = None
        self.context: Context = context
        self.string_count = 0
        self._count = 0
        self.internal_count = 0
        self.methods = {}
        self.attrs = {}
    
    @property
    def params(self)-> List[cil.ParamNode]:
        return self.current_function.params
    
    @property
    def localvars(self)-> List[cil.LocalNode]:
        return self.current_function.localvars
    
    @property
    def instructions(self)-> List[cil.InstructionNode]:
        return self.current_function.instructions
    
    def generate_next_string_id(self):
        self.string_count += 1
        return f'string_{self.string_count}'
    
    def generate_next_id(self):
        self._count += 1
        return f'{self._count}'
    
    def get_local(self, name):
        return f'local_{name}'
    
    def register_local(self, vinfo: VariableInfo = None):
        if vinfo.name:
            vinfo.name = f'local_{vinfo.name}'
        else:
            vinfo.name = f'local_{len(self.current_function.localvars)}'
            
        local_node = cil.LocalNode(vinfo.name)
        self.localvars.append(local_node)
        return vinfo.name

    def define_internal_local(self):
        return self.register_local()

    def register_instruction(self, instruction):
        self.instructions.append(instruction)
        return instruction
    
    def to_function_name(self, method_name, type_name):
        # example: Main_main
        return f'{type_name}_{method_name}'
    
    def to_data_name(self, type_name, value):
        return f'{type_name}_{value}'
    
    def to_attr_name(self, type_name, attr_name):
        return f'{type_name}_{attr_name}'
    
    def register_function(self, function_name):
        function_node = cil.FunctionNode(function_name, [], [], [])
        self.dotcode.append(function_node)
        return function_node
    
    def get_method_id(self, method_name, type_name):
        method_id, _ = self.methods[type_name][method_name]
        return method_id
    
    def register_type(self, name):
        type_node = cil.TypeNode(name)
        self.dottypes.append(type_node)
        return type_node

    def register_data(self, value):
        vname = f'data_{len(self.dotdata)}'
        data_node = cil.DataNode(vname, value)
        self.dotdata.append(data_node)
        return data_node
    
    def internal_param_vname(self, vname):
        self.internal_count += 1
        return f'param_{vname}'
    
    def register_param(self, vinfo: VariableInfo):
        vinfo.name = self.internal_param_vname(vinfo.name)
        arg_node = cil.ParamNode(vinfo.name)
        self.params.append(arg_node)
        return vinfo.name
    
    def is_attribute(self, vname):
        return vname not in [p.name for p in self.params] + [l.name for l in self.localvars]
    
    def add_builtin_main(self):
        builtin_types = ["Object", "Number", "String", "Boolean"]
        for typex in builtin_types:
            self.current_function = cil.FunctionNode(self.to_function_name('main', typex), [], [], [])
            self.params.append(cil.ParamNode('self'))
            self.register_instruction(cil.ReturnNode('self'))
            self.dotcode.append(self.current_function)
    
    def build_main(self, node: TypeDeclaration):
        self.current_function = self.register_function(self.to_function_name('main', node.identifier))
        
        self.params.append(cil.ParamNode('self'))
        self.current_type.define_method('main', [], [], 'Object')
        
        for attr, (_, attr_type) in self.attrs[self.current_type.name].items():
            instance = self.define_internal_local()
            self.register_instruction(cil.ArgNode('self'))
            self.register_instruction(cil.StaticCallNode(self.to_function_name(f'{attr}_main', attr_type), instance))
            self.register_instruction(cil.SetAttribNode('self', self.to_attr_name(node.identifier,attr), instance, node.identifier))

        self.register_instruction(cil.ReturnNode('self'))
        
    

class HulkToCil(BaseHulkToCil):
    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(Program)
    def visit (self, node: Program, scope):
        self.dotdata.append(cil.DataNode('pi', math.pi))
        self.current_function = self.register_function('main')
        self.current_vars: Dict[str, VariableInfo] = {}
        # ?arriba así ?
        # instance = self.define_internal_local()
        # result = self.define_internal_local()
        
        # main_method_name = self.to_function_name('main', 'Main')
        
        # self.register_instruction(cil.AllocateNode('Main', instance))
        # self.register_instruction(cil.ArgNode(instance))
        # self.register_instruction(cil.StaticCallNode(main_method_name, result))
        # self.register_instruction(cil.ReturnNode(0))
        # self.current_function = self.register_function('main') #? dudoso esto
        # self.current_type = self.context.get_type('Global')

        for decl in node.program_decl_list:
            self.visit(decl, scope)
        return cil.ProgramNode(self.dottypes, self.dotdata, self.dotcode)
    
    @visitor.when(VarInit)
    def visit(self, node: VarInit, scope: Scope):
        var_type = node.type_downcast if node.type_downcast != None else node.expression.__class__.__name__ # esto es un parche
        # var_type = node.expression
        # self.current_function = self.register_function("var_init_function") # ? hace falta esto?
        print('!!!!!!!!!!!!!!AQUIIII VARRRRRRRRR')
        print(node.expression)
        var = self.register_local(VariableInfo(node.identifier, self.context.get_type(var_type)))
        self.current_vars[node.identifier] = var
        value = self.visit(node.expression, scope)
        self.register_instruction(cil.AssignNode(var, value))
        return var
    
    @visitor.when(VarDeclaration)
    def visit(self, node: VarDeclaration, scope: Scope):
        new_scope = Scope(scope)
        for var_init in node.var_init_list:
            self.visit(var_init, new_scope)
        return self.visit(node.body, new_scope)
    
    @visitor.when(VarUse)
    def visit(self, node: VarUse, scope: Scope):
        # print('!!!!!!!!!!!!!!AQUIIII')
        # print(self.current_vars[node.identifier]+ "aaaa ??")
        return self.current_vars[node.identifier]

    @visitor.when(Add)
    def visit(self, node: VarUse, scope: Scope):
        # self.current_function = self.register_function("add_function")
        left = self.visit(node.term, scope)
        right = self.visit(node.aritmetic_operation, scope)
        var = self.define_internal_local()   # aquiii
        self.register_instruction(cil.PlusNode(var, left, right))
        return var
    
    @visitor.when(Sub)
    def visit(self, node: Sub, scope: Scope):
        # self.current_function = self.register_function("sub_function")
        left = self.visit(node.term, scope)
        right = self.visit(node.aritmetic_operation, scope)
        var = self.define_internal_local()
        self.register_instruction(cil.MinusNode(var, left, right))
        return var
    
    @visitor.when(Mult)
    def visit(self, node: Mult, scope: Scope):
        # self.current_function = self.register_function("mult_function")
        left = self.visit(node.factor, scope)
        right = self.visit(node.term, scope)
        var = self.define_internal_local()
        self.register_instruction(cil.StarNode(var, left, right))
        return var
    
    @visitor.when(Div)
    def visit(self, node: Div, scope: Scope):
        # self.current_function = self.register_function("div_function")
        left = self.visit(node.factor, scope)
        right = self.visit(node.term, scope)
        var = self.define_internal_local()
        self.register_instruction(cil.DivNode(var, left, right))
        return var
    
    @visitor.when(Number)
    def visit(self, node: Number, scope: Scope):
        # self.register_instruction(cil.ValueNode(node.value))
        return node.value
    
    @visitor.when(Atom)
    def visit(self, node: Atom, scope: Scope):
        # self.register_instruction(cil.ValueNode(node.value))
        return node.value
    
    @visitor.when(Power)
    def visit(self, node: Power, scope: Scope):
        # self.current_function = self.register_function("pow_function")
        base = self.visit(node.base_exponent, scope)
        exp = self.visit(node.factor, scope)
        var = self.define_internal_local()
        self.register_instruction(cil.PowNode(var, base, exp))
        return var
    
    @visitor.when(UnaryBuildInFunction)
    def visit(self, node: UnaryBuildInFunction, scope: Scope):
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
            # print("ARGS: "+ str(arg))
            # print(self.context.get_type(arg))
            self.register_instruction(cil.PrintNode(arg))
            return arg   
    @visitor.when(String)
    def visit(self, node: String, scope: Scope):
        # print("STRING: "+node.value)
        return node.value    
    
    # @visitor.when(TypeDeclaration)
        
    