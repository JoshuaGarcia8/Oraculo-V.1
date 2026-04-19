# 🧿 Oráculo V.1 - Automatización Inteligente de Inventario

> **"Transformando el caos del stock manual en datos precisos con visión de calidad."**

## 🎯 El Problema
En el sector retail, específicamente en la gestión de depósitos de jugueterías, el control de stock suele depender de pedidos escritos a mano o capturas de pantalla de catálogos físicos. Este proceso manual conlleva:
- ❌ **Pérdida de tiempo:** Más de 30 minutos por cada lista de pedido.
- ❌ **Errores humanos:** Transcripción incorrecta de códigos alfanuméricos.
- ❌ **Falta de trazabilidad:** Dificultad para auditar qué se encontró y qué no.

## 🚀 La Solución: Oráculo
**Oráculo** es una herramienta de **QA Automation** que actúa como un puente entre el mundo físico y el digital. El sistema automatiza el flujo completo de verificación de mercadería.

### ¿Cómo funciona?
1.  **Visión de IA:** Analiza una fotografía del pedido (`.HEIC` o `.jpg`) y utiliza **Gemini AI** para extraer los códigos de producto de forma automática.
2.  **Navegación Sigilosa:** Utiliza **Playwright** con técnicas de evasión de detección (Stealth Mode) para buscar cada producto en la web oficial del proveedor.
3.  **Captura de Evidencia:** El robot navega, encuentra el producto, descarga la imagen de referencia y valida su existencia.
4.  **Reporte de Calidad:** Genera un archivo `.csv` detallado con el estado de cada código (Encontrado/No Encontrado) para una auditoría inmediata.

## 🛠️ Stack Tecnológico
* **Lenguaje:** Python 3.14
* **Automatización:** Playwright (Chromium)
* **Inteligencia Artificial:** Google Gemini API (Modelos Flash & Pro)
* **Procesamiento de Imágenes:** Pillow & Pillow-heif (Soporte para iPhone)
* **Gestión de Datos:** Pandas
* **Seguridad:** Python-dotenv (Protección de API Keys)

## 🗺️ Hoja de Ruta (Roadmap)

### Fase 1: Scrapper Artesano (ACTUAL)
* ✅ Extracción de códigos mediante OCR.
* ✅ Navegación automatizada y descarga de imágenes.
* ✅ Generación de reportes CSV locales.
* ✅ Manejo robusto de errores de API y cuotas.

### Fase 2: Persistencia y Escalabilidad (Próximamente)
* ⏳ Integración con **Supabase** para almacenamiento en base de datos.
* ⏳ Creación de un Dashboard visual para comparar precios.
* ⏳ Implementación de notificaciones automáticas de stock bajo.

## 📦 Instalación y Uso

1. **Clonar el repositorio:**
   ```bash
   git clone [https://github.com/JoshuaGarcia8/Oraculo-V.1.git](https://github.com/JoshuaGarcia8/Oraculo-V.1.git)