#include <stdio.h>
#include <Windows.h>
#include "include/PDCDEV.h"
#include "include/PDCVALUE.h"
#include "include/PDCSTR.h"

/*
IN-DLL FUNCTION
unsigned long PDC_DetectDevice(
    unsigned long nInterfaceCode
    unsigned long *pDetectNo
    unsigned long nDetectNum
    unsigned long nDetectParam
    PPDC_DETECT_NUM_INFO pDetectNumInfo
    unsigned long *pErrorCode
)
*/

typedef UINT (CALLBACK* PDC_DETECT_DEVICE_FUNCTION_DLL)(UINT, long unsigned int*, UINT, UINT, PPDC_DETECT_NUM_INFO, UINT*);

int main(int argc, char * argv[])
{
    HINSTANCE libHandle;                                 // Handle to DLL
    PDC_DETECT_DEVICE_FUNCTION_DLL pdc_init_function;    // Function pointer
    UINT error_code, return_value;
    PDC_DETECT_NUM_INFO DetectNumInfo;

    unsigned long IPList[PDC_MAX_DEVICE];
    IPList[0] = 0xC0A8000A; /* 192.168.0.10 */
    IPList[1] = 0xC0A8000B; /* 192.168.0.11 */

    libHandle = LoadLibrary("PDCLIB.dll");
    if (libHandle == NULL) {
        printf("Load failed\n");
        return 1;
    }

    pdc_init_function = (PDC_DETECT_DEVICE_FUNCTION_DLL) GetProcAddress(libHandle, "PDC_DetectDevice");
    if (pdc_init_function == NULL) {
        printf("GetProcAddress failed\n");
        printf("%d\n", GetLastError());
        return 1;
    }

    return_value = pdc_init_function(PDC_INTTYPE_G_ETHER, IPList, 2, PDC_DETECT_NORMAL, &DetectNumInfo, &error_code);
    printf("Return value is %d\n", return_value);
    printf("Error code is %d\n", error_code);
    return 0;
}