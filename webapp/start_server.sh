#!/bin/bash

# Start processes in the background
ng serve &
NG_PID=$!

python3 ../db/backend_python.py &
PYTHON_PID=$!