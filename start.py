import os
import subprocess
import sys

print("🚀FRONTEND  START PY IS RUNNING!")
port = os.environ.get('PORT', '8150')
print(f"🔍 Starting frontend on port: {port}")

subprocess.run([
    sys.executable, '-m', 'uvicorn', 
    'app.main:app', 
    '--host', '0.0.0.0', 
    '--port', port
])