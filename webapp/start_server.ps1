# Start processes
Start-Process "cmd.exe" -ArgumentList "/c ng serve" -NoNewWindow
Start-Process "cmd.exe" -ArgumentList "/c python ../db/login.py" -NoNewWindow
Start-Process "cmd.exe" -ArgumentList "/c python ../db/register.py" -NoNewWindow
Start-Process "cmd.exe" -ArgumentList "/c python ../db/search.py" -NoNewWindow

# Wait for a key to be pressed before exiting out of all the above commands
Write-Host "Press any key to continue..."
[void][System.Console]::ReadKey($true)

# Terminate processes
# Terminate ng serve process listening on port 4200
$ngServePid = Get-NetTCPConnection -LocalPort 4200 -State Listen | Select-Object -ExpandProperty OwningProcess
if ($ngServePid) {
    Stop-Process -Id $ngServePid -Force
}

# Terminate all python.exe processes
Get-Process python | Stop-Process -Force
