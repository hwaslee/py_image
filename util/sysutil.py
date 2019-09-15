# copy text to clipboard


import subprocess
def copyToClip(txt):
    cmd='echo '+txt.strip()+'|clip'
    return subprocess.check_call(cmd, shell=True)


# -- Not working
import win32clipboard as cb
def copy(texts):
    cb.OpenClipboard()
    cb.EmptyClipboard()
    cb.SetClipboardData(cb.CF_TEXT, str(texts))
    cb.CloseClipboard()


import pyperclip
def copy2clip(texts):
    pyperclip.copy(texts)