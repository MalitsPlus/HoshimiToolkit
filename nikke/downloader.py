import re
import json
import requests
import threading
import lobby_pb2 as proto
import rich_console as console
from pathlib import Path
from request_base import send_request
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED

class NikkeDownloader:
  CONFIG_URL = "https://cloud.nikke-kr.com/route/route_config.json"
  HostDatapackLoadURL = "{_res_host}/datapacks/{_datapacks_ver}/datapack"
  HostCoreLoadURL = "{_res_host}/core/{_core_ver}"
  HostSoundLoadURL = "{_res_host}/datapacks/{_datapacks_ver}/sound_{_region}"
  RuntimePath = ""  # FIXME

  _lobby_url: str             # supposed to be "https://global-lobby.nikke-kr.com/"
  _version: str               # something likes "101.6.39"
  _res_ver: str               # something likes "r113"
  _res_host: str              # supposed to be "https://cloud.nikke-kr.com/prdenv/Android"
  _core_ver: str              # something likes "101.6.39F"
  _datapacks_ver: str         # something likes "21dea1d"

  _region: str
  _lock = threading.Lock()
  url_map: dict[str, str]

  def __init__(self, region: str):
    self._region = region

  def _get(self, url: str) -> requests.Response:
    return send_request(requests.get, url, retries=3)

  def _post(self, url: str, data: bytes | str, headers = None) -> requests.Response:
    if not headers:
      headers = {
        "Content-Type": "application/octet-stream+protobuf",
        "Accept": "application/octet-stream+protobuf",
      }
    return send_request(requests.post, url, data=data, headers=headers, retries=3)


  def _get_route_config(self):
    console.info(f"Getting {self.CONFIG_URL}...")
    config: dict = json.loads(self._get(self.CONFIG_URL).text)
    for cfg in config["Config"]:
      for route in cfg["Route"]:
        if route["Name"] == "pub:live-global":
          self._lobby_url = route["Url"]
          self._version = cfg["VersionRange"]["From"]
          return

  def _check_version(self):
    req_proto = proto.CheckVersionRequest()
    req_proto.version = "101.6.39"  # FIXME
    console.info("Posting checkversion...")
    res_raw = self._post(
        self._lobby_url + "v1/system/checkversion", 
        req_proto.SerializeToString()
      ).content
    # FIXME
    res_proto = proto.CheckVersionResponse().ParseFromString(res_raw)

  def _get_res_host(self):
    req_proto = proto.ResourceHostRequest()
    req_proto.rversion = "r113" # FIXME
    console.info("Posting resourcehost2...")
    res_raw = self._post(
        self._lobby_url + "v1/resourcehosts2",
        req_proto.SerializeToString()
    ).content
    res_proto = proto.ResourceHostResponse.FromString(res_raw)
    self._res_ver = res_proto.rversion  # FIXME
    self._res_host = res_proto.endpoint.replace("{Platform}", "Android")

  def _get_versions(self):
    console.info("Getting core_version...")
    self._core_ver = self._get(f"{self._res_host}/core/latest-{self._version}.txt").text
    console.info("Getting datapacks_version...")
    self._datapacks_ver = self._get(f"{self._res_host}/datapacks/latest-{self._res_ver}.txt").text

  def _replace_url(self):
    self.HostDatapackLoadURL = self.HostDatapackLoadURL\
      .replace("{_res_host}", self._res_host).replace("{_datapacks_ver}", self._datapacks_ver)
    self.HostCoreLoadURL = self.HostCoreLoadURL\
      .replace("{_res_host}", self._res_host).replace("{_core_ver}", self._core_ver)
    self.HostSoundLoadURL = self.HostSoundLoadURL\
      .replace("{_res_host}", self._res_host).replace("{_datapacks_ver}", self._datapacks_ver).replace("{_region}", self._region)
    self.url_map = {
      "{NK.Addressable.HostConst.HostCoreLoadURL}": self.HostCoreLoadURL,
      "{NK.Addressable.HostConst.HostDatapackLoadURL}": self.HostDatapackLoadURL,
      "{NK.Addressable.HostConst.HostSoundLoadURL}": self.HostSoundLoadURL,
      "{UnityEngine.AddressableAssets.Addressables.RuntimePath}": self.RuntimePath,
    }

  def _download_all(self):
    Path("cache").mkdir(exist_ok=True)

    # download core
    catalog_core: dict = json.loads(
      self._get(self.HostCoreLoadURL + "/catalog_core.json").text)
    self._download_addressables(catalog_core)

    # download main datapack
    catalog_main = json.loads(
      self._get(self.HostDatapackLoadURL + "/catalog_main.json").text)
    self._download_addressables(catalog_main)

    # download hd datapack
    datapack_jsons = self._get(self.HostDatapackLoadURL + "/catalogs.txt").text.splitlines(False)
    hd_path = filter(lambda x: x.endswith("hd.json"), datapack_jsons).__next__()
    catalog_hd = json.loads(
      self._get(self.HostDatapackLoadURL + "/" + hd_path).text)
    self._download_addressables(catalog_hd)

    # download sound packs
    sound_jsons = self._get(self.HostSoundLoadURL + "/catalogs.txt").text.splitlines(False)
    for it in sound_jsons:
      catalog_sound = json.loads(
        self._get(self.HostDatapackLoadURL + "/" + it).text)
      self._download_addressables(catalog_sound)

  def _download_action(self, endpoint: str):
    try:
      content = self._get(endpoint).content
      with open(f"cache/{endpoint.rsplit('/', 1)[-1]}", "wb") as fp:
        fp.write(content)
    except Exception as err:
      console.error(f"Failed to get or write file '{endpoint}'.")
      console.error(err)
      return
    console.succeed(f"Got '{endpoint}'.")

  def _download_addressables(self, addressables: dict):
    # For single thread testing

    # for endpoint in self._addressable_endpoints(addressables):
    #   self._download_action(endpoint)

    executor = ThreadPoolExecutor(max_workers=20)
    asset_tasks = [
      executor.submit(self._download_action, it) 
      for it in self._addressable_endpoints(addressables)
    ]
    wait(asset_tasks, return_when=ALL_COMPLETED)

  def _addressable_endpoints(self, addressables: dict):
    for it in addressables["m_InternalIds"]:
      m = re.match(r"\{(?!UnityEngine)[\w\.]+\}", it)
      if m:
        yield it.replace(m.group(0), self.url_map[m.group(0)])

  def follow_senarios(self):
    self._get_route_config()
    self._check_version()
    self._get_res_host()
    self._get_versions()
    self._replace_url()
    self._download_all()
