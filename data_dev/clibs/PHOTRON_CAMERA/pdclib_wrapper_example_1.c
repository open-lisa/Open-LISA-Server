#include <stdio.h>
#include <Windows.h>
#include <Windows.h>

/*
unsigned long PDC_Init(
    unsigned long *pErrorCode
)
*/

typedef UINT (CALLBACK* PDC_INIT_FUNCTION_DLL)(UINT*);

int main(int argc, char * argv[])
{
    HINSTANCE libHandle;                        // Handle to DLL
    PDC_INIT_FUNCTION_DLL pdc_init_function;    // Function pointer
    UINT error_code, return_value;

    libHandle = LoadLibrary("PDCLIB.dll");
    if (libHandle == NULL) {
        printf("Load failed\n");
        return 1;
    }

    pdc_init_function = (PDC_INIT_FUNCTION_DLL) GetProcAddress(libHandle, "PDC_Init");
    if (pdc_init_function == NULL) {
        printf("GetProcAddress failed\n");
        printf("%d\n", GetLastError());
        return 1;
    }

    return_value = pdc_init_function(&error_code);
    printf("Return value is %d\n", return_value);
    printf("Error code is %d\n", error_code);
    return 0;
}