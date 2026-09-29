import sympy as sp
from sympy.parsing.sympy_parser import parse_expr

# Define symbolic variables representing LoRA
h, x, alpha, r = sp.symbols("h x alpha r")
W_0 = sp.MatrixSymbol("W_0", 4, 4)
A = sp.MatrixSymbol("A", 2, 4)
B = sp.MatrixSymbol("B", 4, 2)

# Compute low-rank adaptation matrix update: ΔW = (α/r) * B * A
delta_W = (alpha / r) * (B * A)

# Output equivalent formulation symbolically
print("Base linear projection:", W_0)
print("Adapted projection ΔW:", delta_W)