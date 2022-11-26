from pystray._base import MenuItem as item
import pystray._win32

import PySimpleGUI as sg
import csv
import pyperclip
import psgtray
from pynput import keyboard
import threading

min_ratio = 50
def global_hotkey(window):
    def on_global_hotkey_pressed():
        window.write_event_value('-GLOBAL-HOTKEY-', 'UnHide')
    with keyboard.GlobalHotKeys({
        '<ctrl>+<alt>+/': on_global_hotkey_pressed}) as h:
        h.join()

with open('symbols.csv', 'r', encoding="utf-8") as f:
    reader = csv.reader(f)
    data = list(reader)

layout = [[sg.Input(key='-INPUT-', size=(600, 200))], [sg.Table(values=data, size=(600, 200), headings=["Symbol","Description"],  key='-TABLE-', justification='left', auto_size_columns=False, col_widths=[15, 55])]]

window = sg.Window('Symbol search', layout, size=(600, 200), no_titlebar=True, grab_anywhere=True, keep_on_top=True, finalize=True)

tray = psgtray.SystemTray(["",["Open", "Exit"]], single_click_events=False, window=window, tooltip="Symbol search", icon="icon.ico")
window['-TABLE-'].Update(select_rows=[0])
window["-INPUT-"].bind("<KeyRelease>", "KEY-RELEASE-")
window.bind("<Return>", "-Enter-")
window.bind("<Escape>", "-Escape-")
window.bind("<Down>", "-Down-")
window.bind("<Up>", "-Up-")

search_str = ""
threading.Thread(target=global_hotkey, args=(window,), daemon=True).start()
while True:
    event, values = window.read()
    print(event, values)
    if event == sg.WIN_CLOSED or event == '-Escape-':
        window['-INPUT-'].update("")
        window.write_event_value('-INPUT-KEY-RELEASE-', "")
        window.Hide()
    elif event == '-Down-' and window['-TABLE-'].SelectedRows[0] < len(window['-TABLE-'].Values)-1:
        window['-TABLE-'].Update(select_rows=[window['-TABLE-'].SelectedRows[0]+1])
        window['-TABLE-'].Widget.see(window['-TABLE-'].SelectedRows[0]+2)
    elif event == '-Up-' and window['-TABLE-'].SelectedRows[0] > 0:
        window['-TABLE-'].Update(select_rows=[window['-TABLE-'].SelectedRows[0]-1])
        window['-TABLE-'].Widget.see(window['-TABLE-'].SelectedRows[0])
    elif event == '-Enter-':
        symbol = window['-TABLE-'].Values[window['-TABLE-'].SelectedRows[0]][0]
        pyperclip.copy(symbol)
        window.Hide()
    elif event == '-INPUT-KEY-RELEASE-':
        if values['-INPUT-'] == search_str:
            continue
        rows = []
        for row in data:
            words = values['-INPUT-'].split()
            if all(word.lower() in row[1].lower() for word in words):
                rows.append(row)
        window['-TABLE-'].update(values=rows)
        if len(rows) > 0:
            window['-TABLE-'].update(select_rows=[0])
        search_str = values['-INPUT-']
    elif event == "-TRAY-":
        if values["-TRAY-"] == "Exit":
            break
        elif values["-TRAY-"] == "Open" or values["-TRAY-"] == "__DOUBLE_CLICKED__":
            window.UnHide()
            window.BringToFront()
            window.TKroot.focus_force()
            window["-INPUT-"].SetFocus()
    elif event == "-GLOBAL-HOTKEY-":
        window.UnHide()
        window.BringToFront()
        window.TKroot.focus_force()
        window["-INPUT-"].SetFocus()
    elif event == "Exit":
        break

window.close()