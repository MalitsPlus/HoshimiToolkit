import re
from pathlib import Path

cs_file = "caches/pb_sp.cs"
out_file_enum = "caches/ProtoEnum.cs"
out_file_master = "caches/Master.cs"
out_file_api = "caches/Api.cs"
out_file_transaction = "caches/Transaction.cs"
original_str: str

# Enum Patterns
enum_ptn = r"Solis.Common.Proto\n(?P<content>[\s\S]+?)// Namespace:"
enum_name_ptn = r"public enum (?P<name>\w+)"
enum_properties_ptn = r"public const \w+ (?P<k>\w+) = (?P<v>\d+);"

# Common Patterns
common_name_ptn = r"public sealed class (?P<name>\w+)"
common_properties_ptn = r"public const int (?P<fieldName>\w+) = (?P<value>\d+);[\s\S]*?private (readonly )?(?P<type>[\w<>]+) (?P<name>\w+);"

# Master patterns
master_ptn = r"Solis.Common.Proto.Master\n(?P<content>[\s\S]+?)// Namespace:"
# Api patterns 
api_ptn = r"Solis.Common.Proto.Api\n(?P<content>[\s\S]+?)// Namespace:"
# Transaction patterns
transaction_ptn = r"Solis.Common.Proto.Transaction\n(?P<content>[\s\S]+?)// Namespace:"

# Pairs & Generations
enum_pairs = "    [ProtoMember({v})] {k},\n"
enum_text = """[ProtoContract]\npublic enum {name} {
{pairs}}
"""
common_pairs = "    [ProtoMember({value})] public {type} {name} { get; set; }\n"
common_text = """[ProtoContract]\npublic class {name} {
{pairs}}
"""

def gen_enum(name, properties) -> str:
    pairs = ""
    for it in properties:
        pairs += enum_pairs.replace("{k}", it[0]).replace("{v}", it[1])
    return enum_text.replace("{name}", name).replace("{pairs}", pairs)

def analyze_enum() -> str:
    m = re.findall(enum_ptn, original_str)
    txt = ""
    for it in m:
        m = re.search(enum_name_ptn, it)
        if m:
            name = m.group("name")
            properties = re.findall(enum_properties_ptn, it)
            txt += gen_enum(name, properties)
    return txt

def gen_common(name: str, properties: list) -> str:
    pairs = ""
    for ppt in properties:
        pairs += common_pairs.replace("{value}", ppt["value"]).replace(
            "{type}", ppt["type"]).replace("{name}", ppt["name"])
    return common_text.replace("{name}", name).replace("{pairs}", pairs)

def analyze_common(common_ptn: str) -> str:
    m = re.findall(common_ptn, original_str)
    txt = ""
    for one_class in m:
        m_name = re.search(common_name_ptn, one_class)
        if m_name:
            name = m_name.group("name")
            finded_all = re.findall(common_properties_ptn, one_class)
            ppts = []
            for ppt in finded_all:
                field_name = ppt[0]
                value = ppt[1]
                type_ = ppt[3]
                name_ = ppt[4].removesuffix("_")

                m_repeated = re.search(
                    r"RepeatedField<(?P<t_name>\w+)>", type_)
                if m_repeated:
                    type_ = f"List<{m_repeated.group('t_name')}>"
                ppts.append({"field_name": field_name,
                            "value": value, "type": type_, "name": name_})
            txt += gen_common(name, ppts)
    return txt

def analyze_trans():
    feature = "Solis.Common.Proto.Transaction\n"

if __name__ == "__main__":
    original_str = Path(cs_file).read_text(encoding="utf-8")
    enm_txt = analyze_enum()
    Path(out_file_enum).write_text(enm_txt, encoding="utf-8")
    master_txt = analyze_common(master_ptn)
    Path(out_file_master).write_text(master_txt, encoding="utf-8")
    api_txt = analyze_common(api_ptn)
    Path(out_file_api).write_text(api_txt, encoding="utf-8")
    transaction_txt = analyze_common(transaction_ptn)
    Path(out_file_transaction).write_text(transaction_txt, encoding="utf-8")
    # api_txt = analyze_api()
    # Path(out_file_api).write_text(api_txt, encoding="utf-8")
