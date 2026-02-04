# 🎙️ Whisper Transcriptor

Aplicación de escritorio para transcribir archivos de audio a texto usando **OpenAI Whisper**.

Esta aplicación permite convertir archivos de audio (MP3, WAV, M4A, etc.) a texto de manera sencilla, sin necesidad de conocimientos técnicos.

## ✨ Características

- 🎨 Interfaz gráfica moderna y fácil de usar
- 🌍 Soporte para múltiples idiomas (Español, Inglés, Francés, etc.)
- 📊 Varios modelos de transcripción (desde rápido hasta alta precisión)
- 💾 Guardado automático de transcripciones
- 📋 Copiar al portapapeles con un clic
- 🔧 No requiere Python instalado (versión ejecutable)

## 📋 Requisitos del Sistema

### Para usar el ejecutable (usuarios finales):
- Windows 10/11 (64-bit)
- 8GB RAM mínimo (16GB recomendado para modelos grandes)
- Conexión a internet (para descargar modelos la primera vez)

### Para compilar desde código fuente:
- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- 10GB de espacio libre (para dependencias y modelos)

---

## 🚀 Opción 1: Usar el Ejecutable (Recomendado para usuarios)

### Paso 1: Descargar FFmpeg

FFmpeg es necesario para procesar archivos de audio.

1. Ve a: https://github.com/BtbN/FFmpeg-Builds/releases
2. Descarga: `ffmpeg-master-latest-win64-gpl.zip`
3. Extrae el archivo ZIP
4. Dentro encontrarás una carpeta `bin/` con estos archivos:
   - `ffmpeg.exe`
   - `ffprobe.exe`
   - `ffplay.exe`
5. Copia estos 3 archivos a la carpeta `ffmpeg/` junto al ejecutable

### Paso 2: Ejecutar la aplicación

1. Doble clic en `WhisperTranscriptor.exe`
2. Selecciona un archivo de audio
3. Elige el modelo e idioma
4. Clic en "Iniciar Transcripción"
5. ¡Listo! La transcripción se guardará automáticamente

### Estructura de carpetas esperada:
```
WhisperTranscriptor/
├── WhisperTranscriptor.exe
├── ffmpeg/
│   ├── ffmpeg.exe
│   ├── ffprobe.exe
│   └── ffplay.exe
├── LEEME.txt
└── (otros archivos del programa)
```

---

## 🛠️ Opción 2: Compilar desde Código Fuente

### Requisitos previos

1. **Instalar Python 3.8+** desde https://python.org
   - ✅ Marca "Add Python to PATH" durante la instalación

2. **Descargar FFmpeg** (ver instrucciones arriba)

### Pasos para compilar

#### Método A: Script automático (Windows)

```batch
# 1. Abre una terminal (CMD o PowerShell) en la carpeta del proyecto

# 2. Ejecuta el script de construcción
build.bat
```

#### Método B: Manual

```batch
# 1. Crear entorno virtual
python -m venv venv

# 2. Activar entorno virtual
venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Construir ejecutable
python build_exe.py

# O alternativamente con el archivo .spec:
pyinstaller WhisperTranscriptor.spec
```

### Resultado

El ejecutable se creará en: `dist/WhisperTranscriptor/`

**Importante:** Copia la carpeta `ffmpeg/` con los ejecutables de FFmpeg a `dist/WhisperTranscriptor/ffmpeg/` antes de distribuir.

---

## 📁 Estructura del Proyecto

```
whisper-transcriptor/
├── transcriptor.py          # Código principal de la aplicación
├── build_exe.py             # Script para construir el ejecutable
├── build.bat                # Script de construcción para Windows
├── requirements.txt         # Dependencias de Python
├── WhisperTranscriptor.spec # Configuración de PyInstaller
├── README.md                # Este archivo
└── ffmpeg/                  # Carpeta para FFmpeg (crear manualmente)
    ├── ffmpeg.exe
    ├── ffprobe.exe
    └── ffplay.exe
```

---

## 🎯 Modelos de Whisper

| Modelo | Tamaño | RAM necesaria | Velocidad | Precisión |
|--------|--------|---------------|-----------|-----------|
| tiny   | ~75 MB | ~1 GB | Muy rápido | Básica |
| base   | ~150 MB | ~1 GB | Rápido | Buena |
| **small** | ~500 MB | ~2 GB | Moderado | **Recomendado** |
| medium | ~1.5 GB | ~5 GB | Lento | Muy buena |
| large  | ~3 GB | ~10 GB | Muy lento | Excelente |

**Recomendación:** Usa el modelo `small` para un buen balance entre calidad y velocidad.

---

## ❓ Solución de Problemas

### "FFmpeg no encontrado"
- Asegúrate de que `ffmpeg.exe` esté en la carpeta `ffmpeg/`
- Verifica que la carpeta `ffmpeg/` esté junto al ejecutable

### "Error al cargar el modelo"
- Verifica tu conexión a internet (los modelos se descargan automáticamente)
- Asegúrate de tener suficiente espacio en disco
- Prueba con un modelo más pequeño (tiny o base)

### "La transcripción es muy lenta"
- Usa un modelo más pequeño (tiny, base o small)
- Cierra otras aplicaciones para liberar RAM
- Los archivos de audio largos toman más tiempo

### "Error de memoria"
- Usa un modelo más pequeño
- Cierra otras aplicaciones
- Considera dividir el audio en partes más cortas

### La aplicación no abre
- Verifica que tienes Windows 64-bit
- Intenta ejecutar como administrador
- Revisa el antivirus (puede bloquear aplicaciones desconocidas)

---

## 🔧 Desarrollo

### Ejecutar en modo desarrollo

```bash
# Activar entorno virtual
venv\Scripts\activate

# Ejecutar directamente
python transcriptor.py
```

### Agregar un ícono personalizado

1. Crea o descarga un archivo `.ico`
2. Descomenta la línea `icon='icon.ico'` en `WhisperTranscriptor.spec`
3. Reconstruye el ejecutable

---

## 📄 Licencia

Este proyecto usa componentes de código abierto:
- [OpenAI Whisper](https://github.com/openai/whisper) - MIT License
- [PyTorch](https://pytorch.org/) - BSD License
- [FFmpeg](https://ffmpeg.org/) - LGPL/GPL License

---

## 🤝 Contribuir

¿Encontraste un bug o tienes una sugerencia? ¡Las contribuciones son bienvenidas!

1. Haz fork del repositorio
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -m 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

---

## 📞 Soporte

Si tienes problemas o preguntas, abre un Issue en el repositorio.
