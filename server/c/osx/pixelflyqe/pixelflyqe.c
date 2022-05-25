#include <stdio.h>
#include <errno.h>
#include <string.h>
#include "pixelflyqe.h"

extern int errno;

int init(int int_param, float float_param) {
    float some_calculation = int_param * float_param;
    printf("int: %d float %.1f, calculation  %.1f\n", int_param, float_param, some_calculation);
    return -1;
}

int close(void) {
  // TODO: Add code for free cammera resources
  return -1;
}

int get_image(char * file_path) {
  // Simulation of getting image data from a file and returning in a file
  FILE* input_file, *output_file = NULL;
  unsigned char buffer[512];
  // TODO: rename this path
  const char* mock_image_path = "/Users/ariel.alvarez/Repositories/fiuba/taller-iii/electronic-instrument-adapter/server/c/osx/pixelflyqe/mockimg.jpg";
  printf("[get_image] file path provided: %s\n", file_path);
  input_file = fopen(mock_image_path,"rb");
  if (input_file == NULL) {
    fprintf(stderr, "error opening input file: %s\n", strerror(errno));
    return -1;
  }

  output_file = fopen(file_path,"w+b");
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