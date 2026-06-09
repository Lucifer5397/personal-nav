import os
desktop = r'I:\Desktop'
path = os.path.join(desktop, '个人导航中心.url')
with open(path, 'w') as f:
    f.write('[InternetShortcut]\r\n')
    f.write('URL=http://localhost:5000\r\n')
print('Created:', path)
print('Exists:', os.path.exists(path))
