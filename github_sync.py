#!/usr/bin/env python3
"""
🌌 TAKUMIRA GITHUB SYNC V2.1 - FIXED & BULLETPROOF
Script de sincronización inteligente a prueba de errores TOTAL
Compatible Windows/Linux/Mac | Auto-detección rama | Config Git automática
"""

import os
import subprocess
import sys
import datetime
import shutil
from pathlib import Path

def ejecutar_git(comando, cwd=None):
    """Ejecuta comando git con manejo robusto de errores (Windows/Linux)"""
    try:
        resultado = subprocess.run(
            comando, 
            shell=True, 
            cwd=cwd, 
            capture_output=True, 
            text=True, 
            check=True,
            timeout=30
        )
        return True, resultado.stdout.strip()
    except subprocess.TimeoutExpired:
        return False, "⏰ TIMEOUT: Comando tardó demasiado"
    except subprocess.CalledProcessError as e:
        return False, e.stderr.strip() if e.stderr else str(e)

def verificar_git_config():
    """🔍 Verifica y configura user.name/user.email si faltan"""
    print("🔐 Verificando configuración Git...")
    
    # Chequear user.name
    ok, name = ejecutar_git("git config user.name")
    if not ok or not name:
        print("⚠️  FALTA 'user.name' - Configurando...")
        nombre = input("📝 Ingresa tu nombre (ej: Joshua Garcia): ").strip()
        ejecutar_git(f'git config user.name "{nombre}"')
        print(f"✅ user.name = {nombre}")
    
    # Chequear user.email
    ok, email = ejecutar_git("git config user.email")
    if not ok or not email:
        print("⚠️  FALTA 'user.email' - Configurando...")
        email = input("📧 Ingresa tu email (ej: joshua@email.com): ").strip()
        ejecutar_git(f'git config user.email "{email}"')
        print(f"✅ user.email = {email}")
    
    print("✅ Git configurado correctamente ✓")

def detectar_rama_principal():
    """🧠 Detecta automáticamente main/master"""
    print("🔍 Detectando rama principal...")
    
    # 1. Rama actual
    ok, rama_actual = ejecutar_git("git branch --show-current")
    if ok and rama_actual:
        print(f"✅ Rama actual: {rama_actual}")
        return rama_actual
    
    # 2. Revisar remotes
    ok, remotes = ejecutar_git("git remote show origin")
    if ok:
        if "HEAD branch: main" in remotes:
            return "main"
        if "HEAD branch: master" in remotes:
            return "master"
    
    # 3. Default moderno
    ok, default = ejecutar_git("git config init.defaultBranch")
    if ok and "main" in default:
        print("✅ Usando 'main' (GitHub default)")
        return "main"
    
    print("✅ Usando 'master'")
    return "master"

def configurar_remote_si_falta(repo_url):
    """🔗 Configura remote origin si no existe - FIX BUG"""
    print("🔗 Verificando remote origin...")
    
    # ✅ FIX: Lógica corregida
    ok, salida = ejecutar_git("git remote -v")
    
    # Verificar si origin existe en la salida
    if ok and "origin" in salida:
        print("✅ Remote 'origin' ya configurado")
        return True
    else:
        print(f"🔗 Creando remote: {repo_url}")
        resultado, error = ejecutar_git(f'git remote add origin {repo_url}')
        if resultado:
            print("✅ Remote creado exitosamente")
            return True
        else:
            print(f"❌ Error remote: {error}")
            return False

