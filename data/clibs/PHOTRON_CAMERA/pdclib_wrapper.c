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

/*
unsigned long PDC_OpenDevice(
    PPDC_DETECT_INFO pDetectInfo
    unsigned long *pDeviceNo
    unsigned long *pErrorCode
)
*/
typedef UINT (CALLBACK* PDC_OPEN_DEVICE_FUNCTION_DLL)(PDC_DETECT_INFO*, UINT*, UINT*);

/*
unsigned long PDC_CloseDevice(
    unsigned long nDeviceNo
    unsigned long *pErrorCode
)
*/
typedef UINT (CALLBACK* PDC_CLOSE_DEVICE_FUNCTION_DLL)(UINT, UINT*);

/*
unsigned long PDC_GetDeviceName(
    unsigned long nDeviceNo
    unsigned long nChildNo
    TCHAR *pStrName
    unsigned long *pErrorCode
)
*/
typedef UINT (CALLBACK* PDC_GET_DEVICE_NAME_FUNCTION_DLL)(UINT, UINT, TCHAR*, UINT*);

/*
unsigned long PDC_GetStatus(
    unsigned long nDeviceNo
    unsigned long *pStatus
    unsigned long *pErrorCode
)
*/
typedef UINT (CALLBACK* PDC_GET_STATUS_FUNCTION_DLL)(UINT, UINT*, UINT*);

/*
unsigned long PDC_GetExistChildDeviceList(
    unsigned long nDeviceNo
    unsigned long *pSize
    unsigned long *pList
    unsigned long *pErrorCode
)
*/
typedef UINT (CALLBACK* PDC_GET_EXIST_CHILD_DEVICE_LIST_FUNCTION_DLL)(UINT, UINT*, UINT*, UINT*);

/*
unsigned long PDC_GetMaxChildDeviceCount(
    unsigned long nDeviceNo
    unsigned long *pCount
    unsigned long *pErrorCode
)
*/
typedef UINT (CALLBACK* PDC_GET_MAX_CHILD_DEVICE_COUNT_FUNCTION_DLL)(UINT, UINT*, UINT*);

/*
unsigned long PDC_GetMaxBitDepth(
    unsigned long nDeviceNo
    unsigned long nChildNo
    unsigned long *pDepth
    unsigned long *pErrorCode
)
*/
typedef UINT (CALLBACK* PDC_GET_MAX_BIT_DEPTH_FUNCTION_DLL)(UINT, UINT, UINT*, UINT*);

/*
unsigned long PDC_GetBitDepth(
    unsigned long nDeviceNo
    unsigned long nChildNo
    char *pDepth
    unsigned long *pErrorCode
)
*/
typedef UINT (CALLBACK* PDC_GET_BIT_DEPTH_FUNCTION_DLL)(UINT, UINT, char*, UINT*);

/*
This function retrieves the color/monochromatic information of the specified child device.

unsigned long PDC_GetColorType(
    unsigned long nDeviceNo
    unsigned long nChildNo
    char *pMode
    unsigned long *pErrorCode
)
*/
typedef UINT (CALLBACK* PDC_GET_COLOR_TYPE_FUNCTION_DLL)(UINT, UINT, char*, UINT*);

/*
unsigned long PDC_GetRecordRate(
    unsigned long nDeviceNo
    unsigned long nChildNo
    unsigned long *pRate
    unsigned long *pErrorCode
)
*/
typedef UINT (CALLBACK* PDC_GET_RECORD_RATE_FUNCTION_DLL)(UINT, UINT, UINT*, UINT*);

/*
unsigned long PDC_GetMaxResolution(
    unsigned long nDeviceNo
    unsigned long nChildNo
    unsigned long *pWidth
    unsigned long *pHeight
    unsigned long *pErrorCode
)
*/
typedef UINT (CALLBACK* PDC_GET_MAX_RESOLUTION_FUNCTION_DLL)(UINT, UINT, UINT*, UINT*, UINT*);

/*
unsigned long PDC_GetResolution(
    unsigned long nDeviceNo
    unsigned long nChildNo
    unsigned long *pWidth
    unsigned long *pHeight
    unsigned long *pErrorCode
)
*/
typedef UINT (CALLBACK* PDC_GET_RESOLUTION_FUNCTION_DLL)(UINT, UINT, UINT*, UINT*, UINT*);

