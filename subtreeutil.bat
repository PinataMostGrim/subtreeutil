@echo off
:: Run subtree module using its virtual environment interpreter.

setlocal
:: In order to support executing this batch from from any location,
:: module's parent folder must be added to the Python path.
set PYTHONPATH=%~dp0
"%~dp0.venv\Scripts\python.exe" -m subtreeutil %*
endlocal
