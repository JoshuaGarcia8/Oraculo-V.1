import asyncio
import os
import pandas as pd
import random
from playwright.async_api import async_playwright
from dotenv import load_dotenv

load_dotenv()

def inicializar():
    print("🧘🏼 El Oráculo entra en meditación...")
    for carpeta in ['data', 'fotos_pedido']:
        os.makedirs(carpeta, exist_ok=True)
    print("✅ Listo! (Modo BYPASS IA activado)")

# 🎯 BYPASS IA - Códigos reales de juguetería
def obtener_codigos_manual():
    """🔄 Modo emergencia: códigos hardcodeados reales"""
    codigos = [
        "AD2020-36", "ADME-080", "CRFE515", "DIT2788", "DIT3010",
        "DIT3029", "DIT3030", "JYJ0043", "JYJ0044", "JYJ0045",
        "JYJ0046", "LCFTY4014", "LCSET503", "LCSET504", "LG2027",
        "LI1501", "SEB51106", "SEB55274"
    ]
    print(f"✅ BYPASS IA: {len(codigos)} códigos cargados")
    return codigos

async def verificar_smarty(page, codigo):
    """🕹️ Buscador SmartyCart stealth"""
    try:
        # URL real SmartyCart
        url_base = "https://www.smartycart.com.ar/token/0cdedce40a9643385a3d9d745c1295a2c9016ecc"
        search_url = f"{url_base}?keyword={codigo}"
        
        await page.goto(search_url, wait_until="networkidle", timeout=20000)
        await asyncio.sleep(random.uniform(1.5, 2.5))
        
        # Detectar producto (múltiples selectores)
        selectores = [
            ".product-item", ".item-image-primary", 
            ".product-name", "[class*='product']",
            "img[src*='.jpg']"
        ]
        
        elemento = None
        for selector in selectores:
            elemento = await page.query_selector(selector)
            if elemento:
                break
        
        estado = "✅ ENCONTRADO" if elemento else "❌ NO ENCONTRADO"
        
        # 📸 Evidencia
        foto_path = f"fotos_pedido/{codigo}.png"
        await page.screenshot(path=foto_path, full_page=True)
        
        print(f"   📸 {foto_path} guardada")
        return estado
        
    except Exception as e:
        return f"⚠️ ERROR: {str(e)[:30]}"

async def run():
    inicializar()
    FOLDER_FOTOS = "fotos_pedido"
    os.makedirs(FOLDER_FOTOS, exist_ok=True)
    
    # 🎯 Códigos reales (sin IA)
    codigos = obtener_codigos_manual()
    
    print(f"\n🎯 SMARTYCART HUNT: {len(codigos)} ítems")
    resultados = []

    # 🕹️ Playwright stealth mode
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False, 
            slow_mo=1200,
            args=['--disable-blink-features=AutomationControlled']
        )
        
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={'width': 1366, 'height': 768}
        )
        page = await context.new_page()
        
        # Anti-detección
        await page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
            delete navigator.__proto__.webdriver;
        """)
        
        for i, codigo in enumerate(codigos):
            print(f"\n🔍 [{i+1}/{len(codigos)}] {codigo}")
            estado = await verificar_smarty(page, codigo)
            resultados.append({"Código": codigo, "Estado": estado})
            
            # Pausa humana anti-ban
            pausa = random.uniform(3, 6)
            print(f"⏳ Espera humana: {pausa:.1f}s")
            await asyncio.sleep(pausa)
        
        await browser.close()

    # 📊 Reporte profesional
    df = pd.DataFrame(resultados)
    reporte_path = "./data/reporte_oraculo.csv"
    df.to_csv(reporte_path, index=False)
    
    encontrados = sum(1 for r in resultados if "✅" in r["Estado"])
    print(f"\n🎉 MISSION COMPLETE!")
    print(f"✅ Encontrados: {encontrados}/{len(resultados)}")
    print(f"📊 Reporte: {reporte_path}")
    print(f"🖼️  Evidencias: fotos_pedido/")

if __name__ == "__main__":
    asyncio.run(run())