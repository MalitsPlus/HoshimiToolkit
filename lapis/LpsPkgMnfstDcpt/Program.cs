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
using Oz.GameFramework.Runtime;

namespace LpsPkgMnfstDcpt {
    internal class Program {
        static void Main(string[] args) {

            string path = Directory.GetCurrentDirectory();
            DirectoryInfo dir = new DirectoryInfo(path);
            string lapisRoot = GetLapisRoot(dir).FullName;

            string encFilePath = lapisRoot + "\\EncryptedFiles";
            string decFilePath = lapisRoot + "\\DecryptedFiles";
            string encManifest = encFilePath + "\\manifest.xml";

            // decrypt manifest 
            Write2File(encManifest);

            // deserialize the binary file to an object 
            PackageManifest packageManifest;
            using (FileStream fs = File.OpenRead("gziped.bin")) {
                BinaryFormatter formatter = new BinaryFormatter();
                packageManifest = (PackageManifest)formatter.Deserialize(fs);
            }
            var packageInfos = packageManifest.m_PackageInfos;

            // idk why but there seems to be some null objects interspersed among the list 
            packageInfos.RemoveAll(it => it == null);
            // also with some non-null but nonsense objects 
            packageInfos.RemoveAll(it => it.Name == null);

            int i = 1;
            int allCount = packageInfos.Count;
            int errCount = 0;
            List<IPackageInfo> errorAbs = new List<IPackageInfo>();
            foreach (var item in packageInfos) {
                if (item is AssetBundleInfo) {
                    AssetBundleInfo ab = (AssetBundleInfo)item;
                    string inAbPath = $"{encFilePath}\\{item.Name}.bdl";
                    string outAbPath = $"{decFilePath}\\{item.Name}.bdl";
                    inAbPath = inAbPath.Replace("/", "\\");
                    outAbPath = outAbPath.Replace("/", "\\");
                    string outAbDirectory = outAbPath.Remove(outAbPath.LastIndexOf("\\"));

                    byte[] buffer;
                    try {
                        buffer = File.ReadAllBytes(inAbPath);
                        int size = buffer.GetLength(0);
                        LapisDecrypt(ref buffer[0], ab.EncryptKey, 0, size, 0);
                        if (IsUnity(buffer)) {
                            Directory.CreateDirectory(outAbDirectory);
                            File.WriteAllBytes(outAbPath, buffer);
                            Console.WriteLine($"({i}/{allCount}) '{item.Name}' has been successfully decrypted.");
                        } else {
                            throw new Exception("Not an unity assetbundle file.");
                        }
                    } catch(Exception ex) {
                        errCount++;
                        errorAbs.Add(item);
                        Console.ForegroundColor = ConsoleColor.Red;
                        Console.WriteLine($"({i}/{allCount}) Decrypt '{item.Name}' failed.");
                        Console.ForegroundColor = ConsoleColor.White;
                        //throw ex;
                    } finally {
                        i++;
                    }
                }
            }
            foreach (var item in errorAbs) {
                Console.ForegroundColor = ConsoleColor.Red;
                Console.WriteLine($"[ERROR] Decrypt '{item.Name}' failed.");
                Console.ForegroundColor = ConsoleColor.White;
            }
            Console.WriteLine($"Decrypt operations all done, {errCount} error(s) occurred during process.");
            Console.ReadKey();

            // get all *.bdl files in EncryptedFiles directory 
            //var pathDic = new Dictionary<string, string>();
            //GetPathDic(encFilePath, ref pathDic);
        }

        private static void LapisDecrypt(ref byte buff, int key, int start, int size, int startIdx) {
            LapisCpp.Lapis_Decrypt(ref buff, key, start, size, startIdx);
        }

        private static bool IsUnity(byte[] buffer) {
            return buffer[0] == 0x55
                && buffer[1] == 0x6E
                && buffer[2] == 0x69
                && buffer[3] == 0x74
                && buffer[4] == 0x79
                && buffer[5] == 0x46
                && buffer[6] == 0x53;
        }

        private static void GetPathDic(string path, ref Dictionary<string, string> dic) {
            DirectoryInfo directoryInfo = new DirectoryInfo(path);
            foreach (var item in directoryInfo.GetFiles()) {
                if (item.Name.EndsWith(".bdl")) {
                    dic.Add(item.Name, item.FullName);
                }
            }
            foreach (var item in directoryInfo.GetDirectories()) {
                GetPathDic(item.FullName, ref dic);
            }
        }

        private static DirectoryInfo GetLapisRoot(DirectoryInfo dir) {
            if (dir.Name == "lapis") {
                return dir;
            } else {
                dir = GetLapisRoot(dir.Parent);
            }

            if (dir.Name != "lapis") 
                throw new DirectoryNotFoundException("Cannot find 'lapis' directory.");

            return dir;
        }

        private static void Write2File(string path) {
            byte[] key = HexString2Bytes("9ec473ae662f4e2a592a502b903c9ec473ae662f4e2a8d857ea7592750bb903c");
            byte[] iv = HexString2Bytes("f184dfb4912bce95dbdb7d975397723f");

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

        private static byte[] HexString2Bytes(string hexString) {
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
