rm *.dll *.o
x86_64-w64-mingw32-gcc -c -Wall -Werror -fpic mock_lib.c \
  && x86_64-w64-mingw32-gcc -shared -o mock_lib.dll mock_lib.o