import hashlib
import json
from rich.console import Console
from pathlib import Path

inputDirectory = "ipr/Assets/"
outputPath = "ipr/UnobfuscateAssets/"
console = Console()

def unObfuscate(assetList: list, offset: int = 0, streamPos: int = 0, headerLength: int = 256):
    """
    Args: 
        assetList (list): Assets list to unobfuscate
    """
    contents = Path(inputDirectory).iterdir()
    try:
        md5List = [it["md5"] for it in assetList]
        filePaths = [path for path in contents if path.name in md5List]
    except FileNotFoundError:
        console.print(f"[bold red]>>> [Error][/bold red] Folder '{inputDirectory}' is not exists. Unobfuscation has been discarted.")
        return

    filePaths.sort(key=lambda x: x.name)
    unitySignature = b"Unity"
    for path in filePaths:
        buff = path.read_bytes()
        if buff[0:5] == unitySignature:
            continue
        else:
            pass

def StringToMaskBytes() -> bytes:
    pass

def CryptByString() -> bytes:
    pass
