using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Runtime.InteropServices;

namespace LpsPkgMnfstDcpt {
    internal class LapisCpp {
        [DllImport("liblapis.dll", EntryPoint = "Lapis_Decrypt", CallingConvention = CallingConvention.Cdecl)]
        public static extern void Lapis_Decrypt(ref byte buff, int key, int start, int size, int startIdx);
    }
}
