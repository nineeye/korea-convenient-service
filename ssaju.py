import os
import google.generativeai as genai

class Saju:
    def __init__(self, name, birth_date):
        self.name = name
        self.birth_date = birth_date
        # 환경변수에서 API 키 가져오기
        api_key = os.getenv("GEMINI_API_KEY")
        genai.configure(api_key=api_key)
        # 모델 이름을 변경하여 호출 (pro 버전이 더 안정적일 수 있습니다)
        self.model = genai.GenerativeModel("gemini-pro")

    def get_fortune(self):
        try:
            prompt = f"{self.name}님의 생년월일은 {self.birth_date}입니다. 오늘 운세를 다정하게 사주 풀이 형식으로 알려주세요."
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"오류 발생: {str(e)}"
