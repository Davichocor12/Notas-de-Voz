# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file para Whisper Transcriptor

Uso:
    pyinstaller WhisperTranscriptor.spec

Este archivo de especificación define cómo construir el ejecutable.
Puedes modificarlo según tus necesidades.
"""

import os
import sys
from pathlib import Path

# Encontrar la ruta de whisper para incluir sus assets
def get_whisper_path():
    try:
        import whisper
        return Path(whisper.__file__).parent
    except ImportError:
        print("ERROR: Whisper no instalado. Ejecuta: pip install openai-whisper")
        sys.exit(1)

whisper_path = get_whisper_path()
whisper_assets = whisper_path / 'assets'

block_cipher = None

# Análisis del script principal
a = Analysis(
    ['transcriptor.py'],
    pathex=[],
    binaries=[],
    datas=[
        # Incluir assets de Whisper (vocabularios, etc.)
        (str(whisper_assets), 'whisper/assets'),
    ],
    hiddenimports=[
        'whisper',
        'torch',
        'torchaudio', 
        'numpy',
        'tiktoken',
        'tiktoken_ext',
        'tiktoken_ext.openai_public',
        'regex',
        'ffmpeg',
        'numba',
        'llvmlite',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'PIL',
        'IPython',
        'jupyter',
        'notebook',
        'scipy',  # No necesario para inferencia básica
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='WhisperTranscriptor',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,  # Comprimir con UPX si está disponible
    console=False,  # Sin ventana de consola (aplicación GUI)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    # icon='icon.ico',  # Descomenta y agrega tu icono si lo tienes
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='WhisperTranscriptor',
)
