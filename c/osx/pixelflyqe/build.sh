rm *.so *.o
gcc -c -Wall -Werror -fpic pixelflyqe.c && gcc -shared -o libpixelflyqe.so pixelflyqe.o