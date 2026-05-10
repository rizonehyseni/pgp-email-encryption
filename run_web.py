import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE_DIR)
sys.path.append(BASE_DIR)

from web.app import app

if __name__ == "__main__":
    print("PGP Secure Mail Web is starting...")
    print("Open in your browser: http://127.0.0.1:5000")
    app.run(debug=True, port=5000)