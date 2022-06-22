rm *.dll *.so *.o
gcc -c -Wall -Werror -fpic mock_lib.c \
  && gcc -shared -o mock_lib.so mock_lib.o \
  && gcc -shared -o mock_lib.dll mock_lib.o