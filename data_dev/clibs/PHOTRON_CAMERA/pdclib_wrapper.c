#include <stdio.h>
#include <Windows.h>
#include <errno.h>
#include "include/PDCDEV.h"
#include "include/PDCVALUE.h"
#include "include/PDCSTR.h"

/*	Wrapper Return Values	*/
#define	PDC_WRAPPER_SUCCEEDED				0
#define	PDC_WRAPPER_FAILED					-1

/*
    unsigned long PDC_Init(
        unsigned long *pErrorCode
    )
*/
typedef UINT (CALLBACK* PDC_INIT_FUNCTION_DLL)(UINT*);

FILE* open_tmp_file_buffer(const char * tmp_file_buffer) {
    FILE* output_file = fopen(tmp_file_buffer, "wb");
    if (output_file == NULL) {
        fprintf(stderr, "error opening temp file buffer: %s\n", strerror(errno));
    }

    return output_file;
}

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