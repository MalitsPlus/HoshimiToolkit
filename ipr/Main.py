from ManifestDecryptor import doDecrypt
from MaskedHeaderStream import unObfuscate

jDict = doDecrypt()
unObfuscate(jDict["assetBundleList"])
