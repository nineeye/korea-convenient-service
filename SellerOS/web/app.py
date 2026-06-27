from flask import Flask, jsonify, request

app = Flask(__name__)

# 🟢 테스트용 기본 라우트
@app.route("/")
def home():
    return "Seller OS is running 🚀"

# 🟢 상태 체크 API
@app.route("/health")
def health():
    return jsonify({
        "status": "ok",
        "service": "Seller OS"
    })

# 🟢 샘플 API (나중에 AI 붙일 자리)
@app.route("/api/test", methods=["GET"])
def test_api():
    return jsonify({
        "message": "API working",
        "data": "hello seller os"
    })

# 🟢 Render용 실행 보호
if __name__ == "__main__":
    import os

    port = int(os.environ.get("PORT", 10000))

    app.run(
        host="0.0.0.0",
        port=port
    )
