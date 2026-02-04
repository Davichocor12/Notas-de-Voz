#!/usr/bin/env python3
"""
Script de construcción para crear el ejecutable de Whisper Transcriptor
Usa PyInstaller para empaquetar la aplicación
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

def find_whisper_assets():
    """Encuentra los assets de Whisper necesarios para el ejecutable"""
    import whisper
    whisper_path = Path(whisper.__file__).parent
    assets_path = whisper_path / "assets"
    
    return str(whisper_path), str(assets_path)

def find_torch_libs():
    """Encuentra las librerías de PyTorch"""
    import torch
    torch_path = Path(torch.__file__).parent
    return str(torch_path)

def build_executable():
    """Construye el ejecutable usando PyInstaller"""
    
    print("\n=== Preparando construcción ===\n")
    
    # Obtener rutas de los módulos
    try:
        whisper_path, whisper_assets = find_whisper_assets()
        print(f"Whisper encontrado en: {whisper_path}")
        print(f"Whisper assets en: {whisper_assets}")
    except ImportError:
        print("ERROR: Whisper no está instalado. Ejecuta: pip install openai-whisper")
        return False
    
    try:
        torch_path = find_torch_libs()
        print(f"PyTorch encontrado en: {torch_path}")
    except ImportError:
        print("ERROR: PyTorch no está instalado. Ejecuta: pip install torch")
        return False
    
    # Limpiar builds anteriores
    for folder in ['build', 'dist']:
        if os.path.exists(folder):
            print(f"Limpiando {folder}/...")
            shutil.rmtree(folder)
    
    # Comando de PyInstaller
    cmd = [
        sys.executable, '-m', 'PyInstaller',
        '--name=WhisperTranscriptor',
        '--windowed',  # Sin consola (GUI)
        '--noconfirm',  # Sobrescribir sin preguntar
        '--clean',  # Limpiar cache
        
        # Agregar datos de Whisper
        f'--add-data={whisper_assets};whisper/assets',
        
        # Imports ocultos necesarios
        '--hidden-import=whisper',
        '--hidden-import=torch',
        '--hidden-import=torchaudio',
        '--hidden-import=numpy',
        '--hidden-import=tiktoken',
        '--hidden-import=tiktoken_ext',
        '--hidden-import=tiktoken_ext.openai_public',
        '--hidden-import=regex',
        
        # Recopilar todo de estos paquetes
        '--collect-all=whisper',
        '--collect-all=tiktoken',
        '--collect-all=tiktoken_ext',
        
        # Excluir módulos innecesarios para reducir tamaño
        '--exclude-module=matplotlib',
        '--exclude-module=PIL',
        '--exclude-module=IPython',
        '--exclude-module=jupyter',
        '--exclude-module=notebook',
        
        # Script principal
        'transcriptor.py'
    ]
    
    print("\n=== Ejecutando PyInstaller ===\n")
    print("Este proceso puede tardar varios minutos...\n")
    
    try:
        result = subprocess.run(cmd, check=True)
        print("\n=== Construcción exitosa ===\n")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\nERROR: PyInstaller falló con código {e.returncode}")
        return False

def post_build():
    """Tareas post-construcción"""
    dist_path = Path('dist/WhisperTranscriptor')
    
    if not dist_path.exists():
        print("ERROR: La carpeta dist no existe")
        return
    
    # Crear carpeta ffmpeg vacía como recordatorio
    ffmpeg_dist = dist_path / 'ffmpeg'
    ffmpeg_dist.mkdir(exist_ok=True)
    
    # Crear archivo README en la carpeta de distribución
    readme_content = """WHISPER TRANSCRIPTOR
====================

Para usar esta aplicación:

1. Descarga FFmpeg de: https://github.com/BtbN/FFmpeg-Builds/releases
   (Descarga: ffmpeg-master-latest-win64-gpl.zip)

2. Extrae los archivos y copia ffmpeg.exe, ffprobe.exe y ffplay.exe 
   a la carpeta 'ffmpeg' junto a este archivo.

3. Ejecuta WhisperTranscriptor.exe

NOTA: La primera vez que uses cada modelo, se descargará automáticamente.
      Esto requiere conexión a internet.

Modelos disponibles (de menor a mayor calidad/tamaño):
- tiny: ~75MB, más rápido, menor precisión
- base: ~150MB
- small: ~500MB (recomendado)
- medium: ~1.5GB
- large: ~3GB, más lento, mayor precisión
"""
    
    with open(dist_path / 'LEEME.txt', 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    # Copiar FFmpeg si existe
    ffmpeg_src = Path('ffmpeg')
    if ffmpeg_src.exists():
        print("Copiando FFmpeg a la distribución...")
        for file in ffmpeg_src.glob('*.exe'):
            shutil.copy(file, ffmpeg_dist)
    
    print(f"\nArchivos de distribución creados en: {dist_path.absolute()}")
    print("\nContenido de la carpeta:")
    for item in sorted(dist_path.iterdir()):
        size = ""
        if item.is_file():
            size_bytes = item.stat().st_size
            if size_bytes > 1024*1024:
                size = f" ({size_bytes/(1024*1024):.1f} MB)"
            elif size_bytes > 1024:
                size = f" ({size_bytes/1024:.1f} KB)"
        print(f"  - {item.name}{size}")

def main():
    """Función principal"""
    print("=" * 50)
    print("  Whisper Transcriptor - Build Tool")
    print("=" * 50)
    
    if build_executable():
        post_build()
        print("\n" + "=" * 50)
        print("  ¡Construcción completada!")
        print("=" * 50)
        print("\nPróximos pasos:")
        print("1. Asegúrate de copiar FFmpeg a dist/WhisperTranscriptor/ffmpeg/")
        print("2. Prueba el ejecutable")
        print("3. Comprime la carpeta para distribuir")
    else:
        print("\nLa construcción falló. Revisa los errores arriba.")
        sys.exit(1)

if __name__ == "__main__":
    main()
