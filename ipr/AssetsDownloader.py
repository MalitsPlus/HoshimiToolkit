from logging import error, exception
from rich.console import Console
from pathlib import Path
import requests
import wget

console = Console()
URL = "https://d2ilil7yh5oi1v.cloudfront.net/solis-{v}-{type}/{o}?generation={g}&alt=media"
downloadPath = "ipr/Assets/"

def downloadAll(jDict: dict): 
    assetBundleList: list = jDict["assetBundleList"]
    resourceList: list = jDict["resourceList"]
    console.print(f"[bold green]>>> [Succeed][/bold green] Start downloading assets, this may take some hours...\n")
    errCount = downloadFromList(assetBundleList, "assetbundle") + downloadFromList(resourceList, "resources")
    console.print(f"\n[bold white]>>> [Info][/bold white] Download operation has been done, {errCount} error(s) occurred during download.")

def downloadFromList(ablist: list, _type: str) -> int:
    path = Path(downloadPath)
    path.mkdir(parents=True, exist_ok=True)
    contents = path.glob("**/*")
    count = 0
    countAll = ablist.__len__()
    errCount = 0
    fileNames = [path.name for path in contents]
    for it in contents:
        pass
    for it in ablist:
        count += 1
        v = it["uploadVersionId"]
        o = it["objectName"]
        g = it["generation"]
        md5 = it["md5"]
        if md5 in fileNames:
            console.print(f"\n[bold yellow]>>> ({count}/{countAll}) [Warning][/bold yellow] '{md5}' is already exists.")
            continue
        url = URL.replace("{v}", str(v)).replace("{type}", _type).replace("{o}", o).replace("{g}", str(g))
        try:
            downloadAction(url, path.joinpath(md5))
            console.print(f"\n[bold green]>>> ({count}/{countAll}) [Succeed][/bold green] '{md5}' has been successfully download.")
        except:
            errCount += 1
            console.print(f"[bold red]>>> ({count}/{countAll}) [Error][/bold red] Failed to download '{md5}'.")
    return errCount

def downloadAction(url: str, filePath: Path):
    wget.download(url, out=str(filePath))
    # r = requests.get(url)
    # if r.status_code == 200:
    #     try: 
    #         filePath.write_bytes(r.content)
    #         console.print(f"[bold green]>>> [Succeed][/bold green] '{filePath.name}' has been successfully download.")
    #     except:
    #         console.print(f"[bold red]>>> [Error][/bold red] An error was occured when writing '{filePath.name}'.")
    # else: 
    #     console.print(f"[bold red]>>> [Error][/bold red] Failed to download '{filePath.name}'.")

def downloadDiff(jDict: dict):
    pass