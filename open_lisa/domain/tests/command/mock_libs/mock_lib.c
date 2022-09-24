#include <stdio.h>
#include <errno.h>
#include <string.h>
#include "mock_lib.h"


float multiply(float a, float b) {
    float return_value = a * b;
    return return_value;
}

int sum(int a, int b) {
    return a + b;
}

void create_file(char* filename) {
    FILE* f = fopen(filename,"w+b");
    if (f == NULL) {
        printf("[create_file] fopen error: %s", strerror(errno));
    }
    fclose(f);
}

char* echo(char* message) {
    return message;
}

int copy_image(const char * mock_image_path, const char* tmp_file_buffer) {
    FILE* input_file, *output_file = NULL;
    unsigned char buffer[512];

    input_file = fopen(mock_image_path,"rb");
    output_file = fopen(tmp_file_buffer,"w+b");
    if (input_file == NULL) {
        if (output_file != NULL) {
            const char * message = "[copy_image] error opening input file";
            fwrite(message, sizeof(char), strlen(message), output_file);
            fclose(output_file);
        }
        fprintf(stderr, "[copy_image] error opening input file: %s\n", strerror(errno));
        return -1;
    }

    if (output_file == NULL) {
        fclose(input_file);
        fprintf(stderr, "error opening output file: %s\n", strerror(errno));
        return -1;
    }
    size_t read_elements = fread(buffer, sizeof(unsigned char), 512, input_file);
    while (read_elements) {
        fwrite(buffer, sizeof(unsigned char), read_elements, output_file);
        read_elements = fread(buffer, sizeof(unsigned char), 512, input_file);
    }

    fclose(input_file);
    fclose(output_file);
    return 0;
}