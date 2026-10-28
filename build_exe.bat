@echo off
setlocal
cd /d "%~dp0"

echo ========================================
echo             AirSlide EXE Builder
echo ========================================
echo.

if not exist ".venv\Scripts\python.exe" (
    echo Creating virtual environment...
    py -3.11 -m venv .venv
    if errorlevel 1 goto error
)

echo Installing build dependencies...
".venv\Scripts\python.exe" -m pip install --upgrade pip
if errorlevel 1 goto error
".venv\Scripts\python.exe" -m pip install -r requirements-build.txt
if errorlevel 1 goto error

echo.
echo Building AirSlide.exe...
".venv\Scripts\python.exe" -m PyInstaller --noconfirm --clean --onefile --windowed --name AirSlide --collect-all mediapipe --collect-all cv2 --collect-all numpy --collect-all pyautogui airslide.py
if errorlevel 1 goto error

echo.
echo Build complete: dist\AirSlide.exe
echo Copy this EXE to a Windows PC with a webcam to test it.
pause
exit /b 0

:error
echo.
echo Build failed. Read the error above before retrying.
pause
exit /b 1
