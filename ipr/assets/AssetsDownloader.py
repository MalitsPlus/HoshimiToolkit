from logging import error, exception
from shutil import Error
from typing import Dict
from rich.console import Console
from pathlib import Path
import urllib.request
import requests
import time
from concurrent.futures import ThreadPoolExecutor, thread, wait, ALL_COMPLETED
import threading
# import wget

console = Console()
URL = "https://d2ilil7yh5oi1v.cloudfront.net/solis-{v}-{type}/{o}?generation={g}&alt=media"
downloadPath = "Assets/"
path = Path(downloadPath)
path.mkdir(parents=True, exist_ok=True)
contents = path.glob("**/*")
fileNames = [path.name for path in contents]
count = 0
errCount = 0
countAll = 0
lock = threading.Lock()

def downloadAll(jDict: dict, maxThread: int): 
    assetBundleList: list = jDict["assetBundleList"]
    resourceList: list = jDict["resourceList"]
    global countAll
    countAll = assetBundleList.__len__() + resourceList.__len__()
    console.print(f"[bold green]>>> [Succeed][/bold green] Start downloading assets, this may take some hours...\n")
    executor = ThreadPoolExecutor(max_workers=maxThread)
    allTasks = [executor.submit(downloadOne, it, "assetbundle") for it in assetBundleList]
    allTasks.extend([executor.submit(downloadOne, it, "resources") for it in resourceList])
    wait(allTasks, return_when=ALL_COMPLETED)
    console.print(f"\n[bold white]>>> [Info][/bold white] Download operation has been done, {errCount} error(s) occurred during download.")

def downloadOne(it: Dict, _type: str):
    global count
    global errCount
    v = it["uploadVersionId"]
    o = it["objectName"]
    g = it["generation"]
    md5 = it["md5"]
    if md5 in fileNames:
        lock.acquire()
        count = count + 1
        console.print(f"\n[bold yellow]>>> ({count}/{countAll}) [Warning][/bold yellow] '{md5}' is already exists.")
        lock.release()
        return
    url = URL.replace("{v}", str(v)).replace("{type}", _type).replace("{o}", o).replace("{g}", str(g))
    try:
        downloadAction(url, path.joinpath(md5))
        lock.acquire()
        count = count + 1
        console.print(f"\n[bold green]>>> ({count}/{countAll}) [Succeed][/bold green] '{md5}' has been successfully download.")
        lock.release()
    except:
        lock.acquire()
        count = count + 1
        errCount += 1
        console.print(f"[bold red]>>> ({count}/{countAll}) [Error][/bold red] Failed to download '{md5}'.")
        lock.release()

def downloadAction(url: str, filePath: Path):
    try:
        r = requests.get(url, timeout=30)
        if r.status_code == 200:
            filePath.write_bytes(r.content)
        else: 
            raise Error()
    except:
        time.sleep(5)
        downloadAction(url, filePath)

    # urllib.request.urlretrieve(url, filename=filePath)
    # wget.download(url, out=str(filePath), bar=None)

def downloadDiff(jDict: dict):
    pass
