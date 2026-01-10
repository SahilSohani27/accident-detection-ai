import subprocess
import sys
import threading
import os

def run_backend():
    backend_dir = os.path.join(os.path.dirname(__file__), "backend")
    subprocess.run([sys.executable, "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"], cwd=backend_dir)

def run_dashboard():
    dashboard_dir = os.path.join(os.path.dirname(__file__), "dashboard")
    subprocess.run([sys.executable, "-m", "streamlit", "run", "dashboard.py"], cwd=dashboard_dir)

if __name__ == "__main__":
    t1 = threading.Thread(target=run_backend)
    t1.start()

    t2 = threading.Thread(target=run_dashboard)
    t2.start()

    t1.join()
    t2.join()
