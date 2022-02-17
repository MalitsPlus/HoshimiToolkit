using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace SqlCipherTest {
    internal class Program {
        static void Main(string[] args) {

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
