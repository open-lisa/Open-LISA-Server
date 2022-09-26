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

/*
unsigned long PDC_GetLUTParams(
    unsigned long nDeviceNo
    unsigned long nChildNo
    unsigned long nLUTMode
    PPDC_LUT_PARAMS pParams
    unsigned long *pErrorCode
)
*/
typedef UINT (CALLBACK* PDC_GET_LUT_PARAMS_FUNCTION_DLL)(UINT, UINT, UINT, PPDC_LUT_PARAMS*, UINT*);

/*
unsigned long PDC_GetShadingMode(
    unsigned long nDeviceNo
    unsigned long nChildNo
    unsigned long *pMode
    unsigned long *pErrorCode
)
*/
typedef UINT (CALLBACK* PDC_GET_SHADING_MODE_FUNCTION_DLL)(UINT, UINT, UINT*, UINT*);

/*
unsigned long PDC_GetTransferOption(
    unsigned long nDeviceNo
    unsigned long nChildNo
    unsigned long *p8BitSel
    unsigned long *pBayer
    unsigned long *pInterleave
    unsigned long *pErrorCode
)
*/
typedef UINT (CALLBACK* PDC_GET_TRANSFER_OPTION_FUNCTION_DLL)(UINT, UINT, UINT*, UINT*, UINT*, UINT*);

/*
unsigned long PDC_GetExternalOutMode(
    unsigned long nDeviceNo
    unsigned long nPort
    unsigned long *pMode
    unsigned long *pErrorCode
)
*/
typedef UINT (CALLBACK* PDC_GET_EXTERNAL_OUT_MODE_FUNCTION_DLL)(UINT, UINT, UINT*, UINT*);

/*
unsigned long PDC_GetRecordRateList(
    unsigned long nDeviceNo
    unsigned long nChildNo
    unsigned long *pSize
    unsigned long *pList
    unsigned long *pErrorCode
)
*/
typedef UINT (CALLBACK* PDC_GET_RECORD_RATE_LIST_FUNCTION_DLL)(UINT, UINT, UINT*, UINT*, UINT*);

/*
unsigned long PDC_GetResolutionList(
    unsigned long nDeviceNo
    unsigned long nChildNo
    unsigned long *pSize
    unsigned long *pList
    unsigned long *pErrorCode
)
*/
typedef UINT (CALLBACK* PDC_GET_RESOLUTION_LIST_FUNCTION_DLL)(UINT, UINT, UINT*, UINT*, UINT*);

/*
unsigned long PDC_GetShutterSpeedFpsList(
    unsigned long nDeviceNo
    unsigned long nChildNo
    unsigned long *pSize
    unsigned long *pList
    unsigned long *pErrorCode
)
*/
typedef UINT (CALLBACK* PDC_GET_SHUTTER_SPEED_FPS_LIST_FUNCTION_DLL)(UINT, UINT, UINT*, UINT*, UINT*);

/*
unsigned long PDC_GetMemFrameInfo(
    unsigned long nDeviceNo
    unsigned long nChildNo
    PPDC_FRAME_INFO pFrame
    unsigned long *pErrorCode
)
*/
typedef UINT (CALLBACK* PDC_GET_MEM_FRAME_INFO_FUNCTION_DLL)(UINT, UINT, PPDC_FRAME_INFO*, UINT*);

/*
unsigned long PDC_SetStatus(
    unsigned long nDeviceNo
    unsigned long nMode
    unsigned long *pErrorCode
)
*/
typedef UINT (CALLBACK* PDC_SET_STATUS_FUNCTION_DLL)(UINT, UINT, UINT*);

/*
unsigned long PDC_SetRecReady(
    unsigned long nDeviceNo
    unsigned long *pErrorCode
)
*/
typedef UINT (CALLBACK* PDC_SET_REC_READY_FUNCTION_DLL)(UINT, UINT*);

/*
unsigned long PDC_SetEndless(
    unsigned long nDeviceNo
    unsigned long *pErrorCode
)
*/
typedef UINT (CALLBACK* PDC_SET_ENDLESS_FUNCTION_DLL)(UINT, UINT*);

/*
unsigned long PDC_TriggerIn(
    unsigned long nDeviceNo
    unsigned long *pErrorCode
)
*/
typedef UINT (CALLBACK* PDC_TRIGGER_IN_FUNCTION_DLL)(UINT, UINT*);

/*
unsigned long PDC_SetBitDepth(
    unsigned long nDeviceNo
    unsigned long nChildNo
    char nDepth
    unsigned long *pErrorCode
)
*/
typedef UINT (CALLBACK* PDC_SET_BIT_DEPTH_FUNCTION_DLL)(UINT, UINT, CHAR, UINT*);

/*
unsigned long PDC_SetRecordRate(
    unsigned long nDeviceNo
    unsigned long nChildNo
    unsigned long nRate
    unsigned long *pErrorCode
)
*/
typedef UINT (CALLBACK* PDC_SET_RECORD_RATE_FUNCTION_DLL)(UINT, UINT, UINT, UINT*);

/*
unsigned long PDC_SetResolution(
    unsigned long nDeviceNo
    unsigned long nChildNo
    unsigned long nWidth
    unsigned long nHeight
    unsigned long *pErrorCode
)
*/
typedef UINT (CALLBACK* PDC_SET_RESOLUTION_FUNTION_DLL)(UINT, UINT, UINT, UINT, UINT*);

/*
unsigned long PDC_SetShutterSpeedFps(
    unsigned long nDeviceNo
    unsigned long nChildNo
    unsigned long nFps
    unsigned long *pErrorCode
)
*/
typedef UINT (CALLBACK* PDC_SET_SHUTTER_SPEED_FPS_FUNCTION_DLL)(UINT, UINT, UINT, UINT*);

