from cmp import visitor
from cmp import cil_h

REG_ZERO = "$zero" # constant 0
REG_RESERVED = "$at" # assembler reserved

REG_GLOBAL = "$gp" # global area pointer
REG_STACK_POINTER = "$sp" # stack pointer
REG_FRAME_POINTER = "$fp" # fram pointer
REG_RETURN_ADDR = "$ra" # return address

# os kernel reserved
REG_OS_RESERVED_0 = "$k0"
REG_OS_RESERVED_1 = "$k1"

# function return registers
REG_VALUE_0 = "$v0"
REG_VALUE_1 = "$v1"

# argument registers
REG_ARG = ["$a0","$a1","$a2","$a3"]

# temporal registers (not preserved)
REG_TEMP = ["$t0","$t1","$t2","$t3","$t4","$t5","$t6","$t7","$t8","$t9"]

# temporal saved registers (preserved)
REG_SAV = ["$s0","$s1","$s2","$s3","$s4","$s5","$s6","$s7"]

# special float register for syscall print float
REG_FLOAT_OUT = "f12"

# const MIPS char value offset
CHAR_OFFSET = 8

SYSCALL_PRINT_INT = 1
SYSCALL_PRINT_FLOAT = 2
SYSCALL_PRINT_STR = 4
SYSCALL_EXIT = 10

class MIPSTranslator:
    def op_abs(r1, dest):
        return f"abs {dest}, {r1}"
    
    def op_abs_s(r1, dest):
        return f"abs.s {dest}, {r1}"
    
    def op_add(r1, r2, dest):
        return f"add {dest}, {r1}, {r2}"
    
    def op_add_s(r1, r2, dest):
        return f"add.s {dest}, {r1}, {r2}"
    
    def op_addi(r1, imm, dest):
        return f"addi {dest}, {r1}, {imm}"
    
    def op_addiu(r1, imm, dest):
        return f"addiu {dest}, {r1}, {imm}"
    
    def op_addu(r1, r2, dest):
        return f"addu {dest}, {r1}, {r2}"
    
    def op_and(r1, r2, dest):
        return f"and {dest}, {r1}, {r2}"
    
    def op_c_lt_s(r1, r2):
        return f"c.lt.s {r1}, {r2}"
    
    def op_cvt_s_w(r1, dest):
        return f"cvt.s.w {dest}, {r1}"

    def op_div(r1, r2, dest):
        return f"div {dest}, {r1}, {r2}"
    
    def op_div_s(r1, r2, dest):
        return f"div.s {dest}, {r1}, {r2}"
    
    def op_divu(r1, r2, dest):
        return f"divu {dest}, {r1}, {r2}"
    
    def op_li(imm, dest):
        return f"li {dest}, {imm}"
    
    def op_li_s(imm, dest):
        return f"li.s {dest}, {imm}"
    
    def op_lw(r1, offset, dest):
        return f"lw {dest}, {offset}({r1})"
    
    def op_move(r1, dest):
        return f"move {dest}, {r1}"
    
    def op_mov_s(r1, dest):
        return f"mov.s {dest}, {r1}"

    def op_mul(r1, r2, dest):
        return f"mul {dest}, {r1}, {r2}"
    
    def op_mul_s(r1, r2, dest):
        return f"mul.s {dest}, {r1}, {r2}"
    
    def op_multu(r1, r2, dest):
        return f"multu {dest}, {r1}, {r2}"
    
    def op_neg(r1, dest):
        return f"neg {dest}, {r1}"
    
    def op_neg_s(r1, dest):
        return f"neg {dest}, {r1}"

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
    
    def op_sub(r1, r2, dest):
        return f"sub {dest}, {r1}, {r2}"
    
    def op_sw(r1, offset, dest):
        return f"sw {r1}, {offset}({dest})"
    
    def op_syscall():
        return "syscall"
    

