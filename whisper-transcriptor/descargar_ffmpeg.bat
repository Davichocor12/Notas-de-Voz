@echo off
REM Script para descargar FFmpeg facilmente
REM Ejecuta este archivo para descargar FFmpeg automaticamente

echo.
echo ========================================
echo   Descargador de FFmpeg
echo ========================================
echo.

REM Verificar si Python esta disponible
python --version >nul 2>&1
if errorlevel 1 (
    echo Python no encontrado. Descargando FFmpeg manualmente...
    echo.
    echo Por favor descarga FFmpeg manualmente de:
    echo   https://github.com/BtbN/FFmpeg-Builds/releases
    echo.
    echo Busca: ffmpeg-master-latest-win64-gpl.zip
    echo.
    echo Extrae los archivos .exe de la carpeta bin/ 
    echo y copialos a la carpeta ffmpeg/ de este proyecto.
    echo.
    start https://github.com/BtbN/FFmpeg-Builds/releases
    pause
    exit /b 1
)

REM Ejecutar script de descarga
python download_ffmpeg.py

pause
