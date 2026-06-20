import os
import google.generativeai as genai
from fastapi import FastAPI
from pydantic import BaseModel
from ssaju import Saju
from fastapi.middleware.cors import CORSMiddleware

# 1. 웹 서버 초기화
app = FastAPI()

# HTML 화면(프론트엔드)과 통신하기 위한 보안 설정 열기
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. 사용자가 입력할 데이터 구조 정의
class UserInfo(BaseModel):
    name: str
    gender: str
    year: int
    month: int
    day: int

# 3. 사주 분석 및 AI 글쓰기 메인 로직
@app.post("/get_fortune")
async def get_fortune(user: UserInfo):
    try:
        # 환경변수에서 API 키 불러오기 (보안)
        GOOGLE_API_KEY = os.environ.get("GEMINI_API_KEY")
        genai.configure(api_key=GOOGLE_API_KEY)

        # ssaju로 사주 원국 계산 (시간은 점심 12시로 기본 고정)
        saju = Saju(user.year, user.month, user.day, 12, gender=user.gender)
        pillars = saju.get_four_pillars()
        
        # 앞서 완성한 BizShot AI 스토리텔링 프롬프트
        prompt = f"""
        [역할(Role)]
        당신은 사람들의 마음을 따뜻하게 어루만져주는 지혜롭고 다정다감한 인생 멘토이자 명리학 전문가입니다. 딱딱한 사주 용어를 쓰지 않고, 마치 동네에서 가장 믿음직하고 따뜻한 언니/오빠처럼 정감 가는 말투로 이야기합니다.

        [입력 데이터]
        - 사용자 이름: {user.name}
        - 사주 원국 데이터: {pillars}

        [작성 지침: 3단 스토리텔링 구조]
        1. 공감과 위로 (과거~현재)
        사주 데이터의 특징을 바탕으로, {user.name}님이 그동안 돈이나 인간관계, 혹은 삶의 무게 때문에 남몰래 겪었을 고충을 따뜻하게 짚어주며 위로를 건냅니다.

        2. 희망과 반전 (숨겨진 재물운)
        사주 데이터에서 긍정적인 재물운의 요소를 찾아내어 희망을 줍니다. 앞으로 어떤 부분에서 재물운이 터질지, 어떤 강점을 살려야 하는지 구체적이고 확신에 찬 어조로 이야기합니다.

        3. 다정한 응원과 조언 (마무리)
        재물운을 온전히 내 것으로 만들기 위해 일상에서 실천할 수 있는 작은 마음가짐이나 습관을 조언해줍니다. 어떤 대가나 상품 추천 없이, 오직 {user.name}님의 행복과 성장을 진심으로 응원하며 마무리합니다.

        [제한 사항]
        - 절대 특정 상품 판매, 결제 유도, 혹은 타 사이트 이동을 권유하는 상업적인 멘트를 넣지 말 것.
        - 분량: 모바일 화면에서 읽기 좋게 4~5개의 짧은 문단으로 구성할 것.
        - 톤앤매너: 친근한 존댓말(해요체), 부드럽고 다정한 어조. 
        - 부정적인 단어(망한다, 나쁘다, 흉하다)는 절대 사용 금지.
        """
        
        # 구글 무료 AI 호출
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        
        return {"result": response.text}
        
    except Exception as e:
        return {"result": f"앗, 에너지를 읽는 중 오류가 발생했어요. 잠시 후 다시 시도해주세요. ({str(e)})"}




from fastapi import FastAPI
from ssaju import Saju  # 우리가 만든 파일

app = FastAPI()

# 메인 페이지에 접속했을 때 나올 내용
@app.get("/")
def read_root():
    return {"message": "반갑습니다! 사주 서비스에 오신 것을 환영합니다."}

# 사주 결과 보기 예시 경로
@app.get("/fortune/{name}")
def get_user_fortune(name: str):
    saju_data = Saju(name=name, birth_date="2026-06-20")
    return {"result": saju_data.get_fortune()}

