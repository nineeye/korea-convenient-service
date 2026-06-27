import os
import sys

BASE_DIR = os.path.dirname(__file__)
sys.path.append(BASE_DIR)  # ⭐ seller를 루트로 인식

from web.app import app

if __name__ == "__main__":
    print("🚀 Seller System Starting...")
    app.run(debug=True, host="0.0.0.0", port=5000)
