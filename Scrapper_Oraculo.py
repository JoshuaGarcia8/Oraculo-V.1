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
# --- MÚSCULO: FUNCIONES DE EXTRACCIÓN Y BÚSQUEDA ---

async def extraer_codigos_con_ia(ruta_imagen):
    """🧠 El cerebro del Oráculo: Lee la imagen y saca los códigos"""
    print(f"🧠 Oráculo analizando imagen: {ruta_imagen}...")
    
    # Abrimos la imagen
    img = Image.open(ruta_imagen)
    
    # Instrucciones para Gemini
    prompt = "Extrae todos los códigos de producto de esta imagen. Solo devuelve los códigos separados por comas, nada más."
    
    # Llamada a la IA
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[prompt, img]
    )
    
    # Convertimos el texto de la IA en una lista de Python
    codigos = [c.strip() for c in response.text.split(',')]
    print(f"✅ Códigos detectados: {len(codigos)}")
    return codigos

async def buscar_en_catalogo(page, codigo):
    """🕹️ Lógica de Navegación (Bypass SmartyCart)"""
    print(f"🔍 Buscando código en catálogo: {codigo}...")
    try:
        # Navegamos a la búsqueda (ajustá la URL si es necesario)
        await page.goto(f"https://smartycart.com.ar/search?q={codigo}", timeout=60000)
        await asyncio.sleep(random.uniform(2, 4)) # Delay humano Takumira
        
        # Tomamos captura de evidencia
        ruta_foto = os.path.join(FOLDER_FOTOS, f"{codigo}.png")
        await page.screenshot(path=ruta_foto)
        return "Encontrado"
    except Exception as e:
        print(f"⚠️ Error buscando {codigo}: {e}")
        return "No Encontrado"

# --------------------------------------------------
async def run():
    if not os.path.exists(FOLDER_FOTOS):
        os.makedirs(FOLDER_FOTOS)

    # ✅ Ahora usa la IA real con API segura
    lista_codigos = await extraer_codigos_con_ia(ARCHIVO_PEDIDO)
    
    # [resto del código exactamente igual...]
    
if __name__ == "__main__":
    asyncio.run(run())