using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ProtobufNet {
    internal class JsonHelper {
        static string outputDir = "json";

        internal static void generateJsonDir<T>(string pathStr) {
            List<T> list = new List<T>();
            DirectoryInfo directoryInfo = new DirectoryInfo(pathStr);
            foreach (var file in directoryInfo.EnumerateFiles()) {
                using (var stream = file.OpenRead()) {
                    var obj = Serializer.Deserialize<T>(stream);
                    list.Add(obj);
                }
            }
            var options = new JsonSerializerOptions {
                WriteIndented = true,
                Encoder = System.Text.Encodings.Web.JavaScriptEncoder.Create(System.Text.Unicode.UnicodeRanges.All)
            };
            string s = JsonSerializer.Serialize(list, options);

            string output = $"{outputDir}/{pathStr}.json";
            File.WriteAllText(output, s);
        }

        internal static void generateJson<T>(byte[] data, string name) {
            T obj;
            using (MemoryStream ms = new MemoryStream()) {
                ms.Write(data, 0, data.Length);
                ms.Flush();
                ms.Seek(0, SeekOrigin.Begin);
                obj = Serializer.Deserialize<T>(ms);
            }

            var options = new JsonSerializerOptions {
                WriteIndented = true,
                Encoder = System.Text.Encodings.Web.JavaScriptEncoder.Create(System.Text.Unicode.UnicodeRanges.All)
            };
            string s = JsonSerializer.Serialize(obj, options);

            string output = $"{outputDir}/{name}.json";
            File.WriteAllText(output, s);
        }
    }
}
