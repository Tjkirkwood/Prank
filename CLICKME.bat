@echo off
REM 1) Install dependencies into the system Python
pip install pyttsx3 pygame opencv-python --upgrade --quiet

REM 2) Launch the prank EXE
start "" "%~dp0DoNotRUN.exe"

REM 3) Optional: close this window after starting
exit
