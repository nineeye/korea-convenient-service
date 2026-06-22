import streamlit as st
import pdfplumber
import pandas as pd
import io
import re

# 🔑 실시간 추적으로 밝혀낸 유니코드 비밀번호 매핑 테이블
DECODE_MAP = {
    '\uE034': '1',
    '\uE035': '2',
    '\uE036': '3',
    '\uE037': '4',
    '\uE038': '5',
    '\uE039': '6',
    '\uE03A': '7',
    '\uE03B': '8',
    '\uE03C': '9',
    '\uE03D': '0',
    '\uE046': '-',
    '\uE048': '+'
}

def decode_math_text(text):
    """깨진 특수 수식 폰트 문자를 실제 숫자와 기호로 치환하는 함수"""
    if not text:
        return text
    for enc, dec in DECODE_MAP.items():
        text = text.replace(enc, dec)
    return text

def convert_pdf_to_excel():
    st.subheader("🚀 수식 암호 복원 기능 탑재 완전판 변환기")
    st.success("🎯 폰트 깨짐 암호 해독 완료! 이제 깨진 수식이 실제 연산 기호와 숫자로 자동 치환됩니다.")
    
    uploaded_file = st.file_uploader("수학 문제지 PDF 파일을 업로드하세요", type="pdf")
    
    if uploaded_file:
        if st.button("엑셀 변환 및 수식 복원 시작"):
            try:
                excel_buffer = io.BytesIO()
                found_text = False
                
                with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                    with pdfplumber.open(uploaded_file) as pdf:
                        for i, page in enumerate(pdf.pages):
                            text = page.extract_text(layout=True)
                            
                            if text:
                                lines = text.split('\n')
                                page_rows = []
                                
                                for line in lines:
                                    if not line.strip():
                                        continue
                                    
                                    # 1. 한글 특수 수식 코드를 실제 수식문자(숫자, +, -)로 변환
                                    decoded_line = decode_math_text(line)
                                    
                                    # 2. 다단 분리 규칙 적용 (연속된 공백 4칸 이상)
                                    columns = re.split(r'\s{4,}', decoded_line.strip())
                                    page_rows.append(columns)
                                
                                if page_rows:
                                    df = pd.DataFrame(page_rows)
                                    
                                    # 엑셀 에러 유발 문자 세이프 가드
                                    def remove_illegal_chars(val):
                                        if isinstance(val, str):
                                            return re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', val)
                                        return val
                                    df = df.map(remove_illegal_chars) if hasattr(df, 'map') else df.applymap(remove_illegal_chars)
                                    
                                    df.to_excel(writer, sheet_name=f"Page_{i+1}", index=False, header=False)
                                    found_text = True
                    
                    if found_text:
                        excel_buffer.seek(0)
                        st.download_button(
                            label="✨ 복원된 엑셀 파일 다운로드",
                            data=excel_buffer,
                            file_name="math_questions_restored.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )
                        st.success("🎉 수식 복원 및 변환이 완료되었습니다! 엑셀을 다운로드해 보세요.")
                    else:
                        st.error("PDF에서 추출할 수 있는 텍스트를 찾지 못했습니다.")
                        
            except Exception as e:
                st.error(f"🚨 오류 발생: {str(e)}")
