import sys
from pathlib import Path
from ManifestDecryptor import doDecrypt
from MaskedHeaderStream import unObfuscate, rename
from AssetsDownloader import downloadAll
from eDiffMode import DiffMode
from eWorkingMode import WorkingMode
sys.path.append("../..")
from tools.unpack_assets import unpack_with_map
from tools.image_converter import convert_to_size
from tools.image_converter import convert_resize

# Configurations
# Diff, All
diffMode = DiffMode.Diff
# Local, Remote
workingMode = WorkingMode.Remote
# Adjust this param according to your PC's spec
maxDownloadThread = 20

jDict = doDecrypt(diffMode)
if workingMode == WorkingMode.Remote:
    downloadAll(jDict, maxDownloadThread)
unObfuscate(jDict)
rename(jDict)

map = {
    "img_card_full_1": r"F:\CG\IDOLY PRIDE Extract\NewCardsRaw",
    "else": r"F:\CG\IDOLY PRIDE Extract\Miscell",
    "warehouse": r"F:\CG\IDOLY PRIDE Extract\Texture2D"
}
unpack_with_map(src=str(Path("UnobfuscateAssets", str(jDict["revision"]), "img").absolute()),
                map=map,
                clean=True)

input_path = r"F:\CG\IDOLY PRIDE Extract\NewCardsRaw"
convert_path = r"F:\CG\IDOLY PRIDE Extract\Cards"
convert_to_size(c_size=(2560, 1440), inputs=input_path, output=convert_path)
# convert_resize(c_size=(1821, 1024), inputs=input_path, output=convert_path, scale=str(1440/1024))
