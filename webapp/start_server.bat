@echo off
start "" "cmd /k ng serve"
start "" "cmd /k python ../db/login.py"
start "" "cmd /k python ../db/register.py"
start "" "cmd /k python ../db/search.py"
pause