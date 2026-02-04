#!/usr/bin/env python3
"""
Script para descargar FFmpeg automáticamente en Windows
"""

import os
import sys
import zipfile
import shutil
import urllib.request
from pathlib import Path

# URL de FFmpeg (build estable de BtbN)
FFMPEG_URL = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip"
FFMPEG_FILENAME = "ffmpeg-master-latest-win64-gpl.zip"

def download_progress(count, block_size, total_size):
    """Muestra el progreso de descarga"""
    percent = int(count * block_size * 100 / total_size)
    percent = min(percent, 100)
    bar_length = 50
    filled_length = int(bar_length * percent // 100)
    bar = '█' * filled_length + '░' * (bar_length - filled_length)
    print(f'\rDescargando: |{bar}| {percent}%', end='', flush=True)

def download_ffmpeg():
    """Descarga FFmpeg desde GitHub"""
    print("=" * 50)
    print("  Descargador de FFmpeg para Whisper Transcriptor")
    print("=" * 50)
    print()
    
    if sys.platform != "win32":
        print("Este script está diseñado para Windows.")
        print("En Linux/Mac, instala FFmpeg con tu gestor de paquetes:")
        print("  - Ubuntu/Debian: sudo apt install ffmpeg")
        print("  - Mac: brew install ffmpeg")
        return
    
    ffmpeg_dir = Path("ffmpeg")
    ffmpeg_exe = ffmpeg_dir / "ffmpeg.exe"
    
    # Verificar si ya existe
    if ffmpeg_exe.exists():
        print(f"✅ FFmpeg ya está instalado en: {ffmpeg_dir.absolute()}")
        response = input("\n¿Deseas reinstalar? (s/n): ").lower().strip()
        if response != 's':
            print("Cancelado.")
            return
    
    # Crear carpeta si no existe
    ffmpeg_dir.mkdir(exist_ok=True)
    
    # Descargar
    print(f"\nDescargando FFmpeg desde GitHub...")
    print(f"URL: {FFMPEG_URL}")
    print()
    
    try:
        urllib.request.urlretrieve(FFMPEG_URL, FFMPEG_FILENAME, download_progress)
        print("\n✅ Descarga completada!")
    except Exception as e:
        print(f"\n❌ Error al descargar: {e}")
        print("\nDescarga manualmente desde:")
        print(f"  {FFMPEG_URL}")
        return
    
    # Extraer
    print("\nExtrayendo archivos...")
    try:
        with zipfile.ZipFile(FFMPEG_FILENAME, 'r') as zip_ref:
            # Encontrar la carpeta bin dentro del ZIP
            for member in zip_ref.namelist():
                if '/bin/' in member and member.endswith('.exe'):
                    # Extraer solo el nombre del archivo
                    filename = Path(member).name
                    print(f"  Extrayendo: {filename}")
                    
                    # Leer el archivo del ZIP
                    with zip_ref.open(member) as source:
                        target_path = ffmpeg_dir / filename
                        with open(target_path, 'wb') as target:
                            target.write(source.read())
        
        print("✅ Extracción completada!")
        
    except Exception as e:
        print(f"❌ Error al extraer: {e}")
        return
    
    # Limpiar archivo ZIP
    print("\nLimpiando archivos temporales...")
    try:
        os.remove(FFMPEG_FILENAME)
    except:
        pass
    
    # Verificar instalación
    print("\nVerificando instalación...")
    files_found = list(ffmpeg_dir.glob("*.exe"))
    
    if files_found:
        print("\n✅ FFmpeg instalado correctamente!")
        print(f"\nArchivos en {ffmpeg_dir.absolute()}:")
        for f in files_found:
            size_mb = f.stat().st_size / (1024 * 1024)
            print(f"  - {f.name} ({size_mb:.1f} MB)")
    else:
        print("❌ No se encontraron archivos ejecutables")
    
    print("\n" + "=" * 50)
    print("  ¡Listo! Ya puedes usar Whisper Transcriptor")
    print("=" * 50)

if __name__ == "__main__":
    download_ffmpeg()
    input("\nPresiona Enter para salir...")
