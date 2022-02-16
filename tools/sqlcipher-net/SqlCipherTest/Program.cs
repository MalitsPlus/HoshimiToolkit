using SQLite;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace SqlCipherTest {
    internal class Program {
        static void Main(string[] args) {
            string path = "76A40E4F974FD895A0A2598C1CEE28B4_D3F567B42A0C91531AA3A6E219245030";
            byte[] keybytes = HexString2Bytes("5a4e524d74714e343170354e346b67504c6b4b35734f5257314f396f58613354");

            var options = new SQLiteConnectionString(path, true, key: keybytes);
            var encryptedDb = new SQLiteConnection(options);
            encryptedDb.GetTableInfo("sqlite_master");

            var a = 1;
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
