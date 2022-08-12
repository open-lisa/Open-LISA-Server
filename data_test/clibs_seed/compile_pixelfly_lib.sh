rm libpixelflyqe.dll libpixelflyqe.so pixelflyqe.o
gcc -c -Wall -Werror -fpic pixelflyqe.c \
  && gcc -shared -o libpixelflyqe.so pixelflyqe.o \
  && gcc -shared -o libpixelflyqe.dll pixelflyqe.o