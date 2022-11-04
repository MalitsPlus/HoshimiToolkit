from downloader import NikkeDownloader

en = jp = kr = str
# choose your region
# this will affect which voice pack should be downloaded
_REGION: en | jp | kr = "en"

def main():
  downloader = NikkeDownloader(_REGION)
  downloader.follow_senarios()

if __name__ == "__main__":
  main()
