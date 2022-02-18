import re
from pathlib import Path

cs_file = "caches/dump.cs"
out_file = "caches/dump.proto"
original_str: Path

def gen_enum(name, properties) -> str:
    txt = f"enum {name}" + "{\n"
    for it in properties:
        txt += f"  {it[0]} = {it[1]};\n"
    txt += "}\n\n"
    return txt

def analyze_enum() -> str:
    feature = "Solis.Common.Proto\n"
    pattern = feature + r"(?P<content>[\s\S]+?)" + r"// Namespace:"
    m = re.findall(pattern, original_str)
    txt = ""
    for it in m:
        m = re.search(r"public enum (?P<name>\w+)", it)
        if m:
            name = m.group("name")
            properties = re.findall(f"public const {name} (?P<k>\\w+) = (?P<v>\\d+)", it)
            txt += gen_enum(name, properties)
    return txt
    
def analyze_master():
    feature = "Solis.Common.Proto.Master\n"

def analyze_api():
    feature = "Solis.Common.Proto.Api\n"

def analyze_trans():
    feature = "Solis.Common.Proto.Transaction\n"

if __name__ == "__main__":
    original_str = Path(cs_file).read_text(encoding="utf-8")
    txt = ""
    txt += analyze_enum()
    Path(out_file).write_text(txt, encoding="utf-8")
