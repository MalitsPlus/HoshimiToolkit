using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Security.Cryptography;

namespace ProtobufNet {
    internal class CryptoHelper {
        static string keyStr = "AJRnFaOnOj";
        static byte[] key = MD5.HashData(Encoding.UTF8.GetBytes(keyStr));
        static CryptoHelper instance;

        internal static CryptoHelper get() {
            if (instance == null) 
                instance = new CryptoHelper();
            return instance;
        }

        byte[] HexString2Bytes(string hexString) {
            byte[] result = new byte[hexString.Length / 2];
            int cur = 0;
            for (int i = 0; i < hexString.Length; i = i + 2) {
                string w = hexString.Substring(i, 2);
                result[cur] = Convert.ToByte(w, 16);
                cur++;
            }
            return result;
        }

        byte[] createAesIv(byte[] key, byte[] header) {
            MD5 md5 = MD5.Create();
            md5.TransformBlock(key, 0, key.Length, null, 0);
            md5.TransformFinalBlock(header, 0, header.Length);
            return md5.Hash ?? throw new NullReferenceException("key and header cannot be null.");
        }

        byte[] decryptTraffic(Stream stream) {
            Aes aes = Aes.Create();
            aes.Mode = CipherMode.CBC;
            aes.KeySize = 128;
            aes.BlockSize = 128;
            aes.Padding = PaddingMode.PKCS7;

            byte[] flag = new byte[4];
            if (stream.Read(flag, 0, 4) != 4) {
                throw new InvalidDataException("Input stream is invalid.");
            }
            int headerLen = flag[3];
            byte[] header = new byte[headerLen];
            if (stream.Read(header, 0, headerLen) != headerLen) {
                throw new InvalidDataException("Input stream is invalid.");
            }
            byte[] iv = createAesIv(Encoding.UTF8.GetBytes(keyStr), header);
            ICryptoTransform decryptor = aes.CreateDecryptor(key, iv);

            byte[] body;
            using (MemoryStream ms = new MemoryStream()) {
                stream.CopyTo(ms);
                body = ms.ToArray();
            }
            byte[] result;
            using (MemoryStream ms = new MemoryStream()) {
                using (CryptoStream cs = new CryptoStream(ms, decryptor, CryptoStreamMode.Write)) {
                    cs.Write(body, 0, body.Length);
                    cs.FlushFinalBlock();
                    result = ms.ToArray();
                }
            }
            return result;
        }

        internal byte[] doDecrypt(string file) {
            byte[] data;
            using (FileStream fs = File.OpenRead(file)) {
                data = decryptTraffic(fs);
            }
            return data;
        }
    }
}
