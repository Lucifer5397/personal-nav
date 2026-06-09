import os, winreg
key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders')
desktop = winreg.QueryValueEx(key, 'Desktop')[0]
desktop = os.path.expandvars(desktop)
print('Desktop:', desktop)
print('Exists:', os.path.exists(desktop))
if os.path.exists(desktop):
    for f in os.listdir(desktop)[:15]:
        print(' ', f)
