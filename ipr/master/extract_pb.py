import sqlite3
from pathlib import Path
from unittest.mock import patch

db_path = "caches/master/plain"
pb_path = "caches/master/pb"

def extract_bin(v1, v2, v3):
    path = Path(f"{pb_path}/staff_level_{v1}_{v2}.bin")
    path.write_bytes(v3)

db_files = [it for it in Path(db_path).glob("*")]
for db_file in db_files:
    if db_file.name in ["AssetDownload.db"]:
        continue
    # Test file name
    if db_file.name != "StaffLevel.db":
        continue
    conn = sqlite3.connect(db_file.absolute())
    c = conn.cursor()
    cursor_db = c.execute(f"SELECT name FROM sqlite_master WHERE type='table'")
    for row in cursor_db:
        tb_name = row[0]
        cursor_tb = c.execute(
            f"SELECT * FROM {tb_name}")
        for row_tb in cursor_tb:
            v1 = row_tb[0]
            v2 = row_tb[1]
            v3 = row_tb[2]
            extract_bin(v1, v2, v3)
