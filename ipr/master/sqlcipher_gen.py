import json
from pathlib import Path

cache_path = "caches"
db_cache_path = "caches/master/EB0A191797624DD3A48FA681D3061212"
db_out_path = "caches/master/plain"

def do_gen():
    l: list = json.loads(Path(f"{cache_path}/master_key.json").read_text())
    s = ""
    for it in l:
        file_name = it["file_name"]
        name = it["name"]
        key = it["key"]
        cmd = f""".open {db_cache_path}/{file_name}
PRAGMA key = "{key}";
ATTACH DATABASE '{db_out_path}/{name}.db' AS {name} KEY '';
SELECT sqlcipher_export('{name}');
DETACH DATABASE {name};
"""
        s += cmd
    Path(f"{cache_path}/sqlcipher_gen.sql").write_text(s)

if __name__ == "__main__":
    do_gen()
