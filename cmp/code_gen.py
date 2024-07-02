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

class MIPSTranslator:
    def op_abs(src, dest):
        return f"abs {dest}, {src}"
    
    def op_add(r1, r2, dest):
        return f"add {dest}, {r1}, {r2}"
    
    def op_addi(r1, imm, dest):
        return f"addi {dest}, {r1}, {imm}"
    
    def op_addiu(r1, imm, dest):
        return f"addiu {dest}, {r1}, {imm}"
    
    def op_addu(r1, r2, dest):
        return f"addu {dest}, {r1}, {r2}"
    
    def op_and(r1, r2, dest):
        return f"and {dest}, {r1}, {r2}"

    def op_div(r1, r2, dest):
        return f"div {dest}, {r1}, {r2}"
    
    def op_divu(r1, r2, dest):
        return f"divu {dest}, {r1}, {r2}"
    
    def op_lw(r1, offset, dest):
        return f"lw {dest}, {offset}({r1})"
    
    def op_move(r1, dest):
        return f"move {dest}, {r1}"

    def op_mult(r1, r2, dest):
        return f"mult {dest}, {r1}, {r2}"
    
    def op_multu(r1, r2, dest):
        return f"multu {dest}, {r1}, {r2}"
    
    def op_neg(r1, dest):
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
        return f"sw {dest}, {offset}({r1})"

class HulkMIPSGenerator:
    def __init__(self):
        self._registers = list(REG_TEMP)
        self._used_registers = []
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
        reg = self.unused_registers.pop()
        self.allocate_register(reg)
        return reg
    def clear_registers(self):
        self._used_registers.clear()
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

        for op_def in node.dotcode:
            # print(type(op_def))
            self.visit(op_def)

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
        for local in node.localvars:
            print(f"LOCAL {local.name}")
        
        # allocate params and locals in stack (stack grows backwards)
        print(MIPSTranslator.op_addiu(REG_STACK_POINTER, REG_STACK_POINTER, -4 * (len(node.params) + len(node.localvars))))

        # store sp in ra
        print(MIPSTranslator.op_sw(REG_STACK_POINTER, 0, REG_RETURN_ADDR))
        print(MIPSTranslator.op_addiu(REG_STACK_POINTER, REG_STACK_POINTER, -4))

        # store sp in saved fp
        print(MIPSTranslator.op_sw(REG_STACK_POINTER, 0, old_fp))
        print(MIPSTranslator.op_addiu(REG_STACK_POINTER, REG_STACK_POINTER, -4))

        for instruction in node.instructions:
            self.visit(instruction)

        # TODO: generate procedure function code

        # must restore locals context
        self.params = params_snapshot 
        self.locals = locals_snapshot

    @visitor.when(cil_h.LocalNode)
    def visit(self, node: cil_h.LocalNode):
        pass
    
    @visitor.when(cil_h.PlusNode)
    def visit(self, node: cil_h.PlusNode):
        print(f"{node.dest} = {node.left} + {node.right}")

        print(node.left)
        print(node.right)
        print(self.locals)
        
        # load 3 address to registers
        dest_reg = self.get_unused_register()
        left_reg = self.get_unused_register()
        right_reg = self.get_unused_register()

        # get operands offsets
        left_offset = self.get_stack_offset(node.left)
        right_offset = self.get_stack_offset(node.right)

        # load values to registers
        print(MIPSTranslator.op_lw(REG_FRAME_POINTER, left_offset, left_reg))
        print(MIPSTranslator.op_lw(REG_FRAME_POINTER, right_offset, right_reg))

        # add register values
        print(MIPSTranslator.op_add(left_reg, right_reg, dest_reg))

        # get dest offset
        dest_offset = self.get_stack_offset(node.dest)

        # store value to local
        print(MIPSTranslator.op_sw(dest_reg, dest_offset, REG_FRAME_POINTER))

        # TODO: implement global register state
        # clear registers
        self.clear_registers()

    @visitor.when(cil_h.MinusNode)
    def visit(self, node: cil_h.MinusNode):
        print(f"{node.dest} = {node.left} - {node.right}")
        
        # load 3 address to registers
        dest_reg = self.get_unused_register()
        left_reg = self.get_unused_register()
        right_reg = self.get_unused_register()

        # get operands offsets
        left_offset = self.get_stack_offset(node.left)
        right_offset = self.get_stack_offset(node.right)

        # load values to registers
        print(MIPSTranslator.op_lw(REG_FRAME_POINTER, left_offset, left_reg))
        print(MIPSTranslator.op_lw(REG_FRAME_POINTER, right_offset, right_reg))

        # add register values
        print(MIPSTranslator.op_sub(left_reg, right_reg, dest_reg))

        # get dest offset
        dest_offset = self.get_stack_offset(node.dest)

        # store value to local
        print(MIPSTranslator.op_sw(dest_reg, dest_offset, REG_FRAME_POINTER))

        # TODO: implement global register state
        # clear registers
        self.clear_registers()