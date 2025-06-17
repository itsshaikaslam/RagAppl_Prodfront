'''import os
import subprocess
import sys

print("🚀 FRONTEND START.PY IS RUNNING!")

# Get port from environment, default to 8150
port = os.environ.get('PORT', '8150')
print(f"🔍 Starting frontend on port: {port}")

# Path to your Streamlit app
app_path = os.path.join('frontend', 'app.py')

# Run Streamlit
subprocess.run([
    sys.executable, '-m', 'streamlit', 'run',
    app_path,
    '--server.address', '0.0.0.0',
    '--server.port', str(port)
])'''
