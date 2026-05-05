@echo off
cd /d %~dp0

set VENV_PY=..\.venv\Scripts\python.exe

if exist "%VENV_PY%" (
    set PYTHON=%VENV_PY%
    echo [INFO] Using venv Python
) else (
    set PYTHON=python
    echo [INFO] Using system Python
)

%PYTHON% -m PyInstaller --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] PyInstaller not found
    %PYTHON% -m pip install pyinstaller
)

%PYTHON% -m PyInstaller MeowTool.spec

pause