/*
unsigned long PDC_GetShutterSpeedFps(
    unsigned long nDeviceNo
    unsigned long nChildNo
    unsigned long *pFps
    unsigned long *pErrorCode
)
*/
typedef UINT (CALLBACK* PDC_GET_SHUTTER_SPEED_FPS_FUNCTION_DLL)(UINT, UINT, UINT*, UINT*);

/*
unsigned long PDC_GetTriggerMode(
    unsigned long nDeviceNo
    unsigned long *pMode
    unsigned long *pAFrames
    unsigned long *pRFrames
    unsigned long *pRCount
    unsigned long *pErrorCode
)
*/
typedef UINT (CALLBACK* PDC_GET_TRIGGER_MODE_FUNCTION_DLL)(UINT, UINT*, UINT*, UINT*, UINT*, UINT*);

/*
unsigned long PDC_GetMaxFrames(
    unsigned long nDeviceNo
    unsigned long nChildNo
    unsigned long *pFrames
    unsigned long *pBlocks
    unsigned long *pErrorCode
)
*/
typedef UINT (CALLBACK* PDC_GET_MAX_FRAMES_FUNCTION_DLL)(UINT, UINT, UINT*, UINT*, UINT*);

/*
unsigned long PDC_GetSensorGainMode(
    unsigned long nDeviceNo
    unsigned long nChildNo
    unsigned long *pMode
    unsigned long *pErrorCode
)
*/
typedef UINT (CALLBACK* PDC_GET_SENSOR_GAIN_MODE_FUNCTION_DLL)(UINT, UINT, UINT*, UINT*);

/*
unsigned long PDC_GetSensorGammaMode(
    unsigned long nDeviceNo
    unsigned long nChildNo
    unsigned long *pMode
    unsigned long *pErrorCode
)
*/
typedef UINT (CALLBACK* PDC_GET_SENSOR_GAMMA_MODE_FUNCTION_DLL)(UINT, UINT, UINT*, UINT*);

/*
unsigned long PDC_GetLUTMode(
    unsigned long nDeviceNo
    unsigned long nChildNo
    unsigned long *pMode
    unsigned long *pErrorCode
)
*/
typedef UINT (CALLBACK* PDC_GET_LUT_MODE_FUNCTION_DLL)(UINT, UINT, UINT*, UINT*);


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
        const char * message = "GetProcAddress failed loading PDC_DetectDevice function";
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
    if (pdc_detect_num_info.m_nDeviceNum == 0) {
        const char * message = "No devices detected!";
        fwrite(message, sizeof(char), strlen(message), output_file);
        return PDC_WRAPPER_FAILED;
    }
    if (pdc_detect_num_info.m_nDeviceNum > 1) {
        const char * message = "More than 1 device detected!";
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
    fclose(output_file);

    return PDC_WRAPPER_SUCCEEDED;
}

/*
    tmp_file_buffer:
        success case (PDC_WRAPPER_SUCCEEDED):
            4 bytes for function return_value
            if return_value is success:
                4 bytes for error_code
                4 bytes for p_device_no
        error case (PDC_WRAPPER_FAILED):
            string with error message
*/
int pdc_open_device(UINT m_ndevice_code, UINT m_ntmp_device_no, UINT m_ninterface_code, const char * tmp_file_buffer) { 
    HINSTANCE libHandle;

    PDC_OPEN_DEVICE_FUNCTION_DLL pdc_open_device_function;
    UINT p_device_no, error_code, return_value;
    PDC_DETECT_INFO pdc_detect_info;
    pdc_detect_info.m_nDeviceCode = m_ndevice_code;
    pdc_detect_info.m_nTmpDeviceNo = m_ntmp_device_no;
    pdc_detect_info.m_nInterfaceCode = m_ninterface_code;

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

    pdc_open_device_function = (PDC_OPEN_DEVICE_FUNCTION_DLL) GetProcAddress(libHandle, "PDC_OpenDevice");
    if (pdc_open_device_function == NULL) {
        const char * message = "GetProcAddress failed loading PDC_OpenDevice function";
        fwrite(message, sizeof(char), strlen(message), output_file);
        fclose(output_file);
        return PDC_WRAPPER_FAILED;
    }

    return_value = pdc_open_device_function(&pdc_detect_info, &p_device_no, &error_code);

    fwrite(&return_value, sizeof(UINT), 1, output_file);
    if (return_value == PDC_FAILED) {
        fclose(output_file);
        return PDC_WRAPPER_SUCCEEDED;
    }

    fwrite(&error_code, sizeof(UINT), 1, output_file);
    fwrite(&p_device_no, sizeof(UINT), 1, output_file);
    fclose(output_file);

    return PDC_WRAPPER_SUCCEEDED;
}

