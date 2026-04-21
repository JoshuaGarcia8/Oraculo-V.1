import asyncio
import os
import pandas as pd
import random
from google import genai             # <-- Corrige error "genai"
from PIL import Image                # <-- Corrige error "Image"
from playwright.async_api import async_playwright
from pillow_heif import register_heif_opener
from dotenv import load_dotenv

# 1. SETUP
load_dotenv()
register_heif_opener()

def inicializar():
    print("🧘🏼 El Oráculo entra en meditación...")
    for carpeta in ['data', 'fotos_pedido']:
        if not os.path.exists(carpeta):
            os.makedirs(carpeta)
    print("✅ Carpetas listas.")

def cargar_cliente():
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        raise SystemExit("❌ Error: Falta la API Key en el .env")
    return genai.Client(api_key=api_key.strip())

# 2. EXTRACCIÓN (CEREBRO IA)
async def extraer_codigos(ruta_imagen):
    client = cargar_cliente()
    if not os.path.exists(ruta_imagen):
        print(f"❌ No encuentro la foto en: {ruta_imagen}")
        return []

    print(f"🧠 Optimizando imagen para ahorrar tokens...")
    img = Image.open(ruta_imagen)
    img.thumbnail((1024, 1024)) # Achicamos para gastar menos
    img = img.convert("RGB")

    prompt = "Extrae códigos de productos. Devolvé solo los códigos separados por comas."

    modelos_a_probar = ["gemini-1.5-flash", "gemini-3-flash-preview", "gemini-2.0-flash"]
    
    for modelo in modelos_a_probar:
        try:
            response = client.models.generate_content(
                model=modelo,
                contents=[prompt, img],
                config={"temperature": 0.1, "max_output_tokens": 500}
            )
            if response.text:
                tokens = response.usage_metadata.total_token_count
                print(f"💎 Consumo: {tokens} tokens con {modelo}")
                return [c.strip() for c in response.text.split(",") if c.strip()]
        except:
            continue
    return []

# 3. VERIFICACIÓN (PLAYWRIGHT)
async def verificar_smarty(page, codigo):
    try:
        url = f"https://www.smartycart.com.ar/token/0cdedce40a9643385a3d9d745c1295a2c9016ecc?keyword={codigo}"
        await page.goto(url, timeout=20000)
        await asyncio.sleep(1.5)
        producto = await page.query_selector(".product-item, .product-name, h1, .title")
        estado = "Encontrado" if producto else "No encontrado"
        await page.screenshot(path=f"fotos_pedido/{codigo}.png")
        return estado
    except:
        return "Error de Red"

# 4. FLUJO PRINCIPAL (CON IDEA PRO CORREGIDA)
async def run():
    inicializar()
    archivo_pedido = "./data/fotopedido.HEIC"
    archivo_csv = "./data/reporte_automatizacion.csv"
    
    codigos = []
    # 🚀 IDEA PRO: Reutilizar CSV si existe
    if os.path.exists(archivo_csv):
        print("💡 Encontré un reporte anterior.")
        resp = input("¿Reutilizar los códigos del CSV para no gastar tokens? (s/n): ").lower()
        if resp == 's':
            df_temp = pd.read_csv(archivo_csv)
            if 'Código' in df_temp.columns:
                codigos = df_temp['Código'].dropna().unique().tolist()
                print(f"♻️ Reutilizando {len(codigos)} códigos.")

    # Si no hay códigos, le pedimos a la IA
    if not codigos:
        codigos = await extraer_codigos(archivo_pedido)
    
    if not codigos:
        print("❌ No se obtuvieron códigos.")
        return

    # --- AQUÍ DEFINIMOS RESULTADOS (Corrige error "resultados" is not defined) ---
    resultados = [] 

    print(f"🎯 Iniciando verificación de {len(codigos)} productos...")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        
        for i, cod in enumerate(codigos):
            estado = await verificar_smarty(page, cod)
            # Guardamos en la lista que definimos arriba
            resultados.append({"Código": cod, "Estado": estado}) 
            print(f"🔍 {i+1}/{len(codigos)}: {cod} -> {estado}")
            await asyncio.sleep(random.uniform(1, 2))
        
        await browser.close()

    # 📊 Guardar Reporte Final
    df_final = pd.DataFrame(resultados)
    df_final.to_csv(archivo_csv, index=False)
    print(f"\n🎉 ¡MISIÓN CUMPLIDA! Reporte guardado en {archivo_csv}")

if __name__ == "__main__":
    asyncio.run(run())