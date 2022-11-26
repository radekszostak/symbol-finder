rmdir /s /q dist
pyinstaller --hidden-import 'pystray._win32' --onefile --noconsole symbol-finder.py
rmdir /s /q __pycache__
rmdir /s /q build
del symbol-finder.spec
copy /y symbols.csv dist\symbols.csv
