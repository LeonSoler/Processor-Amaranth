from ast import With
from amaranth import *
from amaranth.sim import *
from enum import Enum, unique

class ALU(Elaboratable):
    def __init__(self):
        self.i_sel = Signal(3)
        self.i_a = Signal(32)
        self.i_b = Signal(32)
        self.o_result = Signal(32)
        self.o_zero = Signal(1)
    
    def ports(self):
        return [self.i_sel,self.i_a,self.i_b,self.o_result,self.o_zero]

    def elaborate(self, platfrom):
        m = Module()
        
        with m.Switch(self.i_sel):
            with m.Case(0b000):
                m.d.comb +=self.o_result.eq(self.i_a & self.i_b)
            with m.Case(0b001):
                m.d.comb +=self.o_result.eq(self.i_a | self.i_b)
            with m.Case(0b010):
                m.d.comb +=self.o_result.eq(self.i_a + self.i_b)
            with m.Case(0b110):
                m.d.comb +=self.o_result.eq(self.i_a - self.i_b)
            with m.Case(0b111):
                with m.If(self.i_a < self.i_b):
                    m.d.comb +=self.o_result.eq(0x00000001)  
                with m.If(self.i_a >= self.i_b):  
                    m.d.comb +=self.o_result.eq(0x00000000)  
            with m.Case(0b100):
                m.d.comb +=self.o_result.eq(self.i_b.shift_left(16))
            with m.Default():
                m.d.comb +=self.o_result.eq(0x00000000)

        with m.If(self.o_result==0x00000001):
            self.o_zero.eq(1)
        with m.Else():
            self.o_zero.eq(0)

        return m

def proc():
    yield dut.i_sel.eq(0b000)
    yield dut.i_a.eq(0x00000001)
    yield dut.i_b.eq(0x00000000)
    yield Delay(1e-9)
    yield Settle()

    yield dut.i_sel.eq(0b010)
    yield dut.i_a.eq(0x00000004)
    yield dut.i_b.eq(0x00000000)
    yield Delay(1e-9)
    yield Settle()

    yield dut.i_sel.eq(0b110)
    yield dut.i_a.eq(0x00000001)
    yield dut.i_b.eq(0x00000001)
    yield Delay(1e-9)
    yield Settle()

    yield dut.i_sel.eq(0b111)
    yield dut.i_a.eq(0x00000004)
    yield dut.i_b.eq(0x00000002)
    yield Delay(1e-9)
    yield Settle()

    yield dut.i_sel.eq(0b100)
    yield dut.i_b.eq(0x00000001)
    yield Delay(1e-9)
    yield Settle()

    yield dut.i_sel.eq(0b100)
    yield dut.i_b.eq(0x10000000)
    yield Delay(1e-9)
    yield Settle()

dut = ALU()
sim = Simulator(dut)
sim.add_process(proc)
with sim.write_vcd("alu.vcd"):
    sim.run()
    

    

