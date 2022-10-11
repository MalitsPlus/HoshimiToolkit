from pathlib import Path
from octo_manager import update_octo, scale_with_esrgan

def main():
  enc_bytes = Path("cache/octocacheevai").read_bytes()
  update_octo(enc_bytes, True)
  scale_with_esrgan()

if __name__ == "__main__":
  main()
