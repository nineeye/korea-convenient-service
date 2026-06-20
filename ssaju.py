# ssaju.py

class Saju:
    def __init__(self, name, birth_date):
        self.name = name
        self.birth_date = birth_date

    def get_fortune(self):
        # 여기에 나중에 AI 연동 코드가 들어갈 자리입니다.
        return f"{self.name}님의 {self.birth_date} 사주 결과: 오늘은 아주 좋은 날입니다!"

# 만약 다른 기능이 더 필요하다면 아래에 함수를 추가하세요.

import random

class Saju:
    def __init__(self, name, birth_date):
        self.name = name
        self.birth_date = birth_date

    def get_fortune(self):
        fortunes = ["대박 날 거예요!", "오늘은 조심하세요.", "평범한 하루가 될 거예요.", "귀인을 만날 운입니다."]
        return f"{self.name}님의 사주 결과: {random.choice(fortunes)}"
