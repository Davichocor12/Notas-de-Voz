@echo off
chcp 65001 >nul
title Creando Ejecutable de Whisper Transcriptor

echo.
echo ============================================================
echo    CREADOR DE EJECUTABLE - WHISPER TRANSCRIPTOR
echo ============================================================
echo.
echo Este proceso puede tardar 10-20 minutos la primera vez.
echo NO cierres esta ventana hasta que termine.
echo.
pause

echo.
echo [1/3] Instalando dependencias...
echo       (Esto puede tardar varios minutos)
echo.
pip install openai-whisper pyinstaller torch
if errorlevel 1 (
    echo.
    echo ERROR: No se pudieron instalar las dependencias.
    echo Asegurate de tener Python instalado y en el PATH.
    echo.
    pause
    exit /b 1
)

echo.
echo [2/3] Creando ejecutable...
echo       (Esto tarda varios minutos, espera...)
echo.
pyinstaller --onedir --windowed --name=WhisperTranscriptor --collect-all=whisper --collect-all=tiktoken --hidden-import=tiktoken_ext.openai_public --hidden-import=numba --noconfirm transcriptor_simple.py
if errorlevel 1 (
    echo.
    echo ERROR: Fallo al crear el ejecutable.
    echo.
    pause
    exit /b 1
)

echo.
echo [3/3] Copiando FFmpeg...
if exist "ffmpeg\ffmpeg.exe" (
    xcopy /E /I /Y ffmpeg dist\WhisperTranscriptor\ffmpeg
    echo FFmpeg copiado correctamente.
) else (
    echo.
    echo AVISO: No encontre ffmpeg.exe en la carpeta ffmpeg\
    echo.
    echo Descarga FFmpeg de:
    echo   https://github.com/BtbN/FFmpeg-Builds/releases
    echo.
    echo Y copia ffmpeg.exe a: dist\WhisperTranscriptor\ffmpeg\
    echo.
    mkdir dist\WhisperTranscriptor\ffmpeg 2>nul
)

echo.
echo ============================================================
echo    ¡COMPLETADO!
echo ============================================================
echo.
echo Tu ejecutable esta en: dist\WhisperTranscriptor\
echo.
echo IMPORTANTE: 
echo - Si no copiaste FFmpeg, hazlo ahora manualmente
echo - Comprime esa carpeta en ZIP para enviarla
echo.
echo Abriendo la carpeta...
explorer dist\WhisperTranscriptor
echo.
pause
