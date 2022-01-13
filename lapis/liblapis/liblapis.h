#pragma once

#ifdef LIBLAPIS_EXPORTS
#define LIBLAPIS_EXPORTS_API __declspec(dllexport)
#else
#define LIBLAPIS_EXPORTS_API __declspec(dllimport)
#endif

#define BYTE4(v)					((uint8_t) (v))
#define BYTE3(v)					((uint8_t) (((uint32_t) (v)) >> 8))
#define BYTE2(v)					((uint8_t) (((uint32_t) (v)) >> 16))
#define BYTE1(v)					((uint8_t) (((uint32_t) (v)) >> 24))

extern "C" LIBLAPIS_EXPORTS_API void Lapis_Decrypt(uint8_t* result, int key, int start, int size, int startIdx);