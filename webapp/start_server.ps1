# Start processes
Start-Process "cmd.exe" -ArgumentList "/c ng serve" -NoNewWindow
Start-Process "cmd.exe" -ArgumentList "/c python ../db/backend_python.py" -NoNewWindow

# Wait for a key to be pressed before exiting out of all the above commands
Write-Host "Press any key to continue..."
[void][System.Console]::ReadKey($true)

# Terminate processes

# Terminate all python.exe processes
Get-Process python | Stop-Process -Force
