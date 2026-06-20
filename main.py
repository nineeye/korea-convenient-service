import os
import google.generativeai as genai
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from ssaju import Saju
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 환경변수 설정
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

@app.get("/", response_class=HTMLResponse)
def get_index():
    return """
    <html>
        <body>
            <h1>사주 서비스</h1>
            <form action="/fortune" method="post">
                이름: <input type="text" name="name"><br>
                생년월일(YYYY-MM-DD): <input type="text" name="birth_date"><br>
                <input type="submit" value="운세 확인">
            </form>
        </body>
    </html>
    """

@app.post("/fortune", response_class=HTMLResponse)
async def get_fortune(name: str = Form(...), birth_date: str = Form(...)):
    try:
        # 사주 객체 생성 및 AI 호출
        saju_helper = Saju(name=name, birth_date=birth_date)
        result = saju_helper.get_fortune()
        
        return HTMLResponse(content=f"<h1>{name}님의 운세</h1><p>{result.replace(chr(10), '<br>')}</p><a href='/'>다시 하기</a>")
    except Exception as e:
        return HTMLResponse(content=f"<h1>오류 발생</h1><p>{str(e)}</p><a href='/'>다시 하기</a>")
