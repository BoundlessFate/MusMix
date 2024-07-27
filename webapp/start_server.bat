@echo off

REM start processes
start /B ng serve
start /B python ../db/login.py
start /B python ../db/register.py
start /B python ../db/search.py
start /B python ../db/setProfileData.py
start /B python ../db/getProfileData.py

REM wait for a key to be pressed before exiting out of all the above commands
pause

REM terminate processes
FOR /F "tokens=5 delims= " %%P IN ('netstat -ano ^| find "LISTENING" ^| find ":4200 "') DO (TASKKILL /F /PID %%P)
taskkill /IM "python.exe" /F