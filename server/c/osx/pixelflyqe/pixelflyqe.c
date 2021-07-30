#include <stdio.h>
#include "pixelflyqe.h"

int init(int int_param, float float_param) {
    float some_calculation = int_param * float_param;
    printf("int: %d float %.1f, calculation  %.1f\n", int_param, float_param, some_calculation);
    return -1;
}