/*
    tmp_file_buffer:
        success case (PDC_WRAPPER_SUCCEEDED):
            4 bytes for return_value
            4 bytes for error_code
        error case (PDC_WRAPPER_FAILED):
            string with error message
*/
int pdc_close_device(UINT n_device_no, const char * tmp_file_buffer) {
    HINSTANCE libHandle;

    PDC_CLOSE_DEVICE_FUNCTION_DLL pdc_close_device_function;
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

    pdc_close_device_function = (PDC_CLOSE_DEVICE_FUNCTION_DLL) GetProcAddress(libHandle, "PDC_CloseDevice");
    if (pdc_close_device_function == NULL) {
        const char * message = "GetProcAddress failed loading PDC_CloseDevice function";
        fwrite(message, sizeof(char), strlen(message), output_file);
        fclose(output_file);
        return PDC_WRAPPER_FAILED;
    }

    return_value = pdc_close_device_function(n_device_no, &error_code);

    fwrite(&return_value, sizeof(UINT), 1, output_file);
    fwrite(&error_code, sizeof(UINT), 1, output_file);
    fclose(output_file);

    return PDC_WRAPPER_SUCCEEDED;
}

/*
    tmp_file_buffer:
        success case (PDC_WRAPPER_SUCCEEDED):
            4 bytes for return_value
            4 bytes for error_code
            N bytes for device name
        error case (PDC_WRAPPER_FAILED):
            string with error message
*/
int pdc_get_device_name(UINT n_device_no, UINT n_child_no, const char * tmp_file_buffer) {
    HINSTANCE libHandle;

    PDC_GET_DEVICE_NAME_FUNCTION_DLL pdc_get_device_name_function;
    UINT error_code, return_value;
    TCHAR* p_str_name = NULL;

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

    pdc_get_device_name_function = (PDC_GET_DEVICE_NAME_FUNCTION_DLL) GetProcAddress(libHandle, "PDC_GetDeviceNameW");
    if (pdc_get_device_name_function == NULL) {
        const char * message = "GetProcAddress failed loading PDC_GetDeviceName function";
        fwrite(message, sizeof(char), strlen(message), output_file);
        fclose(output_file);
        return PDC_WRAPPER_FAILED;
    }

    return_value = pdc_get_device_name_function(n_device_no, n_child_no, p_str_name, &error_code);

    fwrite(&return_value, sizeof(UINT), 1, output_file);
    fwrite(&error_code, sizeof(UINT), 1, output_file);
    fputs(p_str_name, output_file);
    fclose(output_file);

    return PDC_WRAPPER_SUCCEEDED;
}

/*
    tmp_file_buffer:
        success case (PDC_WRAPPER_SUCCEEDED):
            4 bytes for return_value
            4 bytes for error_code
            4 bytes for status
        error case (PDC_WRAPPER_FAILED):
            string with error message
*/
int pdc_get_status(UINT n_device_no, const char * tmp_file_buffer) {
    HINSTANCE libHandle;

    PDC_GET_STATUS_FUNCTION_DLL pdc_get_status_function;
    UINT status, error_code, return_value;

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

    pdc_get_status_function = (PDC_GET_STATUS_FUNCTION_DLL) GetProcAddress(libHandle, "PDC_GetStatus");
    if (pdc_get_status_function == NULL) {
        const char * message = "GetProcAddress failed loading PDC_GetStatus function";
        fwrite(message, sizeof(char), strlen(message), output_file);
        fclose(output_file);
        return PDC_WRAPPER_FAILED;
    }

    return_value = pdc_get_status_function(n_device_no, &status, &error_code);

    fwrite(&return_value, sizeof(UINT), 1, output_file);
    fwrite(&error_code, sizeof(UINT), 1, output_file);
    fwrite(&status, sizeof(UINT), 1, output_file);
    fclose(output_file);

    return PDC_WRAPPER_SUCCEEDED;
}

