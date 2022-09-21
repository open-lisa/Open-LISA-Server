#include <stdio.h>
#include <Windows.h>
#include <errno.h>
#include "include/PDCDEV.h"
#include "include/PDCVALUE.h"
#include "include/PDCSTR.h"
#include "include/PDCERROR.h"

/*	Wrapper Return Values	*/
#define	PDC_WRAPPER_SUCCEEDED				0
#define	PDC_WRAPPER_FAILED					-1

/*
    unsigned long PDC_Init(
        unsigned long *pErrorCode
    )
*/
typedef UINT (CALLBACK* PDC_INIT_FUNCTION_DLL)(UINT*);

/*
unsigned long PDC_DetectDevice(
    unsigned long nInterfaceCode
    unsigned long *pDetectNo
    unsigned long nDetectNum
    unsigned long nDetectParam
    PPDC_DETECT_NUM_INFO pDetectNumInfo
    unsigned long *pErrorCode
)
*/
typedef UINT (CALLBACK* PDC_DETECT_DEVICE_FUNCTION_DLL)(UINT, UINT*, UINT, UINT, PDC_DETECT_NUM_INFO*, UINT*);

FILE* open_tmp_file_buffer(const char * tmp_file_buffer) {
    FILE* output_file = fopen(tmp_file_buffer, "wb");
    if (output_file == NULL) {
        fprintf(stderr, "error opening temp file buffer: %s\n", strerror(errno));
    }

    return output_file;
}

/*
    tmp_file_buffer:
        success case (PDC_WRAPPER_SUCCEEDED):
            4 bytes for function return_value
            4 bytes for error_code
        error case (PDC_WRAPPER_FAILED):
            string with error message
*/
int pdc_init(const char * tmp_file_buffer) {
    HINSTANCE libHandle;

    PDC_INIT_FUNCTION_DLL pdc_init_function;

    UINT error_code, return_value;

    FILE* output_file = open_tmp_file_buffer(tmp_file_buffer);
    if (output_file == NULL) {
        return PDC_WRAPPER_FAILED;
    }

    libHandle = LoadLibrary("PDCLIB.dll");
    if (libHandle == NULL) {
        const char * message = "error loading library PDCLIB.dll";
        fwrite(message, sizeof(char), strlen(message), output_file);
        fclose(output_file);
        return PDC_WRAPPER_FAILED;
    }

    pdc_init_function = (PDC_INIT_FUNCTION_DLL) GetProcAddress(libHandle, "PDC_Init");
    if (pdc_init_function == NULL) {
        const char * message = "GetProcAddress failed loading PDC_Init function";
        fwrite(message, sizeof(char), strlen(message), output_file);
        fclose(output_file);
        return PDC_WRAPPER_FAILED;
    }

    return_value = pdc_init_function(&error_code);

    fwrite(&return_value, sizeof(UINT), 1, output_file);
    fwrite(&error_code, sizeof(UINT), 1, output_file);
    fclose(output_file);

    return PDC_WRAPPER_SUCCEEDED;
}

/*
    tmp_file_buffer:
        success case (PDC_WRAPPER_SUCCEEDED):
            4 bytes for function return_value
            if return_value is success:
                4 bytes for m_ndevice_code
                4 bytes for m_ntmp_device_no
                4 bytes for m_ninterface_code
        error case (PDC_WRAPPER_FAILED):
            string with error message
*/
int pdc_detect_device(UINT ip, const char * tmp_file_buffer) {
    HINSTANCE libHandle;

    PDC_DETECT_DEVICE_FUNCTION_DLL pdc_detect_device_function;

    UINT error_code, return_value;
    UINT IPList[1];
    IPList[0] = ip;
    PDC_DETECT_NUM_INFO pdc_detect_num_info;

    FILE* output_file = open_tmp_file_buffer(tmp_file_buffer);
    if (output_file == NULL) {
        return PDC_WRAPPER_FAILED;
    }

    libHandle = LoadLibrary("PDCLIB.dll");
    if (libHandle == NULL) {
        const char * message = "error loading library PDCLIB.dll";
        fwrite(message, sizeof(char), strlen(message), output_file);
        fclose(output_file);
        return PDC_WRAPPER_FAILED;
    }

    pdc_detect_device_function = (PDC_DETECT_DEVICE_FUNCTION_DLL) GetProcAddress(libHandle, "PDC_DetectDevice");
    if (pdc_detect_device_function == NULL) {
        const char * message = "GetProcAddress failed loading PDC_Init function";
        fwrite(message, sizeof(char), strlen(message), output_file);
        fclose(output_file);
        return PDC_WRAPPER_FAILED;
    }

    return_value = pdc_detect_device_function(PDC_INTTYPE_G_ETHER, IPList, 1, PDC_DETECT_NORMAL, &pdc_detect_num_info, &error_code);

    fwrite(&return_value, sizeof(UINT), 1, output_file);
    if (return_value == PDC_FAILED) {
        return PDC_WRAPPER_SUCCEEDED;
    }

    // We assume that only 1 device will be detected
    if (pdc_detect_num_info.m_nDeviceNum != 1 ) {
        const char * message = "Not detected 1 device";
        fwrite(message, sizeof(char), strlen(message), output_file);
        return PDC_WRAPPER_FAILED;
    }
    PDC_DETECT_INFO pdc_detect_info = pdc_detect_num_info.m_DetectInfo[0];

    UINT m_ndevice_code = pdc_detect_info.m_nDeviceCode;
    UINT m_ntmp_device_no = pdc_detect_info.m_nTmpDeviceNo;
    UINT m_ninterface_code = pdc_detect_info.m_nInterfaceCode;

    fwrite(&m_ndevice_code, sizeof(UINT), 1, output_file);
    fwrite(&m_ntmp_device_no, sizeof(UINT), 1, output_file);
    fwrite(&m_ninterface_code, sizeof(UINT), 1, output_file);

    return PDC_WRAPPER_SUCCEEDED;
}