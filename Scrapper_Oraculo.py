import asyncio
import os
import pandas as pd
import random
from google import genai
from PIL import Image
from playwright.async_api import async_playwright
from pillow_heif import register_heif_opener
from dotenv import load_dotenv

# 1. SETUP
load_dotenv()
register_heif_opener()

def inicializar():
    print("📿 El Oráculo inicia su ritual... El artesano prepara sus herramientas.")
    for carpeta in ['data', 'fotos_pedido']:
        if not os.path.exists(carpeta):
            os.makedirs(carpeta)
    print("✅ Recintos sagrados (carpetas) preparados.")

def cargar_cliente():
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        # Corregido el typo del error anterior
        raise SystemExit("⚠️ El Oráculo está ciego. Falta la esencia (API Key) en el .env.")
    return genai.Client(api_key=api_key.strip())

# 2. EXTRACCIÓN (CEREBRO IA)
async def extraer_codigos(ruta_imagen):
    client = cargar_cliente()
    if not os.path.exists(ruta_imagen):
        print(f"❌ El Oráculo no encuentra el pergamino en: {ruta_imagen}")
        return []

    print(f"👁️ Agudizando el ojo del artesano... Purificando la visión de la imagen.")
    img = Image.open(ruta_imagen)
    img.thumbnail((1024, 1024)) 
    img = img.convert("RGB")

    prompt = "Extrae códigos de productos. Devolvé solo los códigos separados por comas."

    modelos_a_probar = ["gemini-1.5-flash", "gemini-3-flash-preview", "gemini-2.0-flash"]
    
    for modelo in modelos_a_probar:
        try:
            print(f"🔮 Consultando los pergaminos de {modelo}...")
            response = client.models.generate_content(
                model=modelo,
                contents=[prompt, img],
                config={"temperature": 0.1, "max_output_tokens": 500}
            )
            if response.text:
                tokens = response.usage_metadata.total_token_count
                print(f"✨ Energía consumida: {tokens} motas de luz (tokens) con {modelo}.")
                return [c.strip() for c in response.text.split(",") if c.strip()]
        except:
            continue
    return []

# 3. VERIFICACIÓN (PLAYWRIGHT)
async def verificar_smarty(page, codigo):
    try:
        url = f"https://www.smartycart.com.ar/token/0cdedce40a9643385a3d9d745c1295a2c9016ecc?keyword={codigo}"
        await page.goto(url, timeout=25000)
        
        # 🧘🏼 Esperamos a que la página se relaje y cargue las imágenes
        await page.wait_for_load_state("networkidle")
        await asyncio.sleep(2) 

        # 🎯 Lista de posibles escondites de la imagen (Selectores)
        # Agregamos el zoomImg que encontraste y otros comunes
        posibles_fotos = [
            "img.zoomImg", 
            ".product-item img", 
            ".product-image img", 
            "img[src*='product_image']", # Busca cualquier imagen que tenga 'product_image' en el link
            ".img-responsive"
        ]

        foto_elemento = None
        for selector in posibles_fotos:
            foto_elemento = await page.query_selector(selector)
            if foto_elemento:
                # Si la encontramos, verificamos que sea visible
                if await foto_elemento.is_visible():
                    break 

        if foto_elemento:
            estado = "Encontrado"
            # Nos aseguramos de que el scroll esté parado sobre la imagen
            await foto_elemento.scroll_into_view_if_needed()
            await asyncio.sleep(0.5)
            # 📸 Captura quirúrgica del elemento
            await foto_elemento.screenshot(path=f"fotos_pedido/{codigo}.png")
        else:
            # Si no hay foto, chequeamos si al menos aparece el código en texto
            cuerpo_pagina = await page.content()
            if codigo in cuerpo_pagina:
                estado = "Encontrado (Sin Foto)"
                # Sacamos captura de pantalla completa como backup si la IA falló el recorte
                await page.screenshot(path=f"fotos_pedido/REVISAR_{codigo}.png")
            else:
                estado = "No encontrado"
        
        return estado
    except Exception as e:
        print(f"⚠️ Niebla en la visión de {codigo}: {str(e)[:50]}")
        return "Error de Red"

# 4. FLUJO PRINCIPAL
async def run():
    inicializar()
    archivo_pedido = "./data/fotopedido.HEIC"
    archivo_csv = "./data/reporte_automatizacion.csv"
    
    codigos = []
    if os.path.exists(archivo_csv):
        print("💡 Visiones pasadas encontradas en el registro.")
        resp = input("¿Deseas invocar las visiones del CSV para ahorrar esencia (tokens)? (s/n): ").lower()
        if resp == 's':
            df_temp = pd.read_csv(archivo_csv)
            if 'Código' in df_temp.columns:
                codigos = df_temp['Código'].dropna().unique().tolist()
                print(f"♻️ Manifestando {len(codigos)} códigos desde el registro ancestral.")

    if not codigos:
        codigos = await extraer_codigos(archivo_pedido)
    
    if not codigos:
        print("❌ El Oráculo no ha podido revelar ningún código.")
        return

    resultados = [] 
    print(f"📜 Revelando la verdad del inventario en SmartyCart...")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        
        for i, cod in enumerate(codigos):
            estado = await verificar_smarty(page, cod)
            resultados.append({"Código": cod, "Estado": estado}) 
            print(f"🌀 Revelando {cod}: {i+1} de {len(codigos)} visiones completadas -> {estado}")
            await asyncio.sleep(random.uniform(1, 2))
        
        await browser.close()

    df_final = pd.DataFrame(resultados)
    df_final.to_csv(archivo_csv, index=False)
    print(f"\n🏮 Iluminación alcanzada. El conocimiento ha sido plasmado en {archivo_csv}")

if __name__ == "__main__":
    asyncio.run(run())