/*
unsigned long PDC_SetTriggerMode(
    unsigned long nDeviceNo
    unsigned long nMode
    unsigned long nAFrames
    unsigned long nRFrames
    unsigned long nRCount
    unsigned long *pErrorCode
)
*/
typedef UINT (CALLBACK* PDC_SET_TRIGGER_MODE_FUNCTION_DLL)(UINT, UINT, UINT, UINT, UINT, UINT*);

/*
unsigned long PDC_SetSensorGainMode(
    unsigned long nDeviceNo
    unsigned long nChildNo
    unsigned long nMode
    unsigned long *pErrorCode
)
*/
typedef UINT (CALLBACK* PDC_SET_SENSOR_GAIN_MODE_FUNCTION_DLL)(UINT, UINT, UINT, UINT*);

/*
unsigned long PDC_SetLUTMode(
    unsigned long nDeviceNo
    unsigned long nChildNo
    unsigned long nMode
    unsigned long *pErrorCode
)
*/
typedef UINT (CALLBACK* PDC_SET_LUT_MODE_FUNCTION_DLL)(UINT, UINT, UINT, UINT*);

/*
unsigned long PDC_SetLUTUser(
    unsigned long nDeviceNo
    unsigned long nChildNo
    unsigned long nMode
    unsigned long *pErrorCode
)
*/
typedef UINT (CALLBACK* PDC_SET_LUT_USER_FUNCTION_DLL)(UINT, UINT, UINT, UINT*);

/*
unsigned long PDC_SetExternalOutMode(
    unsigned long nDeviceNo
    unsigned long nPort
    unsigned long nMode
    unsigned long *pErrorCode
)
*/
typedef UINT (CALLBACK* PDC_SET_EXTERNAL_OUT_MODE_FUNCTION_DLL)(UINT, UINT, UINT, UINT*);

/*
unsigned long PDC_SetTransferOption(
    unsigned long nDeviceNo
    unsigned long nChildNo
    unsigned long n8BitSel
    unsigned long nBayer
    unsigned long nInterleave
    unsigned long *pErrorCode
)
*/
typedef UINT (CALLBACK* PDC_SET_TRANSFER_OPTION_FUNCTION_DLL)(UINT, UINT, UINT, UINT, UINT, UINT*);

/*
unsigned long PDC_BMPFileSave(
    unsigned long nDeviceNo
    unsigned long nChildNo
    const char * lpszFileName
    unsigned long nFrameNo
    unsigned long *pErrorCode
)
*/
typedef UINT (CALLBACK* PDC_BMP_FILE_SAVE_FUNCTION_DLL)(UINT, UINT, const CHAR*, UINT, UINT*);

/*
unsigned long PDC_AVIFileSaveOpen(
    unsigned long nDeviceNo
    unsigned long nChildNo
    LPCTSTR lpszFileName
    long nRate
    unsigned long nShowCompressDlg
    unsigned long *pErrorCode
)
*/
typedef UINT (CALLBACK* PDC_AVI_FILE_SAVE_OPEN_FUNCTION_DLL)(UINT, UINT, const CHAR*, UINT, UINT, UINT*);

/*
unsigned long PDC_AVIFileSave(
    unsigned long nDeviceNo
    unsigned long nChildNo
    unsigned long nFrameNo
    unsigned long *pSize
    unsigned long *pErrorCode
)
*/
typedef UINT (CALLBACK* PDC_AVI_FILE_SAVE_FUNCTION_DLL)(UINT, UINT, UINT, UINT*, UINT*);

/*
unsigned long PDC_AVIFileSaveClose(
    unsigned long nDeviceNo
    unsigned long nChildNo
    unsigned long *pErrorCode
)
*/
typedef UINT (CALLBACK* PDC_AVI_FILE_SAVE_CLOSE_FUNCTION_DLL)(UINT, UINT, UINT*);

/*
unsigned long PDC_MRAWFileSaveOpen(
    unsigned long   nDeviceNo
    unsigned long   nChildNo
    LPCTSTR         lpszFileName
    unsigned long   nMRawBitDepth
    long            nMaxFrameNum
    unsigned long   *pErrorCode
)
*/
typedef UINT (CALLBACK* PDC_MRAW_FILE_SAVE_OPEN_FUNCTION_DLL)(UINT, UINT, const CHAR*, UINT, UINT, UINT*);

/*
unsigned long PDC_MRAWFileSave(
    unsigned long  nDeviceNo
    unsigned long  nChildNo
    long           nFrameNo
    unsigned long  *pErrorCode
)
*/
typedef UINT (CALLBACK* PDC_MRAW_FILE_SAVE_FUNCTION_DLL)(UINT, UINT, UINT, UINT*);

/*
unsigned long PDC_MRAWFileSaveClose(
    unsigned long  nDeviceNo
    unsigned long  nChildNo
    unsigned long  *pErrorCode
)
*/
typedef UINT (CALLBACK* PDC_MRAW_FILE_SAVE_CLOSE_FUNCTION_DLL)(UINT, UINT, UINT*);


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
        fclose(output_file);
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
    fwrite(child_list, sizeof(UINT), list_size, output_file);
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

