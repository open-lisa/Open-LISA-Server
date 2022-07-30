rm *.so *.o
gcc -c -Wall -Werror -fpic mock_lib.c \
  && gcc -shared -o mock_lib.so mock_lib.o