@echo off
echo ========================================
echo    Weebhook Python Setup Script
echo ========================================
echo.

echo Installing Python dependencies...
pip install -r requirements.txt

echo.
echo ========================================
echo    Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Copy env.example to .env
echo 2. Edit .env with your verify token
echo 3. Run: python server.py
echo.
echo For Meta configuration:
echo - Callback URL: http://localhost:3000/webhook
echo - Verify Token: (use the one from your .env file)
echo.
echo Use ngrok to expose your local server:
echo - Install: pip install pyngrok
echo - Or download from: https://ngrok.com/download
echo - Run: ngrok http 3000
echo.
pause 