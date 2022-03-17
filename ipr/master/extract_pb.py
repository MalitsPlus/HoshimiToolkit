import sqlite3
from pathlib import Path
from unittest.mock import patch

db_path = "caches/master/plain"
pb_path = "caches/master/pb"

def extract_bin(id, data):
    path = Path(f"{pb_path}/setting_{id}.bin")
    path.write_bytes(data)

db_files = [it for it in Path(db_path).glob("*")]
for db_file in db_files:
    if db_file.name in ["AssetDownload.db"]:
        continue
    # Test file name
    if db_file.name != "Card.db":
        continue
    conn = sqlite3.connect(db_file.absolute())
    c = conn.cursor()
    cursor_db = c.execute(f"SELECT name FROM sqlite_master WHERE type='table'")
    for row in cursor_db:
        tb_name = row[0]
        cursor_tb = c.execute(
            f"SELECT * FROM {tb_name}")
        for row_tb in cursor_tb:
            id = row_tb[0]
            data = row_tb[1]
            path = Path(f"{pb_path}/card_{id}.bin")
            path.write_bytes(data)
            # extract_bin(id, data)
