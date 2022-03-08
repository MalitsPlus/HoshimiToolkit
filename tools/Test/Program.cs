using System.Security.Cryptography;

//byte[] key = HexString2Bytes("414a526e46614f6e4f6a");
//byte[] dataBytes = HexString2Bytes("0f00000d7371365447586d6b33544445462bf7ed5918ee131e2a48d6fc2f203ea9");
//MD5CryptoServiceProvider crypto = new MD5CryptoServiceProvider();

//crypto.TransformBlock(key, 0, key.Length, null, 0);
//byte[] header = crypto.TransformFinalBlock(dataBytes, 4, 13);
//string headerHexString = BitConverter.ToString(header).Replace("-", "");

//byte[] hash = crypto.Hash;
//string hashHex = BitConverter.ToString(hash).Replace("-", "");



//MD5CryptoServiceProvider crypto2 = new MD5CryptoServiceProvider();
//crypto2.TransformFinalBlock(key, 0, key.Length);
//string b = BitConverter.ToString(crypto2.Hash).Replace("-", "");


//byte[] data = HexString2Bytes("2bf7ed5918ee131e2a48d6fc2f203ea9");
byte[] key = HexString2Bytes("ecf522119ce6d70f58acd9bb7cc222f2");
byte[] iv = HexString2Bytes("ed12f8b4f696a9c766156b70b31cfe4e");
byte[] result;

byte[] data = File.ReadAllBytes("dec_keys.bin");

Aes aes = Aes.Create();
aes.Mode = CipherMode.CBC;
aes.KeySize = 128;
aes.BlockSize = 128;
aes.Padding = PaddingMode.PKCS7;
aes.Key = key;
aes.IV = iv;

ICryptoTransform decryptor = aes.CreateDecryptor(key, iv);

using (MemoryStream ms = new MemoryStream()) {
    using (CryptoStream cs = new CryptoStream(ms, decryptor, CryptoStreamMode.Write)) {
        cs.Write(data, 0, data.Length);
        cs.FlushFinalBlock();
        result = ms.ToArray();
    }
}

File.WriteAllBytes("dec.bin", result);
//string r = BitConverter.ToString(result, 0, result.Length).Replace("-", "");
int a = 1;

static byte[] HexString2Bytes(string hexString) {
    byte[] result = new byte[hexString.Length / 2];
    int cur = 0;
    for (int i = 0; i < hexString.Length; i = i + 2) {
        string w = hexString.Substring(i, 2);
        result[cur] = Convert.ToByte(w, 16);
        cur++;
    }
    return result;
}

