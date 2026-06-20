import os
import google.generativeai as genai

class Saju:
    def __init__(self, name, birth_date):
        self.name = name
        self.birth_date = birth_date
        # 환경변수에서 키를 가져와 설정합니다.
        genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
        # 가장 안정적인 모델로 설정합니다.
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    def get_fortune(self):
        try:
            prompt = f"{self.name}님의 생년월일은 {self.birth_date}입니다. 오늘 운세를 다정하게 말해주세요."
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"오류 발생: {str(e)}"
