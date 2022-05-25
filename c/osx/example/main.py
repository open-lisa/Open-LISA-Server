import ctypes
import sys

if __name__ == "__main__":
    # Load the shared library into c types.
    if sys.platform.startswith("win"):
        c_lib = ctypes.CDLL("mult.dll")
    else:
        c_lib = ctypes.CDLL("libmult.so")
    x, y = 6, 2.3
    # You need tell ctypes that the function returns a float
    c_lib.mult.restype = ctypes.c_float
    answer = c_lib["mult"](x, ctypes.c_float(y))
    print(f"In Python: int: {x} float {y:.1f} return val {answer:.1f}")

