# Calling C from Python

This examples are based on https://realpython.com/python-bindings-overview/ check the code of the article in this [repository](https://github.com/realpython/materials/tree/master/python-bindings?__s=r78ehzuts6ons1inr7pe)

## OSX
1. Create the C lib for the `mult.c` function (this commands will generate `libmult.so` and `mult.o`):
```bash
gcc -c -Wall -Werror -fpic mult.c
gcc -shared -o libmult.so mult.o
```
2. Run the Python scriptxw
