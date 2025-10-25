#!/usr/bin/env python3
"""
Elas ERP - Simple Launcher (NO WAITING)
Just starts both servers and opens browser
"""
import os
import sys
import subprocess
import webbrowser
from pathlib import Path

print("\n🚀 ELAS ERP - Quick Start\n")

# Paths
ROOT = Path(__file__).parent.resolve()
PARENT = ROOT.parent
VENV_PYTHON = PARENT / ".venv" / "Scripts" / "python.exe"

if not VENV_PYTHON.exists():
    print(f"❌ Virtual environment not found at: {VENV_PYTHON}")
    print("\n🔧 Please create it first:")
    print(f"   cd {PARENT}")
    print("   python -m venv .venv")
    print("   .venv\\Scripts\\Activate.ps1")
    print("   pip install -r elas-erp\\backend\\requirements.txt")
    sys.exit(1)

PYTHON = str(VENV_PYTHON)

print(f"Root: {ROOT}")
print(f"Python: {PYTHON}\n")

# Start Backend
print("Starting backend...")
backend = subprocess.Popen(
    [PYTHON, "-m", "uvicorn", "backend.app.main:app", "--host", "127.0.0.1", "--port", "8000", "--reload"],
    cwd=str(ROOT),
    creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == 'nt' else 0
)
print(f"✓ Backend PID: {backend.pid}\n")

# Start Frontend
print("Starting frontend...")
frontend = subprocess.Popen(
    ["npm", "run", "dev", "--", "-p", "4000"],
    cwd=str(ROOT / "frontend"),
    creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == 'nt' else 0,
    shell=True
)
print(f"✓ Frontend PID: {frontend.pid}\n")

print("=" * 60)
print("✅ SERVERS STARTED!")
print("=" * 60)
print("\n📍 URLs:")
print("   Frontend: http://localhost:4000")
print("   Backend:  http://localhost:8000")
print("   API Docs: http://localhost:8000/docs\n")
print("💡 Servers are in separate windows. Check them for logs.\n")
print("Opening browser in 5 seconds...\n")

import time
time.sleep(5)
webbrowser.open("http://localhost:4000")

print("Press Ctrl+C to exit this launcher (servers will keep running)\n")

try:
    while True:
        time.sleep(10)
        if backend.poll() is not None:
            print(f"\n⚠ Backend exited with code: {backend.poll()}")
            break
        if frontend.poll() is not None:
            print(f"\n⚠ Frontend exited with code: {frontend.poll()}")
            break
except KeyboardInterrupt:
    print("\n\n✓ Launcher stopped (servers still running in their windows)\n")
