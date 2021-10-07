from ManifestDecryptor import doDecrypt
from MaskedHeaderStream import unObfuscate
from MaskedHeaderStream import rename
from AssetsDownloader import downloadAll
from eDiffMode import DiffMode
from eWorkingMode import WorkingMode

# configuration
diffMode = DiffMode.Diff
workingMode = WorkingMode.Local

jDict = doDecrypt(diffMode)
if workingMode != WorkingMode.Local:
    downloadAll(jDict)
unObfuscate(jDict["assetBundleList"])
rename(jDict["resourceList"])