def takumira_sync(repo_url="https://github.com/JoshuaGarcia8/Oraculo-V.1.git"):
    """
    🌟 SINCRONIZACIÓN TAKUMIRA ENTERPRISE V2.1
    """
    print("\n" + "="*60)
    print("🧿🔥  ORÁCULO V.1 - TAKUMIRA GITHUB SYNC v2.1 (FIXED)  🔥🧿")
    print("="*60)
    
    proyecto_dir = Path.cwd()
    print(f"📂 Directorio: {proyecto_dir}")
    
    # 1. GIT INSTALADO?
    if not shutil.which("git"):
        print("❌❌ GIT NO ENCONTRADO")
        print("💡 Windows: https://git-scm.com/download/windows")
        print("💡 Instala y reinicia terminal")
        input("Presiona Enter...")
        return False
    
    print("✅ Git detectado ✓")
    
    # 2. CONFIG GIT IDENTITY
    verificar_git_config()
    
    # 3. INIT SI NO EXISTE
    if not os.path.exists(".git"):
        print("\n📂 Inicializando repositorio Git...")
        ok, _ = ejecutar_git("git init")
        if not ok:
            print("❌ Error git init")
            return False
        print("✅ Repositorio creado")
    
    # 4. CONFIGURAR REMOTE
    if not configurar_remote_si_falta(repo_url):
        return False
    
    # 5. GIT ADD
    print("\n📦 Empaquetando archivos (respetando .gitignore)...")
    ok, _ = ejecutar_git("git add .")
    print("✅ Archivos preparados")
    
    # 6. COMMIT INTELIGENTE
    timestamp = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    mensaje = f"✨ Sync Oráculo V.1 - {timestamp} (Takumira v2.1)"
    
    print(f"\n🌀 Commit: {mensaje}")
    ok, error = ejecutar_git(f'git commit -m "{mensaje}"')
    
    if not ok:
        error_lower = error.lower()
        if any(frase in error_lower for frase in ["nothing to commit", "no changes added"]):
            print("🌟 ✨ ¡El Oráculo ya está PERFECTO! No hay cambios nuevos ✨ 🌟")
        else:
            print(f"💥 ERROR COMMIT:\n{error}")
            print("\n🔧 DEBUG:")
            debug, _ = ejecutar_git("git status")
            print(f"   Status: {debug[:200]}...")
            return False
    else:
        print("✅ COMMIT EXITOSO ✓")
    
    # 7. PUSH INTELIGENTE
    rama = detectar_rama_principal()
    print(f"\n🚀 PUSH a rama '{rama}'...")
    
    # Push directo
    ok, error = ejecutar_git(f"git push origin {rama}")
    if not ok:
        print("🔄 Primer push detectado, configurando upstream...")
        ok, error = ejecutar_git(f"git push -u origin {rama}")
        if not ok:
            print(f"💥 ERROR PUSH:\n{error}")
            print("\n🔧 SOLUCIONES RÁPIDAS:")
            print("   1. git pull origin main --allow-unrelated-histories")
            print("   2. https://github.com/settings/tokens (Personal Access Token)")
            print("   3. git config --global credential.helper store")
            return False
    
    print("✅ PUSH EXITOSO ✓")
    
    # 8. ¡TRIUMFO ÉPICO!
    print("\n" + "🌌"*25)
    print("🎉🎊 ¡HITO HISTÓRICO, JOSHUA GARCÍA! 🎊🎉")
    print("🔥🔥 ORÁCULO V.1 ETERNAMENTE EN LA NUBE 🔥🔥")
    print(f"🌐 {repo_url}")
    print(f"📁 Rama activa: {rama}")
    print("✨ Takumira Sync v2.1: 100% BULLETPROOF ✨")
    print("🌌"*25)
    
    return True

if __name__ == "__main__":
    REPO_URL = "https://github.com/JoshuaGarcia8/Oraculo-V.1.git"
    
    success = takumira_sync(REPO_URL)
    
    print("\n" + "="*50)
    if success:
        print("🎊 ¡EJECUCIÓN PERFECTA! 🎊")
        print("💾 Tu código está seguro en GitHub")
        input("\nPresiona Enter para celebrar... 🎉")
        sys.exit(0)
    else:
        print("💥 Sync interrumpido - Revisa errores arriba")
        input("\nPresiona Enter para salir...")
        sys.exit(1)