/*
    tmp_file_buffer:
        success case (PDC_WRAPPER_SUCCEEDED):
            4 bytes for return_value
            4 bytes for error_code
            4 bytes for size
            4*size bytes for child list
        error case (PDC_WRAPPER_FAILED):
            string with error message
*/
int pdc_get_exist_child_device_list(UINT n_device_no, const char * tmp_file_buffer) {
    HINSTANCE libHandle;

    PDC_GET_EXIST_CHILD_DEVICE_LIST_FUNCTION_DLL pdc_get_exist_child_device_list_function_dll;
    PDC_GET_MAX_CHILD_DEVICE_COUNT_FUNCTION_DLL pdc_get_max_child_device_count_function_dll;
    UINT list_size, error_code, return_value;

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

    pdc_get_exist_child_device_list_function_dll = (PDC_GET_EXIST_CHILD_DEVICE_LIST_FUNCTION_DLL) GetProcAddress(libHandle, "PDC_GetExistChildDeviceList");
    if (pdc_get_exist_child_device_list_function_dll == NULL) {
        const char * message = "GetProcAddress failed loading PDC_GetExistChildDeviceList function";
        fwrite(message, sizeof(char), strlen(message), output_file);
        fclose(output_file);
        return PDC_WRAPPER_FAILED;
    }

    pdc_get_max_child_device_count_function_dll = (PDC_GET_MAX_CHILD_DEVICE_COUNT_FUNCTION_DLL) GetProcAddress(libHandle, "PDC_GetMaxChildDeviceCount");
    if (pdc_get_max_child_device_count_function_dll == NULL) {
        const char * message = "GetProcAddress failed loading PDC_GetMaxChildDeviceCount function";
        fwrite(message, sizeof(char), strlen(message), output_file);
        fclose(output_file);
        return PDC_WRAPPER_FAILED;
    }

    UINT p_count;
    return_value = pdc_get_max_child_device_count_function_dll(n_device_no, &p_count, &error_code);
    if (error_code == PDC_FAILED) {
        const char * message = "Error getting child device count";
        fwrite(message, sizeof(char), strlen(message), output_file);
        fclose(output_file);
        return PDC_WRAPPER_FAILED;
    }

    UINT* child_list = (UINT*) malloc(p_count);

    return_value = pdc_get_exist_child_device_list_function_dll(n_device_no, &list_size, child_list, &error_code);

    fwrite(&return_value, sizeof(UINT), 1, output_file);
    fwrite(&error_code, sizeof(UINT), 1, output_file);
    fwrite(&list_size, sizeof(UINT), 1, output_file);
    fwrite(child_list, sizeof(UINT)*list_size, list_size, output_file);
    fclose(output_file);
    free(child_list);

    return PDC_WRAPPER_SUCCEEDED;
}

/*
    tmp_file_buffer:
        success case (PDC_WRAPPER_SUCCEEDED):
            4 bytes for return_value
            4 bytes for error_code
            4 bytes for depth
        error case (PDC_WRAPPER_FAILED):
            string with error message
*/
int pdc_get_max_bit_depth(UINT n_device_no, UINT n_child_no, const char * tmp_file_buffer) {
    HINSTANCE libHandle;

    PDC_GET_MAX_BIT_DEPTH_FUNCTION_DLL pdc_get_max_bit_depth_function_dll;
    UINT depth, error_code, return_value;

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

    pdc_get_max_bit_depth_function_dll = (PDC_GET_MAX_BIT_DEPTH_FUNCTION_DLL) GetProcAddress(libHandle, "PDC_GetMaxBitDepth");
    if (pdc_get_max_bit_depth_function_dll == NULL) {
        const char * message = "GetProcAddress failed loading PDC_GetMaxBitDepth function";
        fwrite(message, sizeof(char), strlen(message), output_file);
        fclose(output_file);
        return PDC_WRAPPER_FAILED;
    }

    return_value = pdc_get_max_bit_depth_function_dll(n_device_no, n_child_no, &depth, &error_code);

    fwrite(&return_value, sizeof(UINT), 1, output_file);
    fwrite(&error_code, sizeof(UINT), 1, output_file);
    fwrite(&depth, sizeof(UINT), 1, output_file);
    fclose(output_file);

    return PDC_WRAPPER_SUCCEEDED;
}

