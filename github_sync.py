import os
import subprocess
import sys
from datetime import datetime

def ejecutar_git(comando):
    """Ejecuta un comando de consola y devuelve si fue exitoso."""
    try:
        # shell=True es necesario en Windows para comandos como 'git'
        resultado = subprocess.run(comando, shell=True, check=True, capture_output=True, text=True)
        return True, resultado.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr

def sincronizar():
    print("\n🧿 === INICIANDO SINCRONIZACIÓN TAKUMIRA ===")
    
    # 1. Tu URL de GitHub (La que me pasaste)
    REPO_URL = "https://github.com/JoshuaGarcia8/Oraculo-V.1.git"

    # 2. Verificar si Git está inicializado, si no, lo hace
    if not os.path.exists(".git"):
        print("📂 Inicializando repositorio local...")
        ejecutar_git("git init")
        ejecutar_git(f"git remote add origin {REPO_URL}")
        print("✅ Repositorio vinculado correctamente.")

    # 3. Preparar los archivos (git add)
    print("📦 Empaquetando archivos (respetando .gitignore)...")
    ejecutar_git("git add .")

    # 4. Crear el sello de tiempo (Commit)
    fecha_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    mensaje = f"Sync Oráculo V.1 - {fecha_hora}"
    
    ok, error = ejecutar_git(f'git commit -m "{mensaje}"')
    if not ok:
        if "nothing to commit" in error:
            print("✨ El Oráculo ya está al día. No hay cambios nuevos.")
        else:
            print(f"❌ Error en el commit: {error}")
        return

    # 5. Subir a la nube (Push)
    print("🚀 Elevando código a GitHub...")
    # Usamos -u origin main para asegurar que se suba a la rama principal
    # La primera vez puede pedirte login en el navegador
    ok, error = ejecutar_git("git push -u origin main")
    
    if ok:
        print("\n" + "="*40)
        print("🎉 ¡HITO ALCANZADO, JOSHUA!")
        print(f"✨ Tu proyecto 'Oráculo V.1' ya está en la nube.")
        print(f"🔗 Link: {REPO_URL}")
        print("="*40)
    else:
        # A veces la rama se llama 'master' en lugar de 'main', por seguridad:
        if "src refspec main does not match" in error:
            print("🔄 Reintentando con rama 'master'...")
            ejecutar_git("git push -u origin master")
        else:
            print(f"❌ Error al subir: {error}")

if __name__ == "__main__":
    sincronizar()