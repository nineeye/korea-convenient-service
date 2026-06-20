import os
import google.generativeai as genai

class Saju:
    def __init__(self, name, birth_date):
        self.name = name
        self.birth_date = birth_date
        # API 키 설정
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        # 모델 이름을 최신형으로 교체!
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    def get_fortune(self):
        prompt = f"{self.name}님의 생년월일은 {self.birth_date}입니다. 이 정보를 바탕으로 오늘 하루의 운세를 사주 풀이 방식으로 아주 흥미롭고 구체적으로 설명해주세요."
        response = self.model.generate_content(prompt)
        return response.text