/*
    tmp_file_buffer:
        success case (PDC_WRAPPER_SUCCEEDED):
            4 bytes for function return_value
            4 bytes for error code
            if return_value is success:
                4 bytes for brightness R
                4 bytes for brightness G
                4 bytes for brightness B
                4 bytes for contrast R
                4 bytes for contrast G
                4 bytes for contrast B
                8 bytes for gain R
                8 bytes for gain G
                8 bytes for gain B
                8 bytes for gamma R
                8 bytes for gamma G
                8 bytes for gamma B
                1 byte for posi nega R
                1 byte for posi nega G
                1 byte for posi nega B
                1 byte for free mode
        error case (PDC_WRAPPER_FAILED):
            string with error message
*/
int pdc_get_lut_params(UINT n_device_no, UINT n_child_no, UINT lut_mode, const char * tmp_file_buffer) {
    HINSTANCE libHandle;

    PDC_GET_LUT_PARAMS_FUNCTION_DLL pdc_get_lut_params_function_dll;

    UINT error_code, return_value;
    PPDC_LUT_PARAMS pdc_lut_params;

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

    pdc_get_lut_params_function_dll = (PDC_GET_LUT_PARAMS_FUNCTION_DLL) GetProcAddress(libHandle, "PDC_GetLUTParams");
    if (pdc_get_lut_params_function_dll == NULL) {
        const char * message = "GetProcAddress failed loading PDC_GetLUTParams function";
        fwrite(message, sizeof(char), strlen(message), output_file);
        fclose(output_file);
        return PDC_WRAPPER_FAILED;
    }

    return_value = pdc_get_lut_params_function_dll(n_device_no, n_child_no, lut_mode, &pdc_lut_params, &error_code);

    fwrite(&return_value, sizeof(UINT), 1, output_file);
    fwrite(&error_code, sizeof(UINT), 1, output_file);
    if (return_value == PDC_FAILED) {
        fclose(output_file);
        return PDC_WRAPPER_SUCCEEDED;
    }

    fwrite(&(pdc_lut_params->m_nBrightnessR), sizeof(INT), 1, output_file);
    fwrite(&(pdc_lut_params->m_nBrightnessG), sizeof(INT), 1, output_file);
    fwrite(&(pdc_lut_params->m_nBrightnessB), sizeof(INT), 1, output_file);
    fwrite(&(pdc_lut_params->m_nContrastR), sizeof(INT), 1, output_file);
    fwrite(&(pdc_lut_params->m_nContrastG), sizeof(INT), 1, output_file);
    fwrite(&(pdc_lut_params->m_nContrastB), sizeof(INT), 1, output_file);

    fwrite(&(pdc_lut_params->m_nGainR), sizeof(DOUBLE), 1, output_file);
    fwrite(&(pdc_lut_params->m_nGainG), sizeof(DOUBLE), 1, output_file);
    fwrite(&(pdc_lut_params->m_nGainB), sizeof(DOUBLE), 1, output_file);
    fwrite(&(pdc_lut_params->m_nGammaR), sizeof(DOUBLE), 1, output_file);
    fwrite(&(pdc_lut_params->m_nGammaG), sizeof(DOUBLE), 1, output_file);
    fwrite(&(pdc_lut_params->m_nGammaB), sizeof(DOUBLE), 1, output_file);

    fwrite(&(pdc_lut_params->m_nPosiNegaR), sizeof(UCHAR), 1, output_file);
    fwrite(&(pdc_lut_params->m_nPosiNegaG), sizeof(UCHAR), 1, output_file);
    fwrite(&(pdc_lut_params->m_nPosiNegaB), sizeof(UCHAR), 1, output_file);
    fwrite(&(pdc_lut_params->m_nFreeMode), sizeof(UCHAR), 1, output_file);

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
int pdc_get_shading_mode(UINT n_device_no, UINT n_child_no, const char * tmp_file_buffer) {
    HINSTANCE libHandle;

    PDC_GET_SHADING_MODE_FUNCTION_DLL pdc_get_shading_mode_function_dll;
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

    pdc_get_shading_mode_function_dll = (PDC_GET_SHADING_MODE_FUNCTION_DLL) GetProcAddress(libHandle, "PDC_GetShadingMode");
    if (pdc_get_shading_mode_function_dll == NULL) {
        const char * message = "GetProcAddress failed loading PDC_GetShadingMode function";
        fwrite(message, sizeof(char), strlen(message), output_file);
        fclose(output_file);
        return PDC_WRAPPER_FAILED;
    }

    return_value = pdc_get_shading_mode_function_dll(n_device_no, n_child_no, &mode, &error_code);

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
            4 bytes for 8 bit sel
            4 bytes for bayer
            4 bytes for interleave
        error case (PDC_WRAPPER_FAILED):
            string with error message
*/
int pdc_get_transfer_option(UINT n_device_no, UINT n_child_no, const char * tmp_file_buffer) {
    HINSTANCE libHandle;

    PDC_GET_TRANSFER_OPTION_FUNCTION_DLL pdc_get_transfer_option_function_dll;
    UINT error_code, return_value;
    UINT eight_bit_sel, bayer, interleave;

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

    pdc_get_transfer_option_function_dll = (PDC_GET_TRANSFER_OPTION_FUNCTION_DLL) GetProcAddress(libHandle, "PDC_GetTransferOption");
    if (pdc_get_transfer_option_function_dll == NULL) {
        const char * message = "GetProcAddress failed loading PDC_GetTransferOption function";
        fwrite(message, sizeof(char), strlen(message), output_file);
        fclose(output_file);
        return PDC_WRAPPER_FAILED;
    }

    return_value = pdc_get_transfer_option_function_dll(n_device_no, n_child_no, &eight_bit_sel, &bayer, &interleave, &error_code);

    fwrite(&return_value, sizeof(UINT), 1, output_file);
    fwrite(&error_code, sizeof(UINT), 1, output_file);
    fwrite(&eight_bit_sel, sizeof(UINT), 1, output_file);
    fwrite(&bayer, sizeof(UINT), 1, output_file);
    fwrite(&interleave, sizeof(UINT), 1, output_file);
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
int pdc_get_external_out_mode(UINT n_device_no, UINT n_port, const char * tmp_file_buffer) {
    HINSTANCE libHandle;

    PDC_GET_EXTERNAL_OUT_MODE_FUNCTION_DLL pdc_get_external_out_mode_function_dll;
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

    pdc_get_external_out_mode_function_dll = (PDC_GET_EXTERNAL_OUT_MODE_FUNCTION_DLL) GetProcAddress(libHandle, "PDC_GetExternalOutMode");
    if (pdc_get_external_out_mode_function_dll == NULL) {
        const char * message = "GetProcAddress failed loading PDC_GetExternalOutMode function";
        fwrite(message, sizeof(char), strlen(message), output_file);
        fclose(output_file);
        return PDC_WRAPPER_FAILED;
    }

    return_value = pdc_get_external_out_mode_function_dll(n_device_no, n_port, &mode, &error_code);

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
            4 bytes for size
            4*size bytes for rate list
        error case (PDC_WRAPPER_FAILED):
            string with error message
*/
int pdc_get_record_rate_list(UINT n_device_no, UINT n_child_no, const char * tmp_file_buffer) {
    HINSTANCE libHandle;

    PDC_GET_RECORD_RATE_LIST_FUNCTION_DLL pdc_get_record_rate_list_function_dll;
    UINT list_size, error_code, return_value;
    UINT* list_top = NULL;

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

    pdc_get_record_rate_list_function_dll = (PDC_GET_RECORD_RATE_LIST_FUNCTION_DLL) GetProcAddress(libHandle, "PDC_GetRecordRateList");
    if (pdc_get_record_rate_list_function_dll == NULL) {
        const char * message = "GetProcAddress failed loading PDC_GetRecordRateList function";
        fwrite(message, sizeof(char), strlen(message), output_file);
        fclose(output_file);
        return PDC_WRAPPER_FAILED;
    }

    return_value = pdc_get_record_rate_list_function_dll(n_device_no, n_child_no, &list_size, list_top, &error_code);
    if (error_code == PDC_FAILED) {
        const char * message = "Error getting record rate list";
        fwrite(message, sizeof(char), strlen(message), output_file);
        fclose(output_file);
        return PDC_WRAPPER_FAILED;
    }

    fwrite(&return_value, sizeof(UINT), 1, output_file);
    fwrite(&error_code, sizeof(UINT), 1, output_file);
    fwrite(&list_size, sizeof(UINT), 1, output_file);
    fwrite(list_top, sizeof(UINT), list_size, output_file);
    fclose(output_file);

    return PDC_WRAPPER_SUCCEEDED;
}

/*
    tmp_file_buffer:
        success case (PDC_WRAPPER_SUCCEEDED):
            4 bytes for return_value
            4 bytes for error_code
            4 bytes for size
            4*size bytes for resolution list
        error case (PDC_WRAPPER_FAILED):
            string with error message
*/
int pdc_get_resolution_list(UINT n_device_no, UINT n_child_no, const char * tmp_file_buffer) {
    HINSTANCE libHandle;

    PDC_GET_RESOLUTION_FUNCTION_DLL pdc_get_resolution_list_function_dll;
    UINT list_size, error_code, return_value;
    UINT* list_top = NULL;

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

    pdc_get_resolution_list_function_dll = (PDC_GET_RESOLUTION_FUNCTION_DLL) GetProcAddress(libHandle, "PDC_GetResolutionList");
    if (pdc_get_resolution_list_function_dll == NULL) {
        const char * message = "GetProcAddress failed loading PDC_GetResolutionList function";
        fwrite(message, sizeof(char), strlen(message), output_file);
        fclose(output_file);
        return PDC_WRAPPER_FAILED;
    }

    return_value = pdc_get_resolution_list_function_dll(n_device_no, n_child_no, &list_size, list_top, &error_code);
    if (error_code == PDC_FAILED) {
        const char * message = "Error getting record rate list";
        fwrite(message, sizeof(char), strlen(message), output_file);
        fclose(output_file);
        return PDC_WRAPPER_FAILED;
    }

    fwrite(&return_value, sizeof(UINT), 1, output_file);
    fwrite(&error_code, sizeof(UINT), 1, output_file);
    fwrite(&list_size, sizeof(UINT), 1, output_file);
    fwrite(list_top, sizeof(UINT), list_size, output_file);
    fclose(output_file);

    return PDC_WRAPPER_SUCCEEDED;
}

/*
    tmp_file_buffer:
        success case (PDC_WRAPPER_SUCCEEDED):
            4 bytes for return_value
            4 bytes for error_code
            4 bytes for size
            4*size bytes for shutter speed fps list
        error case (PDC_WRAPPER_FAILED):
            string with error message
*/
int pdc_get_shutter_speed_fps_list(UINT n_device_no, UINT n_child_no, const char * tmp_file_buffer) {
    HINSTANCE libHandle;

    PDC_GET_SHUTTER_SPEED_FPS_LIST_FUNCTION_DLL pdc_get_shutter_speed_fps_list_function_dll;
    UINT list_size, error_code, return_value;
    UINT* list_top = NULL;

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

    pdc_get_shutter_speed_fps_list_function_dll = (PDC_GET_SHUTTER_SPEED_FPS_LIST_FUNCTION_DLL) GetProcAddress(libHandle, "PDC_GetShutterSpeedFpsList");
    if (pdc_get_shutter_speed_fps_list_function_dll == NULL) {
        const char * message = "GetProcAddress failed loading PDC_GetShutterSpeedFpsList function";
        fwrite(message, sizeof(char), strlen(message), output_file);
        fclose(output_file);
        return PDC_WRAPPER_FAILED;
    }

    return_value = pdc_get_shutter_speed_fps_list_function_dll(n_device_no, n_child_no, &list_size, list_top, &error_code);
    if (error_code == PDC_FAILED) {
        const char * message = "Error getting record rate list";
        fwrite(message, sizeof(char), strlen(message), output_file);
        fclose(output_file);
        return PDC_WRAPPER_FAILED;
    }

    fwrite(&return_value, sizeof(UINT), 1, output_file);
    fwrite(&error_code, sizeof(UINT), 1, output_file);
    fwrite(&list_size, sizeof(UINT), 1, output_file);
    fwrite(list_top, sizeof(UINT), list_size, output_file);
    fclose(output_file);

    return PDC_WRAPPER_SUCCEEDED;
}

/*
    tmp_file_buffer:
        success case (PDC_WRAPPER_SUCCEEDED):
            4 bytes for function return_value
            4 bytes for error code
            if return_value is success:
                4 bytes for start
                4 bytes for end
                4 bytes for trigger
                4 bytes for two stage low to high
                4 bytes for two stage high to low
                4*10 bytes for 10 events
                4 bytes for event count
                4 bytes for recorded frames
        error case (PDC_WRAPPER_FAILED):
            string with error message
*/
int pdc_get_mem_frame_info(UINT n_device_no, UINT n_child_no, const char * tmp_file_buffer) {
    HINSTANCE libHandle;

    PDC_GET_MEM_FRAME_INFO_FUNCTION_DLL pdc_get_mem_frame_info_function_dll;

    UINT error_code, return_value;
    PPDC_FRAME_INFO pdc_frame_info;

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

    pdc_get_mem_frame_info_function_dll = (PDC_GET_MEM_FRAME_INFO_FUNCTION_DLL) GetProcAddress(libHandle, "PDC_GetMemFrameInfo");
    if (pdc_get_mem_frame_info_function_dll == NULL) {
        const char * message = "GetProcAddress failed loading PDC_GetMemFrameInfo function";
        fwrite(message, sizeof(char), strlen(message), output_file);
        fclose(output_file);
        return PDC_WRAPPER_FAILED;
    }

    return_value = pdc_get_mem_frame_info_function_dll(n_device_no, n_child_no, &pdc_frame_info, &error_code);

    fwrite(&return_value, sizeof(UINT), 1, output_file);
    fwrite(&error_code, sizeof(UINT), 1, output_file);
    if (return_value == PDC_FAILED) {
        fclose(output_file);
        return PDC_WRAPPER_SUCCEEDED;
    }

    fwrite(&(pdc_frame_info->m_nStart), sizeof(INT), 1, output_file);
    fwrite(&(pdc_frame_info->m_nEnd), sizeof(INT), 1, output_file);
    fwrite(&(pdc_frame_info->m_nTrigger), sizeof(INT), 1, output_file);
    fwrite(&(pdc_frame_info->m_nTwoStageLowToHigh), sizeof(INT), 1, output_file);
    fwrite(&(pdc_frame_info->m_nTwoStageHighToLow), sizeof(INT), 1, output_file);
    fwrite(&(pdc_frame_info->m_nEvent), sizeof(INT), 10, output_file);
    fwrite(&(pdc_frame_info->m_nEventCount), sizeof(INT), 1, output_file);
    fwrite(&(pdc_frame_info->m_nRecordedFrames), sizeof(INT), 1, output_file);

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
int pdc_set_status(UINT n_device_no, UINT mode, const char * tmp_file_buffer) {
    HINSTANCE libHandle;

    PDC_SET_STATUS_FUNCTION_DLL pdc_set_status_function_dll;
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

    pdc_set_status_function_dll = (PDC_SET_STATUS_FUNCTION_DLL) GetProcAddress(libHandle, "PDC_SetStatus");
    if (pdc_set_status_function_dll == NULL) {
        const char * message = "GetProcAddress failed loading PDC_SetStatus function";
        fwrite(message, sizeof(char), strlen(message), output_file);
        fclose(output_file);
        return PDC_WRAPPER_FAILED;
    }

    return_value = pdc_set_status_function_dll(n_device_no, mode, &error_code);

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
        error case (PDC_WRAPPER_FAILED):
            string with error message
*/
int pdc_set_rec_ready(UINT n_device_no, const char * tmp_file_buffer) {
    HINSTANCE libHandle;

    PDC_SET_REC_READY_FUNCTION_DLL pdc_set_rec_ready_function_dll;
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

    pdc_set_rec_ready_function_dll = (PDC_SET_REC_READY_FUNCTION_DLL) GetProcAddress(libHandle, "PDC_SetRecReady");
    if (pdc_set_rec_ready_function_dll == NULL) {
        const char * message = "GetProcAddress failed loading PDC_SetRecReady function";
        fwrite(message, sizeof(char), strlen(message), output_file);
        fclose(output_file);
        return PDC_WRAPPER_FAILED;
    }

    return_value = pdc_set_rec_ready_function_dll(n_device_no, &error_code);

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
        error case (PDC_WRAPPER_FAILED):
            string with error message
*/
int pdc_set_endless(UINT n_device_no, const char * tmp_file_buffer) {
    HINSTANCE libHandle;

    PDC_SET_ENDLESS_FUNCTION_DLL pdc_set_endless_function_dll;
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

    pdc_set_endless_function_dll = (PDC_SET_ENDLESS_FUNCTION_DLL) GetProcAddress(libHandle, "PDC_SetEndless");
    if (pdc_set_endless_function_dll == NULL) {
        const char * message = "GetProcAddress failed loading PDC_SetEndless function";
        fwrite(message, sizeof(char), strlen(message), output_file);
        fclose(output_file);
        return PDC_WRAPPER_FAILED;
    }

    return_value = pdc_set_endless_function_dll(n_device_no, &error_code);

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
        error case (PDC_WRAPPER_FAILED):
            string with error message
*/
int pdc_trigger_in(UINT n_device_no, const char * tmp_file_buffer) {
    HINSTANCE libHandle;

    PDC_TRIGGER_IN_FUNCTION_DLL pdc_trigger_in_function_dll;
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

    pdc_trigger_in_function_dll = (PDC_TRIGGER_IN_FUNCTION_DLL) GetProcAddress(libHandle, "PDC_TriggerIn");
    if (pdc_trigger_in_function_dll == NULL) {
        const char * message = "GetProcAddress failed loading PDC_TriggerIn function";
        fwrite(message, sizeof(char), strlen(message), output_file);
        fclose(output_file);
        return PDC_WRAPPER_FAILED;
    }

    return_value = pdc_trigger_in_function_dll(n_device_no, &error_code);

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
        error case (PDC_WRAPPER_FAILED):
            string with error message
*/
int pdc_set_bit_depth(UINT n_device_no, UINT n_child_no, CHAR depth, const char * tmp_file_buffer) {
    HINSTANCE libHandle;

    PDC_SET_BIT_DEPTH_FUNCTION_DLL pdc_set_bit_depth_function_dll;
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

    pdc_set_bit_depth_function_dll = (PDC_SET_BIT_DEPTH_FUNCTION_DLL) GetProcAddress(libHandle, "PDC_SetBitDepth");
    if (pdc_set_bit_depth_function_dll == NULL) {
        const char * message = "GetProcAddress failed loading PDC_SetBitDepth function";
        fwrite(message, sizeof(char), strlen(message), output_file);
        fclose(output_file);
        return PDC_WRAPPER_FAILED;
    }

    return_value = pdc_set_bit_depth_function_dll(n_device_no, n_child_no, depth, &error_code);

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
        error case (PDC_WRAPPER_FAILED):
            string with error message
*/
int pdc_set_record_rate(UINT n_device_no, UINT n_child_no, UINT rate, const char * tmp_file_buffer) {
    HINSTANCE libHandle;

    PDC_SET_RECORD_RATE_FUNCTION_DLL pdc_set_record_rate_function_dll;
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

    pdc_set_record_rate_function_dll = (PDC_SET_RECORD_RATE_FUNCTION_DLL) GetProcAddress(libHandle, "PDC_SetRecordRate");
    if (pdc_set_record_rate_function_dll == NULL) {
        const char * message = "GetProcAddress failed loading PDC_SetRecordRate function";
        fwrite(message, sizeof(char), strlen(message), output_file);
        fclose(output_file);
        return PDC_WRAPPER_FAILED;
    }

    return_value = pdc_set_record_rate_function_dll(n_device_no, n_child_no, rate, &error_code);

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
        error case (PDC_WRAPPER_FAILED):
            string with error message
*/
int pdc_set_resolution(UINT n_device_no, UINT n_child_no, UINT width, UINT height, const char * tmp_file_buffer) {
    HINSTANCE libHandle;

    PDC_SET_RESOLUTION_FUNTION_DLL pdc_set_resolution_function_dll;
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

    pdc_set_resolution_function_dll = (PDC_SET_RESOLUTION_FUNTION_DLL) GetProcAddress(libHandle, "PDC_SetResolution");
    if (pdc_set_resolution_function_dll == NULL) {
        const char * message = "GetProcAddress failed loading PDC_SetResolution function";
        fwrite(message, sizeof(char), strlen(message), output_file);
        fclose(output_file);
        return PDC_WRAPPER_FAILED;
    }

    return_value = pdc_set_resolution_function_dll(n_device_no, n_child_no, width, height, &error_code);

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
        error case (PDC_WRAPPER_FAILED):
            string with error message
*/
int pdc_set_shutter_speed_fps(UINT n_device_no, UINT n_child_no, UINT fps, const char * tmp_file_buffer) {
    HINSTANCE libHandle;

    PDC_SET_SHUTTER_SPEED_FPS_FUNCTION_DLL pdc_set_shutter_speed_fps_function_dll;
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

    pdc_set_shutter_speed_fps_function_dll = (PDC_SET_SHUTTER_SPEED_FPS_FUNCTION_DLL) GetProcAddress(libHandle, "PDC_SetShutterSpeedFps");
    if (pdc_set_shutter_speed_fps_function_dll == NULL) {
        const char * message = "GetProcAddress failed loading PDC_SetShutterSpeedFps function";
        fwrite(message, sizeof(char), strlen(message), output_file);
        fclose(output_file);
        return PDC_WRAPPER_FAILED;
    }

    return_value = pdc_set_shutter_speed_fps_function_dll(n_device_no, n_child_no, fps, &error_code);

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
        error case (PDC_WRAPPER_FAILED):
            string with error message
*/
int pdc_set_trigger_mode(UINT n_device_no, UINT mode, UINT aframes, UINT rframes, UINT rcount, const char * tmp_file_buffer) {
    HINSTANCE libHandle;

    PDC_SET_TRIGGER_MODE_FUNCTION_DLL pdc_set_trigger_mode_function_dll;
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

    pdc_set_trigger_mode_function_dll = (PDC_SET_TRIGGER_MODE_FUNCTION_DLL) GetProcAddress(libHandle, "PDC_SetTriggerMode");
    if (pdc_set_trigger_mode_function_dll == NULL) {
        const char * message = "GetProcAddress failed loading PDC_SetTriggerMode function";
        fwrite(message, sizeof(char), strlen(message), output_file);
        fclose(output_file);
        return PDC_WRAPPER_FAILED;
    }

    return_value = pdc_set_trigger_mode_function_dll(n_device_no, mode, aframes, rframes, rcount, &error_code);

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
        error case (PDC_WRAPPER_FAILED):
            string with error message
*/
int pdc_set_sensor_gain_mode(UINT n_device_no, UINT n_child_no, UINT mode, const char * tmp_file_buffer) {
    HINSTANCE libHandle;

    PDC_SET_SENSOR_GAIN_MODE_FUNCTION_DLL pdc_set_sensor_gain_mode_function_dll;
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

    pdc_set_sensor_gain_mode_function_dll = (PDC_SET_SENSOR_GAIN_MODE_FUNCTION_DLL) GetProcAddress(libHandle, "PDC_SetSensorGainMode");
    if (pdc_set_sensor_gain_mode_function_dll == NULL) {
        const char * message = "GetProcAddress failed loading PDC_SetSensorGainMode function";
        fwrite(message, sizeof(char), strlen(message), output_file);
        fclose(output_file);
        return PDC_WRAPPER_FAILED;
    }

    return_value = pdc_set_sensor_gain_mode_function_dll(n_device_no, n_child_no, mode, &error_code);

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
        error case (PDC_WRAPPER_FAILED):
            string with error message
*/
int pdc_set_lut_mode(UINT n_device_no, UINT n_child_no, UINT mode, const char * tmp_file_buffer) {
    HINSTANCE libHandle;

    PDC_SET_LUT_MODE_FUNCTION_DLL pdc_set_lut_mode_function_dll;
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

    pdc_set_lut_mode_function_dll = (PDC_SET_LUT_MODE_FUNCTION_DLL) GetProcAddress(libHandle, "PDC_SetLUTMode");
    if (pdc_set_lut_mode_function_dll == NULL) {
        const char * message = "GetProcAddress failed loading PDC_SetLUTMode function";
        fwrite(message, sizeof(char), strlen(message), output_file);
        fclose(output_file);
        return PDC_WRAPPER_FAILED;
    }

    return_value = pdc_set_lut_mode_function_dll(n_device_no, n_child_no, mode, &error_code);

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
        error case (PDC_WRAPPER_FAILED):
            string with error message
*/
int pdc_set_lut_user(UINT n_device_no, UINT n_child_no, UINT mode, const char * tmp_file_buffer) {
    HINSTANCE libHandle;

    PDC_SET_LUT_USER_FUNCTION_DLL pdc_set_lut_user_function_dll;
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

    pdc_set_lut_user_function_dll = (PDC_SET_LUT_USER_FUNCTION_DLL) GetProcAddress(libHandle, "PDC_SetLUTUser");
    if (pdc_set_lut_user_function_dll == NULL) {
        const char * message = "GetProcAddress failed loading PDC_SetLUTUser function";
        fwrite(message, sizeof(char), strlen(message), output_file);
        fclose(output_file);
        return PDC_WRAPPER_FAILED;
    }

    return_value = pdc_set_lut_user_function_dll(n_device_no, n_child_no, mode, &error_code);

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
        error case (PDC_WRAPPER_FAILED):
            string with error message
*/
int pdc_set_external_out_mode(UINT n_device_no, UINT port, UINT mode, const char * tmp_file_buffer) {
    HINSTANCE libHandle;

    PDC_SET_EXTERNAL_OUT_MODE_FUNCTION_DLL pdc_set_external_out_mode_function_dll;
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

    pdc_set_external_out_mode_function_dll = (PDC_SET_EXTERNAL_OUT_MODE_FUNCTION_DLL) GetProcAddress(libHandle, "PDC_SetExternalOutMode");
    if (pdc_set_external_out_mode_function_dll == NULL) {
        const char * message = "GetProcAddress failed loading PDC_SetExternalOutMode function";
        fwrite(message, sizeof(char), strlen(message), output_file);
        fclose(output_file);
        return PDC_WRAPPER_FAILED;
    }

    return_value = pdc_set_external_out_mode_function_dll(n_device_no, port, mode, &error_code);

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
        error case (PDC_WRAPPER_FAILED):
            string with error message
*/
int pdc_set_transfer_option(UINT n_device_no, UINT n_child_no, UINT eight_bit_sel, UINT bayer, UINT interleave, const char * tmp_file_buffer) {
    HINSTANCE libHandle;

    PDC_SET_TRANSFER_OPTION_FUNCTION_DLL pdc_set_transfer_option_function_dll;
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

    pdc_set_transfer_option_function_dll = (PDC_SET_TRANSFER_OPTION_FUNCTION_DLL) GetProcAddress(libHandle, "PDC_SetTransferOption");
    if (pdc_set_transfer_option_function_dll == NULL) {
        const char * message = "GetProcAddress failed loading PDC_SetTransferOption function";
        fwrite(message, sizeof(char), strlen(message), output_file);
        fclose(output_file);
        return PDC_WRAPPER_FAILED;
    }

    return_value = pdc_set_transfer_option_function_dll(n_device_no, n_child_no, eight_bit_sel, bayer, interleave, &error_code);

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
        error case (PDC_WRAPPER_FAILED):
            string with error message
*/
int pdc_bmp_file_save(UINT n_device_no, UINT n_child_no, const char * file_name, UINT frame_no, const char * tmp_file_buffer) {
    HINSTANCE libHandle;

    PDC_BMP_FILE_SAVE_FUNCTION_DLL pdc_bmp_file_save_function_dll;
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

    pdc_bmp_file_save_function_dll = (PDC_BMP_FILE_SAVE_FUNCTION_DLL) GetProcAddress(libHandle, "PDC_BMPFileSaveA");
    if (pdc_bmp_file_save_function_dll == NULL) {
        const char * message = "GetProcAddress failed loading PDC_BMPFileSaveA function";
        fwrite(message, sizeof(char), strlen(message), output_file);
        fclose(output_file);
        return PDC_WRAPPER_FAILED;
    }

    return_value = pdc_bmp_file_save_function_dll(n_device_no, n_child_no, file_name, frame_no, &error_code);

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
        error case (PDC_WRAPPER_FAILED):
            string with error message
*/
int pdc_avi_file_save_open(UINT n_device_no, UINT n_child_no, const char * file_name, UINT rate, UINT show_compress, const char * tmp_file_buffer) {
    HINSTANCE libHandle;

    PDC_AVI_FILE_SAVE_OPEN_FUNCTION_DLL pdc_avi_file_save_open_function_dll;
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

    pdc_avi_file_save_open_function_dll = (PDC_AVI_FILE_SAVE_OPEN_FUNCTION_DLL) GetProcAddress(libHandle, "PDC_AVIFileSaveOpenA");
    if (pdc_avi_file_save_open_function_dll == NULL) {
        const char * message = "GetProcAddress failed loading PDC_AVIFileSaveOpen function";
        fwrite(message, sizeof(char), strlen(message), output_file);
        fclose(output_file);
        return PDC_WRAPPER_FAILED;
    }

    return_value = pdc_avi_file_save_open_function_dll(n_device_no, n_child_no, file_name, rate, show_compress, &error_code);

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
            4 bytes for file size expressed in bytes
        error case (PDC_WRAPPER_FAILED):
            string with error message
*/
int pdc_avi_file_save(UINT n_device_no, UINT n_child_no, UINT frame_no, const char * tmp_file_buffer) {
    HINSTANCE libHandle;

    PDC_AVI_FILE_SAVE_FUNCTION_DLL pdc_avi_file_save_function_dll;
    UINT error_code, return_value;
    UINT size;

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

    pdc_avi_file_save_function_dll = (PDC_AVI_FILE_SAVE_FUNCTION_DLL) GetProcAddress(libHandle, "PDC_AVIFileSave");
    if (pdc_avi_file_save_function_dll == NULL) {
        const char * message = "GetProcAddress failed loading PDC_AVIFileSave function";
        fwrite(message, sizeof(char), strlen(message), output_file);
        fclose(output_file);
        return PDC_WRAPPER_FAILED;
    }

    return_value = pdc_avi_file_save_function_dll(n_device_no, n_child_no, frame_no, &size, &error_code);

    fwrite(&return_value, sizeof(UINT), 1, output_file);
    fwrite(&error_code, sizeof(UINT), 1, output_file);
    fwrite(&size, sizeof(UINT), 1, output_file);
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
int pdc_avi_file_save_close(UINT n_device_no, UINT n_child_no, const char * tmp_file_buffer) {
    HINSTANCE libHandle;

    PDC_AVI_FILE_SAVE_CLOSE_FUNCTION_DLL pdc_avi_file_save_close_function_dll;
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

    pdc_avi_file_save_close_function_dll = (PDC_AVI_FILE_SAVE_CLOSE_FUNCTION_DLL) GetProcAddress(libHandle, "PDC_AVIFileSaveClose");
    if (pdc_avi_file_save_close_function_dll == NULL) {
        const char * message = "GetProcAddress failed loading PDC_AVIFileSaveClose function";
        fwrite(message, sizeof(char), strlen(message), output_file);
        fclose(output_file);
        return PDC_WRAPPER_FAILED;
    }

    return_value = pdc_avi_file_save_close_function_dll(n_device_no, n_child_no, &error_code);

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
        error case (PDC_WRAPPER_FAILED):
            string with error message
*/
int pdc_mraw_file_save_open(UINT n_device_no, UINT n_child_no, const char * file_name, UINT raw_bit_depth, UINT max_frame_num, const char * tmp_file_buffer) {
    HINSTANCE libHandle;

    PDC_MRAW_FILE_SAVE_OPEN_FUNCTION_DLL pdc_mraw_file_save_open_function_dll;
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

    pdc_mraw_file_save_open_function_dll = (PDC_MRAW_FILE_SAVE_OPEN_FUNCTION_DLL) GetProcAddress(libHandle, "PDC_MRAWFileSaveOpenA");
    if (pdc_mraw_file_save_open_function_dll == NULL) {
        const char * message = "GetProcAddress failed loading PDC_MRAWFileSaveOpenA function";
        fwrite(message, sizeof(char), strlen(message), output_file);
        fclose(output_file);
        return PDC_WRAPPER_FAILED;
    }

    return_value = pdc_mraw_file_save_open_function_dll(n_device_no, n_child_no, file_name, raw_bit_depth, max_frame_num, &error_code);

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
        error case (PDC_WRAPPER_FAILED):
            string with error message
*/
int pdc_mraw_file_save(UINT n_device_no, UINT n_child_no, UINT n_frame_no, const char * tmp_file_buffer) {
    HINSTANCE libHandle;

    PDC_MRAW_FILE_SAVE_FUNCTION_DLL pdc_mraw_file_save_function_dll;
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

    pdc_mraw_file_save_function_dll = (PDC_MRAW_FILE_SAVE_FUNCTION_DLL) GetProcAddress(libHandle, "PDC_MRAWFileSave");
    if (pdc_mraw_file_save_function_dll == NULL) {
        const char * message = "GetProcAddress failed loading PDC_MRAWFileSave function";
        fwrite(message, sizeof(char), strlen(message), output_file);
        fclose(output_file);
        return PDC_WRAPPER_FAILED;
    }

    return_value = pdc_mraw_file_save_function_dll(n_device_no, n_child_no, n_frame_no, &error_code);

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
        error case (PDC_WRAPPER_FAILED):
            string with error message
*/
int pdc_mraw_file_save_close(UINT n_device_no, UINT n_child_no, const char * tmp_file_buffer) {
    HINSTANCE libHandle;

    PDC_MRAW_FILE_SAVE_CLOSE_FUNCTION_DLL pdc_mraw_file_save_close_function_dll;
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

    pdc_mraw_file_save_close_function_dll = (PDC_MRAW_FILE_SAVE_CLOSE_FUNCTION_DLL) GetProcAddress(libHandle, "PDC_MRAWFileSaveClose");
    if (pdc_mraw_file_save_close_function_dll == NULL) {
        const char * message = "GetProcAddress failed loading PDC_MRAWFileSaveClose function";
        fwrite(message, sizeof(char), strlen(message), output_file);
        fclose(output_file);
        return PDC_WRAPPER_FAILED;
    }

    return_value = pdc_mraw_file_save_close_function_dll(n_device_no, n_child_no, &error_code);

    fwrite(&return_value, sizeof(UINT), 1, output_file);
    fwrite(&error_code, sizeof(UINT), 1, output_file);
    fclose(output_file);

    return PDC_WRAPPER_SUCCEEDED;
}