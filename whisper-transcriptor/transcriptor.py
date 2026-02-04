#!/usr/bin/env python3
"""
Whisper Transcriptor - Aplicación de transcripción de audio
Convierte archivos de audio a texto usando OpenAI Whisper
"""

import os
import sys
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path

# Función para obtener la ruta base (funciona tanto en desarrollo como en ejecutable)
def get_base_path():
    """Obtiene la ruta base del ejecutable o del script"""
    if getattr(sys, 'frozen', False):
        # Ejecutando como ejecutable empaquetado
        return Path(sys._MEIPASS)
    else:
        # Ejecutando como script Python
        return Path(__file__).parent

def get_app_path():
    """Obtiene la ruta donde está el ejecutable/script"""
    if getattr(sys, 'frozen', False):
        return Path(sys.executable).parent
    else:
        return Path(__file__).parent

# Configurar FFmpeg
def setup_ffmpeg():
    """Configura las rutas de FFmpeg"""
    base_path = get_base_path()
    app_path = get_app_path()
    
    # Buscar FFmpeg en varias ubicaciones
    possible_paths = [
        base_path / "ffmpeg",
        base_path / "ffmpeg" / "bin",
        app_path / "ffmpeg",
        app_path / "ffmpeg" / "bin",
        Path("ffmpeg"),
        Path("ffmpeg") / "bin",
    ]
    
    # En Windows, agregar rutas específicas
    if sys.platform == "win32":
        possible_paths.extend([
            Path(r"C:\ffmpeg_local"),
            Path(r"C:\ffmpeg\bin"),
            Path(os.environ.get("LOCALAPPDATA", "")) / "ffmpeg" / "bin",
        ])
    
    ffmpeg_dir = None
    ffmpeg_exe = None
    
    for path in possible_paths:
        if sys.platform == "win32":
            exe_path = path / "ffmpeg.exe"
        else:
            exe_path = path / "ffmpeg"
        
        if exe_path.exists():
            ffmpeg_dir = str(path)
            ffmpeg_exe = str(exe_path)
            break
    
    if ffmpeg_exe and ffmpeg_dir:
        os.environ["FFMPEG_BINARY"] = ffmpeg_exe
        os.environ["PATH"] = ffmpeg_dir + os.pathsep + os.environ.get("PATH", "")
        return True, ffmpeg_exe
    
    return False, None

class TranscriptorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Whisper Transcriptor")
        self.root.geometry("700x550")
        self.root.resizable(True, True)
        
        # Variables
        self.audio_file = tk.StringVar()
        self.model_var = tk.StringVar(value="small")
        self.language_var = tk.StringVar(value="es")
        self.is_transcribing = False
        self.model = None
        
        # Configurar estilo
        self.setup_style()
        
        # Crear interfaz
        self.create_widgets()
        
        # Configurar FFmpeg al inicio
        self.check_ffmpeg()
    
    def setup_style(self):
        """Configura el estilo de la aplicación"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Colores
        bg_color = "#2b2b2b"
        fg_color = "#ffffff"
        accent_color = "#4a9eff"
        
        self.root.configure(bg=bg_color)
        
        style.configure("TFrame", background=bg_color)
        style.configure("TLabel", background=bg_color, foreground=fg_color, font=("Segoe UI", 10))
        style.configure("TButton", font=("Segoe UI", 10))
        style.configure("Header.TLabel", font=("Segoe UI", 16, "bold"), foreground=accent_color)
        style.configure("Status.TLabel", font=("Segoe UI", 9), foreground="#888888")
    
    def create_widgets(self):
        """Crea los widgets de la interfaz"""
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title_label = ttk.Label(main_frame, text="🎙️ Whisper Transcriptor", style="Header.TLabel")
        title_label.pack(pady=(0, 20))
        
        # Frame de selección de archivo
        file_frame = ttk.LabelFrame(main_frame, text="Archivo de Audio", padding="10")
        file_frame.pack(fill=tk.X, pady=(0, 15))
        
        file_entry = ttk.Entry(file_frame, textvariable=self.audio_file, width=60)
        file_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        browse_btn = ttk.Button(file_frame, text="Examinar...", command=self.browse_file)
        browse_btn.pack(side=tk.RIGHT)
        
        # Frame de opciones
        options_frame = ttk.LabelFrame(main_frame, text="Opciones", padding="10")
        options_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Modelo
        model_frame = ttk.Frame(options_frame)
        model_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(model_frame, text="Modelo:").pack(side=tk.LEFT, padx=(0, 10))
        models = ["tiny", "base", "small", "medium", "large"]
        model_combo = ttk.Combobox(model_frame, textvariable=self.model_var, values=models, state="readonly", width=15)
        model_combo.pack(side=tk.LEFT)
        
        ttk.Label(model_frame, text="(small recomendado)", style="Status.TLabel").pack(side=tk.LEFT, padx=(10, 0))
        
        # Idioma
        lang_frame = ttk.Frame(options_frame)
        lang_frame.pack(fill=tk.X)
        
        ttk.Label(lang_frame, text="Idioma:").pack(side=tk.LEFT, padx=(0, 10))
        languages = [
            ("Español", "es"),
            ("Inglés", "en"),
            ("Francés", "fr"),
            ("Alemán", "de"),
            ("Italiano", "it"),
            ("Portugués", "pt"),
            ("Detectar auto", None)
        ]
        lang_names = [l[0] for l in languages]
        self.lang_map = {l[0]: l[1] for l in languages}
        lang_combo = ttk.Combobox(lang_frame, values=lang_names, state="readonly", width=15)
        lang_combo.set("Español")
        lang_combo.bind("<<ComboboxSelected>>", lambda e: self.language_var.set(self.lang_map.get(lang_combo.get(), "es") or ""))
        lang_combo.pack(side=tk.LEFT)
        
        # Botón de transcribir
        self.transcribe_btn = ttk.Button(main_frame, text="🎯 Iniciar Transcripción", command=self.start_transcription)
        self.transcribe_btn.pack(pady=15)
        
        # Barra de progreso
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.pack(fill=tk.X, pady=(0, 10))
        
        # Estado
        self.status_label = ttk.Label(main_frame, text="Listo", style="Status.TLabel")
        self.status_label.pack()
        
        # Área de resultado
        result_frame = ttk.LabelFrame(main_frame, text="Transcripción", padding="10")
        result_frame.pack(fill=tk.BOTH, expand=True, pady=(15, 0))
        
        # Text widget con scrollbar
        text_frame = ttk.Frame(result_frame)
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.result_text = tk.Text(text_frame, wrap=tk.WORD, font=("Consolas", 10),
                                   bg="#1e1e1e", fg="#ffffff", insertbackground="#ffffff",
                                   yscrollcommand=scrollbar.set)
        self.result_text.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.result_text.yview)
        
        # Botones de acción para el resultado
        action_frame = ttk.Frame(main_frame)
        action_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.copy_btn = ttk.Button(action_frame, text="📋 Copiar", command=self.copy_result, state=tk.DISABLED)
        self.copy_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.save_btn = ttk.Button(action_frame, text="💾 Guardar como...", command=self.save_result, state=tk.DISABLED)
        self.save_btn.pack(side=tk.LEFT)
    
    def check_ffmpeg(self):
        """Verifica si FFmpeg está disponible"""
        found, path = setup_ffmpeg()
        if found:
            self.update_status(f"FFmpeg encontrado: {path}")
        else:
            self.update_status("⚠️ FFmpeg no encontrado - Coloca FFmpeg en la carpeta 'ffmpeg'")
    
    def browse_file(self):
        """Abre el diálogo para seleccionar archivo"""
        filetypes = [
            ("Archivos de audio", "*.mp3 *.wav *.m4a *.aac *.ogg *.flac *.wma *.opus"),
            ("MP3", "*.mp3"),
            ("WAV", "*.wav"),
            ("M4A", "*.m4a"),
            ("Todos los archivos", "*.*")
        ]
        
        filename = filedialog.askopenfilename(
            title="Selecciona el archivo de audio",
            filetypes=filetypes
        )
        
        if filename:
            self.audio_file.set(filename)
            self.update_status(f"Archivo seleccionado: {Path(filename).name}")
    
    def update_status(self, message):
        """Actualiza el mensaje de estado"""
        self.status_label.config(text=message)
        self.root.update_idletasks()
    
    def start_transcription(self):
        """Inicia el proceso de transcripción"""
        if self.is_transcribing:
            return
        
        audio_path = self.audio_file.get()
        if not audio_path:
            messagebox.showwarning("Atención", "Por favor selecciona un archivo de audio primero.")
            return
        
        if not os.path.exists(audio_path):
            messagebox.showerror("Error", "El archivo seleccionado no existe.")
            return
        
        self.is_transcribing = True
        self.transcribe_btn.config(state=tk.DISABLED)
        self.progress.start(10)
        self.result_text.delete(1.0, tk.END)
        self.copy_btn.config(state=tk.DISABLED)
        self.save_btn.config(state=tk.DISABLED)
        
        # Ejecutar en hilo separado
        thread = threading.Thread(target=self.transcribe_audio, args=(audio_path,))
        thread.daemon = True
        thread.start()
    
    def transcribe_audio(self, audio_path):
        """Realiza la transcripción del audio"""
        try:
            self.update_status("Cargando modelo Whisper...")
            
            import whisper
            
            model_name = self.model_var.get()
            
            # Cargar modelo (se descarga automáticamente si no existe)
            self.update_status(f"Cargando modelo '{model_name}'... (puede tardar la primera vez)")
            model = whisper.load_model(model_name)
            
            self.update_status("Transcribiendo audio... Por favor espera.")
            
            # Configurar idioma
            language = self.language_var.get() if self.language_var.get() else None
            
            # Realizar transcripción
            result = model.transcribe(
                audio_path,
                language=language,
                fp16=False,
                verbose=False
            )
            
            transcription = result["text"]
            
            # Guardar automáticamente
            output_file = os.path.splitext(audio_path)[0] + "_transcripcion.txt"
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(transcription)
            
            # Actualizar UI en el hilo principal
            self.root.after(0, lambda: self.transcription_complete(transcription, output_file))
            
        except Exception as e:
            error_msg = str(e)
            self.root.after(0, lambda: self.transcription_error(error_msg))
    
    def transcription_complete(self, text, output_file):
        """Maneja la finalización exitosa de la transcripción"""
        self.is_transcribing = False
        self.progress.stop()
        self.transcribe_btn.config(state=tk.NORMAL)
        
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, text)
        
        self.copy_btn.config(state=tk.NORMAL)
        self.save_btn.config(state=tk.NORMAL)
        
        self.update_status(f"✅ Transcripción completada y guardada en: {Path(output_file).name}")
        messagebox.showinfo("Completado", f"Transcripción guardada en:\n{output_file}")
    
    def transcription_error(self, error):
        """Maneja los errores de transcripción"""
        self.is_transcribing = False
        self.progress.stop()
        self.transcribe_btn.config(state=tk.NORMAL)
        
        self.update_status(f"❌ Error: {error}")
        messagebox.showerror("Error", f"Error durante la transcripción:\n{error}")
    
    def copy_result(self):
        """Copia el resultado al portapapeles"""
        text = self.result_text.get(1.0, tk.END).strip()
        if text:
            self.root.clipboard_clear()
            self.root.clipboard_append(text)
            self.update_status("📋 Texto copiado al portapapeles")
    
    def save_result(self):
        """Guarda el resultado en un archivo"""
        text = self.result_text.get(1.0, tk.END).strip()
        if not text:
            return
        
        filename = filedialog.asksaveasfilename(
            title="Guardar transcripción",
            defaultextension=".txt",
            filetypes=[("Archivo de texto", "*.txt"), ("Todos los archivos", "*.*")]
        )
        
        if filename:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(text)
            self.update_status(f"💾 Guardado en: {Path(filename).name}")


def main():
    """Función principal"""
    # Configurar FFmpeg antes de iniciar
    setup_ffmpeg()
    
    # Crear ventana principal
    root = tk.Tk()
    
    # Centrar ventana
    root.update_idletasks()
    width = 700
    height = 550
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    # Crear aplicación
    app = TranscriptorApp(root)
    
    # Ejecutar
    root.mainloop()


if __name__ == "__main__":
    main()
