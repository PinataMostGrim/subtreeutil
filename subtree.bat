@echo off
REM: Run subtree_cli.py using the virtual environment '.venv'
"%~dp0.venv\Scripts\python.exe" "%~dp0subtree_cli.py" %*
