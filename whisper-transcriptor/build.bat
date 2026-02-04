@echo off
REM ============================================
REM Script de construcción para Whisper Transcriptor
REM Para Windows
REM ============================================

echo.
echo ========================================
echo   Whisper Transcriptor - Build Script
echo ========================================
echo.

REM Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python no esta instalado o no esta en el PATH
    echo Por favor instala Python 3.8+ desde https://python.org
    pause
    exit /b 1
)

echo [1/5] Creando entorno virtual...
if not exist "venv" (
    python -m venv venv
)

echo [2/5] Activando entorno virtual...
call venv\Scripts\activate.bat

echo [3/5] Instalando dependencias...
pip install --upgrade pip
pip install -r requirements.txt

echo [4/5] Verificando FFmpeg...
if not exist "ffmpeg\ffmpeg.exe" (
    echo.
    echo [AVISO] FFmpeg no encontrado en la carpeta 'ffmpeg'
    echo.
    echo Por favor descarga FFmpeg de:
    echo   https://github.com/BtbN/FFmpeg-Builds/releases
    echo.
    echo Descarga: ffmpeg-master-latest-win64-gpl.zip
    echo Extrae el contenido y copia los archivos .exe a la carpeta 'ffmpeg'
    echo ^(ffmpeg.exe, ffprobe.exe, ffplay.exe^)
    echo.
    pause
)

echo [5/5] Construyendo ejecutable con PyInstaller...
python build_exe.py

echo.
echo ========================================
echo   Construccion completada!
echo ========================================
echo.
echo El ejecutable esta en: dist\WhisperTranscriptor\
echo.
echo IMPORTANTE: Copia la carpeta 'ffmpeg' dentro de 'dist\WhisperTranscriptor\'
echo antes de distribuir la aplicacion.
echo.
pause
