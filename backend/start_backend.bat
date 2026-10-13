@echo off
echo Starting BloodID Backend on 0.0.0.0 (LAN Accessible)...
echo Make sure your phone is on the same Wi-Fi network as this computer.
echo.
call venv\Scripts\activate.bat
python -m uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
pause
