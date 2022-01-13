#include "pch.h" // use stdafx.h in Visual Studio 2017 and earlier
#include <utility>
#include "liblapis.h"

void Lapis_Decrypt(uint8_t* result, int key, int start, int size, int startIdx) {
    int v5;
    unsigned int v6;
    int v7;
    int v8;

    int key_mod = key % 10;
    if (key % 10 < 0) {
        key_mod = -key_mod; // in IDA pseudocode we get a ~ actually, but for some reasons we should use - here 
    }
    int step = key_mod + 1;

    v5 = key / 10 % 10;
    if (v5 < 0)
        v5 = -v5;   // in IDA pseudocode we get a ~ actually, but for some reasons we should use - here 
    while (1)
    {
        v7 = start >= size ? 905677402 : -1904922419;
        if (v7 != -1904922419)
            break;
        v6 = 1103515245 * startIdx + 77880;
        if (1103515245 * startIdx + 12345 >= 0)
            v6 = 1103515245 * startIdx + 12345;
        *(result + start) ^= key >> (BYTE2(v6) - (HIWORD(v6) & 0x7FFF) / (unsigned int)(v5 + 1) * (v5 + 1));
        ++startIdx;
        start += step;
    }
}