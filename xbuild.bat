rmdir /s /f dist
pyinstaller.exe --onefile --icon=icon.ico ./main.py --name=Zalo 
xcopy "chrome" "dist/chrome/" /D
xcopy "bin" "dist/chrome/" /D
xcopy "config.json" "dist"