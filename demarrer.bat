@echo off
setlocal
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
  echo Environnement Python manquant. Lancez d'abord installer.bat.
  pause
  exit /b 1
)
call ".venv\Scripts\activate.bat"
python -m streamlit run dashboard.py --server.address 127.0.0.1
