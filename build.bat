rmdir /s /q dist
pyinstaller --hidden-import pystray._win32 --hidden-import pynput.keyboard._win32 --onefile --noconsole symbol-finder.py --icon icon.ico
rmdir /s /q __pycache__
rmdir /s /q build
del symbol-finder.spec
copy /y symbols.csv dist\symbols.csv
copy /y icon.ico dist\icon.ico