class HulkMIPSGenerator:
    def __init__(self):
        self._registers = list(REG_TEMP)
        self._float_registers = list([f"$f{i}" for i in range(32) if i != 12]) # special register f12 not included
        self._used_registers = []
        self._used_float_registers = []
        # stack = params + locals
        self._params = []
        self._locals = []

    # register managing
    @property
    def unused_registers(self) -> set:
        return set(self._registers).difference(set(self._used_registers))
    
    def allocate_register(self, register):
        self._used_registers.append(register)
        
    def get_unused_register(self):
        reg = next(iter(self.unused_registers))
        self.allocate_register(reg)
        return reg
    
    def clear_registers(self):
        self._used_registers.clear()

    @property
    def unused_float_registers(self) -> set:
        return set(self._float_registers).difference(set(self._used_float_registers))
    
    def allocate_float_register(self, register):
        self._used_float_registers.append(register)

    def get_unused_float_register(self):
        reg = next(iter(self.unused_float_registers))
        self.allocate_float_register(reg)
        return reg
    
    def clear_float_registers(self):
        self._used_float_registers.clear()

    # end register managing

    # stack managing
    @property
    def params(self):
        return self._params
    @params.setter
    def params(self, value):
        self._params = value
    
    @property
    def locals(self):
        return self._locals
    @locals.setter
    def locals(self, value):
        self._locals = value
    
    # offset = sp - 4 * index
    def get_stack_offset(self, elem):
        if elem in self.params:
            return 4 * self.params.index(elem)
        elif elem in self.locals:
            return 4 * (len(self.params) + self.locals.index(elem))
    # end stack managing

    # builtins
    def generate_sin_builtin(self):
        print("sin:")
        n_reg = self.get_unused_register()
        n_next_reg = self.get_unused_register()
        n_float_reg = self.get_unused_float_register()
        epsilon_freg = self.get_unused_float_register()
        # TODO: load x
        param_freg = self.get_unused_float_register()
        mult_freg = self.get_unused_float_register()
        compare_freg = self.get_unused_float_register()
        abs_freg = self.get_unused_float_register()

        print(MIPSTranslator.op_li_s("1.0e-6", epsilon_freg))
        # TODO: change for lw.s
        print(MIPSTranslator.op_li_s("xvalue", param_freg))
        print(MIPSTranslator.op_mul_s(param_freg, param_freg, mult_freg))
        print(MIPSTranslator.op_mov_s(param_freg, REG_FLOAT_OUT))

        print("sin_for:")
        print(MIPSTranslator.op_abs_s(abs_freg, param_freg))
        print(MIPSTranslator.op_c_lt_s(param_freg, epsilon_freg))
        print("bc1t end_sin_for")
        
        print(MIPSTranslator.op_addiu(n_reg, -1, n_next_reg))
        print(MIPSTranslator.op_mul(n_next_reg, n_reg, n_next_reg))
        print(f"mtc1 {n_next_reg}, {n_float_reg}")
        print(MIPSTranslator.op_cvt_s_w(n_float_reg, n_float_reg))
        print(MIPSTranslator.op_div_s(n_float_reg, mult_freg, n_float_reg))
        print(MIPSTranslator.op_neg_s(n_float_reg, n_float_reg))
        print(MIPSTranslator.op_mul_s(param_freg, n_float_reg, param_freg))
        print(MIPSTranslator.op_add_s(REG_FLOAT_OUT, param_freg, REG_FLOAT_OUT))

        print(MIPSTranslator.op_addiu(n_reg, 2, n_reg))
        print("b sin_for")
        print("end_sin_for")
        print(MIPSTranslator.op_li(SYSCALL_PRINT_FLOAT, REG_VALUE_0)) # syscall print float
        print(MIPSTranslator.op_syscall())
    # end builtins

    def three_addr_op(self, op, node):
        # load 3 address to registers
        dest_reg = self.get_unused_register()
        left_reg = self.get_unused_register()
        right_reg = self.get_unused_register()

        # get operands offsets
        left_offset = self.get_stack_offset(node.left)
        right_offset = self.get_stack_offset(node.right)

        # load values to registers
        if left_offset is not None:
            print(MIPSTranslator.op_lw(REG_FRAME_POINTER, left_offset, left_reg))
        else:
            print(MIPSTranslator.op_li(int(float(node.left)), left_reg))
        if right_offset is not None:
            print(MIPSTranslator.op_lw(REG_FRAME_POINTER, right_offset, right_reg))
        else:
            print(MIPSTranslator.op_li(int(float(node.right)), right_reg))

        # add register values
        print(op(left_reg, right_reg, dest_reg))

        # get dest offset
        dest_offset = self.get_stack_offset(node.dest)

        # store value to local
        print(MIPSTranslator.op_sw(dest_reg, dest_offset, REG_FRAME_POINTER))

        # TODO: implement global register state
        # clear registers
        self.clear_registers()

    @visitor.on('node')
    def visit(self, node, tabs):
        pass
    
    @visitor.when(cil_h.Node)
    def visit(self, node):
        pass   

    @visitor.when(cil_h.ProgramNode)
    def visit(self, node: cil_h.ProgramNode):
        print("visiting cil")
        for type_def in node.dottypes:
            pass

        for data_def in node.dotdata:
            pass

        print("main:")
        for op_def in node.dotcode:
            # print(type(op_def))
            self.visit(op_def)
        print(MIPSTranslator.op_li(SYSCALL_EXIT, REG_VALUE_0))
        print(MIPSTranslator.op_syscall())

    @visitor.when(cil_h.FunctionNode)
    def visit(self, node: cil_h.FunctionNode):
        print(f"visiting function {node.name}")
        # save current state
        params_snapshot = self.params
        locals_snapshot = self.locals

        # change new function state
        self.params = [x.name for x in node.params]
        self.locals = [x.name for x in node.localvars]

        # save fp state
        old_fp = self.get_unused_register()
        print(MIPSTranslator.op_move(REG_FRAME_POINTER, old_fp))

        # set new frame pointer context
        print(MIPSTranslator.op_move(REG_STACK_POINTER, REG_FRAME_POINTER))

        # for param in node.params:
        #     print(param)
        # for local in node.localvars:
        #     print(f"LOCAL {local.name}")
        
        # allocate params and locals in stack (stack grows backwards)
        print(MIPSTranslator.op_addiu(REG_STACK_POINTER, -4 * (len(node.params) + len(node.localvars)), REG_STACK_POINTER))

        # store sp in ra
        print(MIPSTranslator.op_sw(REG_STACK_POINTER, 0, REG_RETURN_ADDR))
        print(MIPSTranslator.op_addiu(REG_STACK_POINTER, -4, REG_STACK_POINTER))

        # store sp in saved fp
        print(MIPSTranslator.op_sw(old_fp, 0, REG_STACK_POINTER))
        print(MIPSTranslator.op_addiu(REG_STACK_POINTER, -4, REG_STACK_POINTER))

        for instruction in node.instructions:
            self.visit(instruction)

        # TODO: generate procedure function code

        # must restore locals context
        self.params = params_snapshot 
        self.locals = locals_snapshot
    
    @visitor.when(cil_h.AssignNode)
    def visit(self, node: cil_h.AssignNode):
        reg = self.get_unused_register()

        if node.type.name in ("Number", "Boolean"):
            print(MIPSTranslator.op_li(int(float(node.source)), reg))
        elif node.type.name == "String":
            print(node.source)
        else:
            source_offset = self.get_stack_offset(node.source)
            print(MIPSTranslator.op_lw(REG_FRAME_POINTER, source_offset, reg))

        dest_offset = self.get_stack_offset(node.dest)
        print(MIPSTranslator.op_sw(reg, dest_offset, REG_FRAME_POINTER))

        self.clear_registers()

    @visitor.when(cil_h.LocalNode)
    def visit(self, node: cil_h.LocalNode):
        pass
    
    @visitor.when(cil_h.PlusNode)
    def visit(self, node: cil_h.PlusNode):
        # print(f"{node.dest} = {node.left} + {node.right}")
        self.three_addr_op(MIPSTranslator.op_add, node)
        

    @visitor.when(cil_h.MinusNode)
    def visit(self, node: cil_h.MinusNode):
        # print(f"{node.dest} = {node.left} - {node.right}")
        self.three_addr_op(MIPSTranslator.op_sub, node)

    @visitor.when(cil_h.StarNode)
    def visit(self, node: cil_h.StarNode):
        # print(f"{node.dest} = {node.left} * {node.right}")
        self.three_addr_op(MIPSTranslator.op_mul, node)

    @visitor.when(cil_h.DivNode)
    def visit(self, node: cil_h.DivNode):
        # print(f"{node.dest} = {node.left} / {node.right}")
        self.three_addr_op(MIPSTranslator.op_div, node)
    
    @visitor.when(cil_h.PrintNode)
    def visit(self, node: cil_h.PrintNode):
        straddr_offset = self.get_stack_offset(node.str_addr)
        value = f"{node.str_addr}"
        print(MIPSTranslator.op_lw(REG_FRAME_POINTER, straddr_offset, REG_ARG[0]))
        # print(MIPSTranslator.op_lw(REG_ARG[0], CHAR_OFFSET, REG_ARG[0]))
        print(MIPSTranslator.op_li(SYSCALL_PRINT_INT, REG_VALUE_0))
        print(MIPSTranslator.op_syscall())