/*
    tmp_file_buffer:
        success case (PDC_WRAPPER_SUCCEEDED):
            4 bytes for return_value
            4 bytes for error_code
            1 byte for depth
        error case (PDC_WRAPPER_FAILED):
            string with error message
*/
int pdc_get_bit_depth(UINT n_device_no, UINT n_child_no, const char * tmp_file_buffer) {
    HINSTANCE libHandle;

    PDC_GET_BIT_DEPTH_FUNCTION_DLL pdc_get_bit_depth_function_dll;
    UINT error_code, return_value;
    char depth;

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

    pdc_get_bit_depth_function_dll = (PDC_GET_BIT_DEPTH_FUNCTION_DLL) GetProcAddress(libHandle, "PDC_GetBitDepth");
    if (pdc_get_bit_depth_function_dll == NULL) {
        const char * message = "GetProcAddress failed loading PDC_GetBitDepth function";
        fwrite(message, sizeof(char), strlen(message), output_file);
        fclose(output_file);
        return PDC_WRAPPER_FAILED;
    }

    return_value = pdc_get_bit_depth_function_dll(n_device_no, n_child_no, &depth, &error_code);

    fwrite(&return_value, sizeof(UINT), 1, output_file);
    fwrite(&error_code, sizeof(UINT), 1, output_file);
    fwrite(&depth, sizeof(char), 1, output_file);
    fclose(output_file);

    return PDC_WRAPPER_SUCCEEDED;
}

/*
    tmp_file_buffer:
        success case (PDC_WRAPPER_SUCCEEDED):
            4 bytes for return_value
            4 bytes for error_code
            1 byte for color type
        error case (PDC_WRAPPER_FAILED):
            string with error message
*/
int pdc_get_color_type(UINT n_device_no, UINT n_child_no, const char * tmp_file_buffer) {
    HINSTANCE libHandle;

    PDC_GET_COLOR_TYPE_FUNCTION_DLL pdc_get_color_type_function_dll;
    UINT error_code, return_value;
    char color_type;

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

    pdc_get_color_type_function_dll = (PDC_GET_COLOR_TYPE_FUNCTION_DLL) GetProcAddress(libHandle, "PDC_GetColorType");
    if (pdc_get_color_type_function_dll == NULL) {
        const char * message = "GetProcAddress failed loading PDC_GetColorType function";
        fwrite(message, sizeof(char), strlen(message), output_file);
        fclose(output_file);
        return PDC_WRAPPER_FAILED;
    }

    return_value = pdc_get_color_type_function_dll(n_device_no, n_child_no, &color_type, &error_code);

    fwrite(&return_value, sizeof(UINT), 1, output_file);
    fwrite(&error_code, sizeof(UINT), 1, output_file);
    fwrite(&color_type, sizeof(char), 1, output_file);
    fclose(output_file);

    return PDC_WRAPPER_SUCCEEDED;
}

/*
    tmp_file_buffer:
        success case (PDC_WRAPPER_SUCCEEDED):
            4 bytes for return_value
            4 bytes for error_code
            4 bytes for record rate
        error case (PDC_WRAPPER_FAILED):
            string with error message
*/
int pdc_get_record_rate(UINT n_device_no, UINT n_child_no, const char * tmp_file_buffer) {
    HINSTANCE libHandle;

    PDC_GET_RECORD_RATE_FUNCTION_DLL pdc_get_record_rate_function_dll;
    UINT error_code, return_value;
    UINT record_rate;

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

    pdc_get_record_rate_function_dll = (PDC_GET_RECORD_RATE_FUNCTION_DLL) GetProcAddress(libHandle, "PDC_GetRecordRate");
    if (pdc_get_record_rate_function_dll == NULL) {
        const char * message = "GetProcAddress failed loading PDC_GetRecordRate function";
        fwrite(message, sizeof(char), strlen(message), output_file);
        fclose(output_file);
        return PDC_WRAPPER_FAILED;
    }

    return_value = pdc_get_record_rate_function_dll(n_device_no, n_child_no, &record_rate, &error_code);

    fwrite(&return_value, sizeof(UINT), 1, output_file);
    fwrite(&error_code, sizeof(UINT), 1, output_file);
    fwrite(&record_rate, sizeof(UINT), 1, output_file);
    fclose(output_file);

    return PDC_WRAPPER_SUCCEEDED;
}

