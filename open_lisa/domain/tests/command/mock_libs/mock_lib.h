#ifdef _MSC_VER
    #define EXPORT_SYMBOL __declspec(dllexport)
#else
    #define EXPORT_SYMBOL
#endif

EXPORT_SYMBOL float multiply(float, float);
EXPORT_SYMBOL int sum(int, int);
EXPORT_SYMBOL void create_file(char*);
EXPORT_SYMBOL char* echo(char*);
EXPORT_SYMBOL int copy_image(const char *, const char*);