#!/usr/bin/env python3
"""
Whisper Transcriptor - Versión Simple
Versión minimalista basada en el código original del usuario
"""

import os
import sys
from pathlib import Path
from tkinter import Tk, filedialog, messagebox

def get_base_path():
    """Obtiene la ruta base del ejecutable o del script"""
    if getattr(sys, 'frozen', False):
        return Path(sys._MEIPASS)
    else:
        return Path(__file__).parent

def get_app_path():
    """Obtiene la ruta donde está el ejecutable/script"""
    if getattr(sys, 'frozen', False):
        return Path(sys.executable).parent
    else:
        return Path(__file__).parent

def setup_ffmpeg():
    """Configura FFmpeg buscando en varias ubicaciones"""
    base_path = get_base_path()
    app_path = get_app_path()
    
    possible_paths = [
        app_path / "ffmpeg",
        base_path / "ffmpeg",
        Path("ffmpeg"),
    ]
    
    if sys.platform == "win32":
        possible_paths.extend([
            Path(r"C:\ffmpeg_local"),
            Path(r"C:\ffmpeg\bin"),
        ])
    
    for path in possible_paths:
        exe_name = "ffmpeg.exe" if sys.platform == "win32" else "ffmpeg"
        exe_path = path / exe_name
        
        if exe_path.exists():
            os.environ["FFMPEG_BINARY"] = str(exe_path)
            os.environ["PATH"] = str(path) + os.pathsep + os.environ.get("PATH", "")
            print(f"FFmpeg encontrado: {exe_path}")
            return True
    
    print("AVISO: FFmpeg no encontrado")
    print("Coloca ffmpeg.exe en la carpeta 'ffmpeg/' junto al ejecutable")
    return False

def main():
    # Configurar FFmpeg
    setup_ffmpeg()
    
    # Importar whisper después de configurar FFmpeg
    import whisper
    
    # Ocultar ventana principal de Tk
    root = Tk()
    root.withdraw()
    
    # Selector de archivo
    audio_file = filedialog.askopenfilename(
        title="Selecciona el archivo de audio",
        filetypes=[
            ("Archivos de audio", "*.mp3 *.wav *.m4a *.aac *.ogg *.flac *.wma"),
            ("MP3", "*.mp3"),
            ("WAV", "*.wav"),
            ("Todos los archivos", "*.*")
        ]
    )
    
    if not audio_file:
        messagebox.showinfo("Cancelado", "No se seleccionó ningún archivo.")
        return
    
    print(f"\nArchivo seleccionado: {audio_file}")
    
    # Mostrar mensaje de carga
    print("\nCargando modelo Whisper 'small'...")
    print("(Esto puede tardar la primera vez mientras se descarga el modelo)")
    
    # Cargar modelo
    model = whisper.load_model("small")
    
    print("\nTranscribiendo audio... Por favor espera.")
    
    # Transcripción
    result = model.transcribe(
        audio_file,
        language="es",
        fp16=False,
        verbose=False
    )
    
    transcription = result["text"]
    
    print("\n" + "=" * 50)
    print("TRANSCRIPCIÓN")
    print("=" * 50)
    print(transcription)
    print("=" * 50)
    
    # Guardar resultado
    output_txt = os.path.splitext(audio_file)[0] + "_transcripcion.txt"
    with open(output_txt, "w", encoding="utf-8") as f:
        f.write(transcription)
    
    print(f"\n✅ Transcripción guardada en: {output_txt}")
    
    # Mostrar mensaje de éxito
    messagebox.showinfo(
        "Completado", 
        f"Transcripción completada y guardada en:\n{output_txt}"
    )

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        Tk().withdraw()
        messagebox.showerror("Error", f"Ocurrió un error:\n{e}")
        input("\nPresiona Enter para salir...")
