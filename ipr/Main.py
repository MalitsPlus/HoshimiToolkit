from ManifestDecryptor import doDecrypt
from MaskedHeaderStream import unObfuscate, rename
from AssetsDownloader import downloadAll
from eDiffMode import DiffMode
from eWorkingMode import WorkingMode

# Configurations
# Diff, All
diffMode = DiffMode.Diff
# Local, Remote
workingMode = WorkingMode.Local
# Adjust this param according to your PC's spec
maxDownloadThread = 20

jDict = doDecrypt(diffMode)
if workingMode != WorkingMode.Local:
    downloadAll(jDict, maxDownloadThread)
unObfuscate(jDict["assetBundleList"])
rename(jDict["resourceList"])