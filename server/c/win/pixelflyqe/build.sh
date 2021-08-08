rm *.so *.o
gcc -c -Wall -Werror -fpic pixelflyqe.c && gcc -shared -o libpixelflyqe.dll pixelflyqe.o