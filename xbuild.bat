rmdir /s /f dist
pyinstaller.exe --onefile --icon=icon.ico ./main.py --name=Zalo
xcopy "chrome" "dist/chrome/"
xcopy "config.json" "dist"