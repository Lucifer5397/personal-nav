import os
import subprocess

desktop = r"I:\Desktop"
icon = r"E:\works\web-app\favicon.ico"

# PowerShell script to create proper .lnk
ps_script = f'''
$ws = New-Object -ComObject WScript.Shell
$s = $ws.CreateShortcut("{desktop}\\个人导航中心.lnk")
$s.TargetPath = "http://localhost:5000"
$s.IconLocation = "{icon}"
$s.Save()
Write-Output "Done"
'''
result = subprocess.run(
    ['powershell', '-NoProfile', '-Command', ps_script],
    capture_output=True, text=True
)
print("stdout:", result.stdout)
print("stderr:", result.stderr)
print("rc:", result.returncode)

# Verify
lnk = os.path.join(desktop, "个人导航中心.lnk")
print("LNK exists:", os.path.exists(lnk))
