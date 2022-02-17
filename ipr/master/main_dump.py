import subprocess
from pathlib import Path
from sqlcipher_gen import do_gen

do_gen()
path = Path("sqlcipher_dec.cmd").absolute()
args = ["powershell", path]
subprocess.Popen(args)
