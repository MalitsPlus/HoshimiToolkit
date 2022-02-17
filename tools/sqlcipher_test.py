import ctypes

from sqlalchemy import null

sqlite3 = ctypes.CDLL("tools/caches/sqlite3.dll")
db = null
p = ctypes.c_void_p()
c = sqlite3.sqlite3_open(
    "76A40E4F974FD895A0A2598C1CEE28B4_D3F567B42A0C91531AA3A6E219245030", p)
a = 1
