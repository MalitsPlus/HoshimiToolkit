using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.IO;
using System.Security.Cryptography;
using ICSharpCode.SharpZipLib.GZip;
using System.Runtime.Serialization.Formatters.Binary;
using Oz.GameKit.Version;

namespace LpsPkgMnfstDcpt {
    internal class Program {
        static void Main(string[] args) {
            write2File();
            PackageManifest packageInfo;
            string decFile = "gziped.bin";
            using (FileStream fs = File.OpenRead(decFile)) {
                BinaryFormatter formatter = new BinaryFormatter();
                packageInfo = (PackageManifest)formatter.Deserialize(fs);
            }

        }

        private static void write2File() {
            string path = "manifest.xml";
            byte[] key = hexString2Bytes("9ec473ae662f4e2a592a502b903c9ec473ae662f4e2a8d857ea7592750bb903c");
            byte[] iv = hexString2Bytes("f184dfb4912bce95dbdb7d975397723f");

            RijndaelManaged rijndael = new RijndaelManaged() {
                Mode = CipherMode.CBC,
                KeySize = 128,
                BlockSize = 128,
                Padding = PaddingMode.PKCS7,
                Key = key,
                IV = iv,
            };

            using (FileStream fs = File.OpenRead(path)) {
                using (CryptoStream crptStm = new CryptoStream(fs, rijndael.CreateDecryptor(), CryptoStreamMode.Read)) {
                    using (GZipInputStream gStream = new GZipInputStream(crptStm)) {
                        using (FileStream outFs = File.Create("gziped.bin")) {
                            gStream.CopyTo(outFs);
                        }
                    }
                }
            }
        }

        private static byte[] hexString2Bytes(string hexString) {
            byte[] result = new byte[hexString.Length / 2];
            int cur = 0;
            for (int i = 0; i < hexString.Length; i = i + 2) {
                string w = hexString.Substring(i, 2);
                result[cur] = Convert.ToByte(w, 16);
                cur++;
            }
            return result;
        }
    }
}