/*
    tmp_file_buffer:
        success case (PDC_WRAPPER_SUCCEEDED):
            4 bytes for return_value
            4 bytes for error_code
            4 bytes for width
            4 bytes for height
        error case (PDC_WRAPPER_FAILED):
            string with error message
*/
int pdc_get_max_resolution(UINT n_device_no, UINT n_child_no, const char * tmp_file_buffer) {
    HINSTANCE libHandle;

    PDC_GET_MAX_RESOLUTION_FUNCTION_DLL pdc_get_max_resolution_function_dll;
    UINT error_code, return_value;
    UINT width, height;

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

    pdc_get_max_resolution_function_dll = (PDC_GET_MAX_RESOLUTION_FUNCTION_DLL) GetProcAddress(libHandle, "PDC_GetMaxResolution");
    if (pdc_get_max_resolution_function_dll == NULL) {
        const char * message = "GetProcAddress failed loading PDC_GetMaxResolution function";
        fwrite(message, sizeof(char), strlen(message), output_file);
        fclose(output_file);
        return PDC_WRAPPER_FAILED;
    }

    return_value = pdc_get_max_resolution_function_dll(n_device_no, n_child_no, &width, &height, &error_code);

    fwrite(&return_value, sizeof(UINT), 1, output_file);
    fwrite(&error_code, sizeof(UINT), 1, output_file);
    fwrite(&width, sizeof(UINT), 1, output_file);
    fwrite(&height, sizeof(UINT), 1, output_file);
    fclose(output_file);

    return PDC_WRAPPER_SUCCEEDED;
}

/*
    tmp_file_buffer:
        success case (PDC_WRAPPER_SUCCEEDED):
            4 bytes for return_value
            4 bytes for error_code
            4 bytes for width
            4 bytes for height
        error case (PDC_WRAPPER_FAILED):
            string with error message
*/
int pdc_get_resolution(UINT n_device_no, UINT n_child_no, const char * tmp_file_buffer) {
    HINSTANCE libHandle;

    PDC_GET_RESOLUTION_FUNCTION_DLL pdc_get_resolution_function_dll;
    UINT error_code, return_value;
    UINT width, height;

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

    pdc_get_resolution_function_dll = (PDC_GET_MAX_RESOLUTION_FUNCTION_DLL) GetProcAddress(libHandle, "PDC_GetResolution");
    if (pdc_get_resolution_function_dll == NULL) {
        const char * message = "GetProcAddress failed loading PDC_GetResolution function";
        fwrite(message, sizeof(char), strlen(message), output_file);
        fclose(output_file);
        return PDC_WRAPPER_FAILED;
    }

    return_value = pdc_get_resolution_function_dll(n_device_no, n_child_no, &width, &height, &error_code);

    fwrite(&return_value, sizeof(UINT), 1, output_file);
    fwrite(&error_code, sizeof(UINT), 1, output_file);
    fwrite(&width, sizeof(UINT), 1, output_file);
    fwrite(&height, sizeof(UINT), 1, output_file);
    fclose(output_file);

    return PDC_WRAPPER_SUCCEEDED;
}

/*
    tmp_file_buffer:
        success case (PDC_WRAPPER_SUCCEEDED):
            4 bytes for return_value
            4 bytes for error_code
            4 bytes for fps
        error case (PDC_WRAPPER_FAILED):
            string with error message
*/
int pdc_get_shutter_speed_fps(UINT n_device_no, UINT n_child_no, const char * tmp_file_buffer) {
    HINSTANCE libHandle;

    PDC_GET_SHUTTER_SPEED_FPS_FUNCTION_DLL pdc_get_shutter_speed_fps_function_dll;
    UINT error_code, return_value;
    UINT fps;

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

    pdc_get_shutter_speed_fps_function_dll = (PDC_GET_SHUTTER_SPEED_FPS_FUNCTION_DLL) GetProcAddress(libHandle, "PDC_GetShutterSpeedFps");
    if (pdc_get_shutter_speed_fps_function_dll == NULL) {
        const char * message = "GetProcAddress failed loading PDC_GetShutterSpeedFps function";
        fwrite(message, sizeof(char), strlen(message), output_file);
        fclose(output_file);
        return PDC_WRAPPER_FAILED;
    }

    return_value = pdc_get_shutter_speed_fps_function_dll(n_device_no, n_child_no, &fps, &error_code);

    fwrite(&return_value, sizeof(UINT), 1, output_file);
    fwrite(&error_code, sizeof(UINT), 1, output_file);
    fwrite(&fps, sizeof(UINT), 1, output_file);
    fclose(output_file);

    return PDC_WRAPPER_SUCCEEDED;
}

