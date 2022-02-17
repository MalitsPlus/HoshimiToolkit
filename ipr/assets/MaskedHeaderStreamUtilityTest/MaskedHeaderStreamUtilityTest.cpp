#define _CRT_SECURE_NO_WARNINGS

#include <iostream>
#include <fstream>

void StringToMaskBytes(uint16_t* maskString, uint32_t maskLen, uint8_t* maskBytes, int32_t bytesLength)
{
    uint8_t b;
    uint8_t char_j;
    int i;
    __int64 j;
    int k;
    __int64 l;
    __int64 m;
    int v13;
    uint8_t* pMaskBytes;
    int v16;
    uint32_t maskStringLength;

    if (maskString != 0) {
        maskStringLength = maskLen;
        if ((int)maskStringLength >= 1) {
            i = 0;
            j = 0LL;
            k = bytesLength - 1;
            do {
                char_j = maskString[j++];
                maskBytes[i] = char_j;
                i += 2;
                maskBytes[k] = ~char_j;
                k -= 2;
            } while (maskStringLength != j);  
        }
        if (bytesLength >= 1) {
            l = (unsigned int)bytesLength;
            v13 = 0x9B;
            m = (unsigned int)bytesLength;
            pMaskBytes = maskBytes;
            do
            {
                v16 = *pMaskBytes++;
                --m;
                v13 = (((v13 & 1) << 7) | (v13 >> 1)) ^ v16;
            } while (m);
            b = 0;
            do
            {
                --l;
                maskBytes[b] ^= (uint8_t)v13;   // 必须先强转为单字节
                b++;
            } while (l);
        }
        return;
    }
}

void CryptByString(uint8_t* input, int32_t input_len, uint8_t** output, uint8_t* maskString, uint8_t maskStringlen, int32_t offset, uint64_t streamPos, uint64_t headerLength) // int32_t count
{
    __int64 i;
    int k;
    uint32_t byteslen;
    uint8_t* maskBytes;

    uint8_t* buffer = (uint8_t*)malloc(input_len);
    memcpy(buffer, input, input_len);

    byteslen = maskStringlen << 1;
    maskBytes = (uint8_t*)malloc(byteslen);
    memset(maskBytes, 0x00, byteslen);
StringToMaskBytes((uint16_t*)maskString, maskStringlen, maskBytes, byteslen);
i = 0;
do {
    buffer[offset + i] ^= maskBytes[streamPos + i - (streamPos + i) / byteslen * byteslen];
    i++;
} while (streamPos + i < headerLength);

    *output = buffer;

    free(maskBytes); 
    return;
}

int main()
{
    std::ifstream ifs("Debug/694ff80f3f7b6c8696ecde3d5c3fc027", std::ios::binary | std::ios::ate);
    std::streamsize size = ifs.tellg();
    ifs.seekg(0, std::ios::beg);

    if (ifs.fail())
    {
        std::cerr << "Error: " << strerror(errno);
        return -1;
    }

    uint8_t* buff = (uint8_t*)malloc(size);

    ifs.read((char*)buff, size);
    ifs.close();

    uint8_t* outputbuff = (uint8_t*)malloc(size);
    uint8_t** output = &outputbuff;

    char16_t maskString16[] = u"sud_vo_home_ktn_talk-12-5";

    int stringLength = sizeof(maskString16) / sizeof(maskString16[0]) - 1;  // c++会胜手在字符串最后加个\0

    CryptByString(buff, (int32_t)size, output, (uint8_t*)maskString16, stringLength, 0, 0, 256);
}