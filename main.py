import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from ssaju import Saju

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def get_index():
    return """
    <html>
        <body>
            <h1>사주 서비스</h1>
            <form action="/fortune" method="get">
                이름: <input type="text" name="name"><br>
                생년월일(YYYY-MM-DD): <input type="text" name="birth_date"><br>
                <input type="submit" value="운세 확인">
            </form>
        </body>
    </html>
    """

@app.get("/fortune")
def get_fortune(name: str, birth_date: str):
    saju_helper = Saju(name=name, birth_date=birth_date)
    result = saju_helper.get_fortune()
    return HTMLResponse(content=f"<h1>{name}님의 운세</h1><p>{result}</p><a href='/'>다시 하기</a>")