/*
    tmp_file_buffer:
        success case (PDC_WRAPPER_SUCCEEDED):
            4 bytes for return_value
            4 bytes for error_code
            4 bytes for mode
            4 bytes for aframes
            4 bytes for rframes
            4 bytes for rcount
        error case (PDC_WRAPPER_FAILED):
            string with error message
*/
int pdc_get_trigger_mode(UINT n_device_no, const char * tmp_file_buffer) {
    HINSTANCE libHandle;

    PDC_GET_TRIGGER_MODE_FUNCTION_DLL pdc_get_trigger_mode_function_dll;
    UINT error_code, return_value;
    UINT mode, aframes, rframes, rcount;

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

    pdc_get_trigger_mode_function_dll = (PDC_GET_TRIGGER_MODE_FUNCTION_DLL) GetProcAddress(libHandle, "PDC_GetTriggerMode");
    if (pdc_get_trigger_mode_function_dll == NULL) {
        const char * message = "GetProcAddress failed loading PDC_GetTriggerMode function";
        fwrite(message, sizeof(char), strlen(message), output_file);
        fclose(output_file);
        return PDC_WRAPPER_FAILED;
    }

    return_value = pdc_get_trigger_mode_function_dll(n_device_no, &mode, &aframes, &rframes, &rcount, &error_code);

    fwrite(&return_value, sizeof(UINT), 1, output_file);
    fwrite(&error_code, sizeof(UINT), 1, output_file);
    fwrite(&mode, sizeof(UINT), 1, output_file);
    fwrite(&aframes, sizeof(UINT), 1, output_file);
    fwrite(&rframes, sizeof(UINT), 1, output_file);
    fwrite(&rcount, sizeof(UINT), 1, output_file);
    fclose(output_file);

    return PDC_WRAPPER_SUCCEEDED;
}

/*
    tmp_file_buffer:
        success case (PDC_WRAPPER_SUCCEEDED):
            4 bytes for return_value
            4 bytes for error_code
            4 bytes for frames
            4 bytes for blocks
        error case (PDC_WRAPPER_FAILED):
            string with error message
*/
int pdc_get_max_frames(UINT n_device_no, UINT n_child_no, const char * tmp_file_buffer) {
    HINSTANCE libHandle;

    PDC_GET_MAX_FRAMES_FUNCTION_DLL pdc_get_max_frames_function_dll;
    UINT error_code, return_value;
    UINT frames, blocks;

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

    pdc_get_max_frames_function_dll = (PDC_GET_MAX_FRAMES_FUNCTION_DLL) GetProcAddress(libHandle, "PDC_GetMaxFrames");
    if (pdc_get_max_frames_function_dll == NULL) {
        const char * message = "GetProcAddress failed loading PDC_GetMaxFrames function";
        fwrite(message, sizeof(char), strlen(message), output_file);
        fclose(output_file);
        return PDC_WRAPPER_FAILED;
    }

    return_value = pdc_get_max_frames_function_dll(n_device_no, n_child_no, &frames, &blocks, &error_code);

    fwrite(&return_value, sizeof(UINT), 1, output_file);
    fwrite(&error_code, sizeof(UINT), 1, output_file);
    fwrite(&frames, sizeof(UINT), 1, output_file);
    fwrite(&blocks, sizeof(UINT), 1, output_file);
    fclose(output_file);

    return PDC_WRAPPER_SUCCEEDED;
}

