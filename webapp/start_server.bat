@echo off

REM start processes
start /B ng serve
start /B python ../db/backend_python.py

REM wait for a key to be pressed before exiting out of all the above commands
pause

REM terminate processes
taskkill /IM "python.exe" /F