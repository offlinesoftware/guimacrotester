''''
LzTZopUnYTXPqdKIDKo6LA==
'''

import pyautogui as pag
from time import sleep

delay = 0.2
screenWidth, screenHeight = pag.size()

# Status bar
s_bar = {
    "home": [950, 100]
}

login = {
    "prod": [200, 350]
}

prod = {
    "advanced": [950, 680]
}

advanced = {
    "new_prog": [600, 300],
    "del_prog": [420, 320]
}

new_prog = {
    "name": [200, 200],
    "next": [750, 680],
    "add_min": [425, 600],
    "edit": [650, 600],
    "min": [145, 230],
    "low": [380, 320],
    "targ": [560, 230],
    "high": [750, 300],
    "max": [970, 230],
    "tick": [860, 670],
    "page": [970, 590],
    "unwd": [720, 290]
}

del_prog = {
    "select": [490, 180]
}

numpad = {
    "dot": [600, 520],
    "tick": [750, 600]
}

pw_pad = {
    "entry": [600, 230],
    "tick": [700, 650]
}

keyboard = {
    "tick": [850, 680],
    "clear": [950, 120]
}

yes_no = {
    "tick": [620, 560]
}

def push(pos):
    pag.moveTo(pos)
    pag.click()
    sleep(delay)
    # print(pos)

def new_val(val, pos):
    push(pos)
    pag.press(['del', 'del', 'del', 'del'])
    pag.write(str(val), interval=delay)
    push(numpad["dot"])
    push(numpad["tick"])

def load_advanced():
    push(s_bar["home"])
    push(login["prod"])
    push(prod["advanced"])
    push(pw_pad["entry"])
    pag.write('3')
    push(pw_pad["tick"])

def new_program(name, mn=200, lo=300, targ=400, hi=500, mx=600):
    load_advanced()
    push(advanced["new_prog"])
    push(new_prog["name"])
    pag.write(name, interval=delay)
    push(keyboard["tick"])
    push(new_prog["next"])
    push(new_prog["add_min"])
    push(new_prog["edit"])
    new_val(mn, new_prog["min"])
    new_val(lo, new_prog["low"])
    new_val(targ, new_prog["targ"])
    new_val(hi, new_prog["high"])
    new_val(mx, new_prog["max"])
    push(new_prog["page"])
    push(new_prog["unwd"])
    push(new_prog["unwd"])
    push(new_prog["tick"])
    push(new_prog["next"])
    push(new_prog["tick"])
    push(new_prog["next"])
    push(new_prog["next"])
    push(new_prog["tick"])

def delete_program(name):
    load_advanced()
    push(advanced["del_prog"])
    push(del_prog["select"])
    push(keyboard["clear"])
    pag.write(name, interval=delay)
    push(keyboard["tick"])
    push(new_prog["tick"])
    push(yes_no["tick"])

pag.moveTo(screenWidth / 2, 20)

if __name__ == "__main__":

    assert (screenWidth, screenHeight) == (1600, 900), "Wrong screen resolution"

    new_program("TW1")
    delete_program("TW1")


