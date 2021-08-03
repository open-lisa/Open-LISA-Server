#ifdef _MSC_VER
    #define EXPORT_SYMBOL __declspec(dllexport)
#else
    #define EXPORT_SYMBOL
#endif

EXPORT_SYMBOL int init(int int_param, float float_param);
EXPORT_SYMBOL int get_image(char * file_path);
EXPORT_SYMBOL int close(void);