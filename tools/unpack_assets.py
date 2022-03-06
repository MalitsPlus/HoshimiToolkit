import UnityPy
import re
import sys
from pathlib import Path
sys.path.append("../")
import tools.rich_console as console

def unpack_with_map(src: str, map: dict, clean: bool=False):
    if clean:
        move_to_warehouse(map)
    map.pop("warehouse")

    src_path = Path(src)
    else_path = Path(map.pop("else"))
    console.info("Extracting assets-Texture2D to png...")
    for path in src_path.glob("**/*"):
        env = UnityPy.load(str(path))
        for obj in env.objects:
            if obj.type.name in ["Texture2D"]:
                data = obj.read()
                m = re.search("|".join(map.keys()), str(data.name))
                if m:
                    dest_path = Path(map[m.group(0)], data.name).with_suffix(".png")
                else:
                    dest_path = Path(else_path, data.name).with_suffix(".png")
                dest_path.parent.mkdir(exist_ok=True)
                img = data.image
                img.save(dest_path)

def unpack_image(src: str, dest: str, features: list=[], warehouse: str=""):
    if not warehouse == "":
        move_to_warehouse(dest, warehouse)
    src_path = Path(src)
    console.info("Extracting assets-Texture2D to png...")
    for path in src_path.glob("**/*"):
        env = UnityPy.load(str(path))
        for obj in env.objects:
            if obj.type.name in ["Texture2D"]:
                data = obj.read()
                if features.__len__() > 0 and not re.search("|".join(features), str(data.name)):
                    continue
                dest_path = Path(dest, data.name).with_suffix(".png")
                dest_path.parent.mkdir(exist_ok=True)
                img = data.image
                img.save(dest_path)

def move_to_warehouse(map: dict):
    console.info("Moving previous files to warehouse...")
    warehouse = map["warehouse"]
    for k, v in map.items():
        if k != "warehouse":
            for file in Path(v).glob("**/*"):
                file.replace(Path(warehouse, file.name))

if __name__ == "__main__":
    src = r"D:\GitHub\HoshimiToolkit\ipr\assets\UnobfuscateAssets\1710\img"
    dest = r"D:\GitHub\HoshimiToolkit\ipr\assets\UnobfuscateAssets\test"
    unpack_image(src, dest)
