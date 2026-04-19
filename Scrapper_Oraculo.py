import asyncio
import os
import time
import pandas as pd
from google import genai
from playwright.async_api import async_playwright
from PIL import Image
from pillow_heif import register_heif_opener
import random
from dotenv import load_dotenv

# 🔒 Cargar variables de entorno de forma segura
load_dotenv()

def inicializar_proyecto():
    """Crea la estructura de carpetas y archivos iniciales"""
    print("🧘🏼Entrando en Meditación...")
    
    carpetas = ['data', 'fotos_pedido', 'assets']
    for carpeta in carpetas:
        if not os.path.exists(carpeta):
            os.makedirs(carpeta)
            print(f"✅ Revelacion creada: {carpeta}")

    print("✅ Estructura lista. ¡Listo para la meditación!")

# --- CONFIGURACIÓN SEGURA ---
def cargar_configuracion():
    """Carga la API Key de forma segura desde .env"""
    api_key = os.getenv('GEMINI_API_KEY')
    
    if not api_key or not str(api_key).strip():
        raise SystemExit(
            "\n❌ ERROR CRÍTICO: FALTA GEMINI_API_KEY\n\n"
            "🔧 SOLUCIÓN:\n"
            "1. Crea tu API Key: https://aistudio.google.com/app/apikey\n"
            "2. Crea archivo .env en la raíz del proyecto:\n"
            "   GEMINI_API_KEY=tu_api_key_aqui\n"
            "3. Instala python-dotenv: pip install python-dotenv\n\n"
            "💡 El archivo .env NUNCA se sube a GitHub (está en .gitignore)"
        )
    
    return genai.Client(api_key=str(api_key).strip())

# Inicialización
inicializar_proyecto()
register_heif_opener()
client = cargar_configuracion()  # 🔒 Configuración segura

# Resto del código igual pero limpiando la API hardcodeada...
BASE_DIR = os.getenv('BASE_DIR', './data')
FOLDER_FOTOS = os.path.join(BASE_DIR, "fotos_pedido")
ARCHIVO_PEDIDO = os.path.join(BASE_DIR, "fotopedido.HEIC")

_MODELOS_GEMINI = (
    "gemini-2.0-flash-exp",
    "gemini-1.5-flash",
    "gemini-1.5-pro",
    "gemini-2.0-flash",
    "gemini-1.5-flash-8b",
)

# [El resto de tus funciones permanecen IGUALES hasta async def run()]
# Solo cambio la línea comentada de bypass:

async def run():
    if not os.path.exists(FOLDER_FOTOS):
        os.makedirs(FOLDER_FOTOS)

    # ✅ Ahora usa la IA real con API segura
    lista_codigos = await extraer_codigos_con_ia(ARCHIVO_PEDIDO)
    
    # [resto del código exactamente igual...]
    
if __name__ == "__main__":
    asyncio.run(run())