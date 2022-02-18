import re
from pathlib import Path

cs_file = "caches/dump.cs"
feature_file = "caches/pb_sp.cs"
original_str: Path
good_str = ""

def analyze_enum():
    name = re.search(r"public enum (\w)")

def get_point():
    feature = [
        "Solis.Common.Proto\n",
        "Solis.Common.Proto.Transaction\n", 
        "Solis.Common.Proto.Api\n", 
        "Solis.Common.Proto.Master\n"
    ]
    for it in feature:
        get_str(it)
    Path(feature_file).write_text(good_str, encoding="utf-8")

def get_str(feature: str):
    global good_str
    pattern = feature + r"(?P<content>[\s\S]+?)" + r"// Namespace:"
    m = re.findall(pattern, original_str)
    for it in m:
        good_str += f"// Namespace: {feature}" + it

if __name__ == "__main__":
    original_str = Path(cs_file).read_text(encoding="utf-8")
    get_point()
