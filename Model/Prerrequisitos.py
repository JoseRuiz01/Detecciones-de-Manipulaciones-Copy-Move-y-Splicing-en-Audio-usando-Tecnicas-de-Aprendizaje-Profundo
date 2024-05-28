# Instalación de prerrequisitos
import subprocess
import sys

# Función para instalar 
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Lista de paquetes a instalar
packages = [
    "torch",
    "torchaudio",
    "gradio",
    "timm",
    "torchvision",
    "numpy",
    "transformers",
    "PIL"
]

for package in packages:
    install(package)