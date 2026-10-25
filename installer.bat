@echo off
setlocal
cd /d "%~dp0"
where py >nul 2>nul
if errorlevel 1 (
  echo Python 3 est introuvable. Installez Python 3.10 ou 3.11 et cochez Add Python to PATH.
  pause
  exit /b 1
)
py -3.11 -m venv .venv 2>nul
if errorlevel 1 py -3.10 -m venv .venv
if errorlevel 1 (
  echo Impossible de creer l'environnement Python.
  pause
  exit /b 1
)
call ".venv\Scripts\activate.bat"
python -m pip install --upgrade pip
if errorlevel 1 goto erreur
python -m pip install -r requirements.txt
if errorlevel 1 goto erreur
echo Installation terminee. Vous pouvez lancer demarrer.bat.
pause
exit /b 0
:erreur
echo L'installation a echoue. Verifiez votre connexion et les versions Python supportees.
pause
exit /b 1
