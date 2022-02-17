import re
import json
from pathlib import Path

path = Path("caches/master_key_log.txt")
ltr = path.read_text()
key_list = []
m = re.findall(
    r"masterName is (?P<name>\w+)[\s\S]*?idolypride/files/EB0A191797624DD3A48FA681D3061212/(?P<file_name>\w+)[\s\S]*?cryptoKey is (?P<key>\w+)", ltr)
for it in m:
    name = it[0]
    file_name = it[1]
    key = bytes.fromhex(it[2]).decode(encoding="utf-8")
    key_list.append({
        "name": name,
        "file_name": file_name,
        "key": key
    })
j = json.dumps(key_list, indent=4)
path = Path("caches/master_key.json")
path.write_text(j)
