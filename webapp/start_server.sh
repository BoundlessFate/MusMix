#!/bin/bash

# Start processes in the background
ng serve &
NG_PID=$!

python3 ../db/backend_python.py &
PYTHON_PID=$!

# Wait for a key to be pressed before exiting
read -p "Press any key to terminate processes..." -n1 -s

# Terminate processes
kill $NG_PID
kill $PYTHON_PID