/*
    tmp_file_buffer:
        success case (PDC_WRAPPER_SUCCEEDED):
            4 bytes for return_value
            4 bytes for error_code
            4 bytes for mode
        error case (PDC_WRAPPER_FAILED):
            string with error message
*/
int pdc_get_sensor_gain_mode(UINT n_device_no, UINT n_child_no, const char * tmp_file_buffer) {
    HINSTANCE libHandle;

    PDC_GET_SENSOR_GAIN_MODE_FUNCTION_DLL pdc_get_sensor_gain_mode_function_dll;
    UINT error_code, return_value;
    UINT mode;

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

    pdc_get_sensor_gain_mode_function_dll = (PDC_GET_SENSOR_GAIN_MODE_FUNCTION_DLL) GetProcAddress(libHandle, "PDC_GetSensorGainMode");
    if (pdc_get_sensor_gain_mode_function_dll == NULL) {
        const char * message = "GetProcAddress failed loading PDC_GetSensorGainMode function";
        fwrite(message, sizeof(char), strlen(message), output_file);
        fclose(output_file);
        return PDC_WRAPPER_FAILED;
    }

    return_value = pdc_get_sensor_gain_mode_function_dll(n_device_no, n_child_no, &mode, &error_code);

    fwrite(&return_value, sizeof(UINT), 1, output_file);
    fwrite(&error_code, sizeof(UINT), 1, output_file);
    fwrite(&mode, sizeof(UINT), 1, output_file);
    fclose(output_file);

    return PDC_WRAPPER_SUCCEEDED;
}

/*
    tmp_file_buffer:
        success case (PDC_WRAPPER_SUCCEEDED):
            4 bytes for return_value
            4 bytes for error_code
            4 bytes for mode
        error case (PDC_WRAPPER_FAILED):
            string with error message
*/
int pdc_get_sensor_gamma_mode(UINT n_device_no, UINT n_child_no, const char * tmp_file_buffer) {
    HINSTANCE libHandle;

    PDC_GET_SENSOR_GAMMA_MODE_FUNCTION_DLL pdc_get_sensor_gamma_mode_function_dll;
    UINT error_code, return_value;
    UINT mode;

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

    pdc_get_sensor_gamma_mode_function_dll = (PDC_GET_SENSOR_GAMMA_MODE_FUNCTION_DLL) GetProcAddress(libHandle, "PDC_GetSensorGammaMode");
    if (pdc_get_sensor_gamma_mode_function_dll == NULL) {
        const char * message = "GetProcAddress failed loading PDC_GetSensorGammaMode function";
        fwrite(message, sizeof(char), strlen(message), output_file);
        fclose(output_file);
        return PDC_WRAPPER_FAILED;
    }

    return_value = pdc_get_sensor_gamma_mode_function_dll(n_device_no, n_child_no, &mode, &error_code);

    fwrite(&return_value, sizeof(UINT), 1, output_file);
    fwrite(&error_code, sizeof(UINT), 1, output_file);
    fwrite(&mode, sizeof(UINT), 1, output_file);
    fclose(output_file);

    return PDC_WRAPPER_SUCCEEDED;
}

/*
    tmp_file_buffer:
        success case (PDC_WRAPPER_SUCCEEDED):
            4 bytes for return_value
            4 bytes for error_code
            4 bytes for mode
        error case (PDC_WRAPPER_FAILED):
            string with error message
*/
int pdc_get_lut_mode(UINT n_device_no, UINT n_child_no, const char * tmp_file_buffer) {
    HINSTANCE libHandle;

    PDC_GET_LUT_MODE_FUNCTION_DLL pdc_get_lut_mode_function_dll;
    UINT error_code, return_value;
    UINT mode;

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

    pdc_get_lut_mode_function_dll = (PDC_GET_LUT_MODE_FUNCTION_DLL) GetProcAddress(libHandle, "PDC_GetLUTMode");
    if (pdc_get_lut_mode_function_dll == NULL) {
        const char * message = "GetProcAddress failed loading PDC_GetLUTMode function";
        fwrite(message, sizeof(char), strlen(message), output_file);
        fclose(output_file);
        return PDC_WRAPPER_FAILED;
    }

    return_value = pdc_get_lut_mode_function_dll(n_device_no, n_child_no, &mode, &error_code);

    fwrite(&return_value, sizeof(UINT), 1, output_file);
    fwrite(&error_code, sizeof(UINT), 1, output_file);
    fwrite(&mode, sizeof(UINT), 1, output_file);
    fclose(output_file);

    return PDC_WRAPPER_SUCCEEDED;
}