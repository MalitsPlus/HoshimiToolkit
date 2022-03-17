
string pathStr = "UserResponse";
byte[] data = CryptoHelper.get().doDecrypt("UserResponse/userClientGetAsync220317174823119.bin");
File.WriteAllBytes("userdata.bin", data);
JsonHelper.generateJson<UserGetResponse>(data, "UserGetResponse");
int a = 0;