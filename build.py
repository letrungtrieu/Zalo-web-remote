from main import __version__
import subprocess

with open("dist/version.txt", "w") as f:
  f.write(__version__)
  
subprocess.run(f"pyinstaller --onefile --icon=icon.ico ./main.py --name=Zalo_{__version__}", shell=True)
