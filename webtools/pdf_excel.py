import streamlit as st
import pdfplumber
import pandas as pd
import io
import re

# 🔑 유니코드 매핑 테이블 (수식 복원용)
DECODE_MAP = {
    '\uE034': '1', '\uE035': '2', '\uE036': '3', '\uE037': '4',
    '\uE038': '5', '\uE039': '6', '\uE03A': '7', '\uE03B': '8',
    '\uE03C': '9', '\uE03D': '0', '\uE046': '-', '\uE048': '+'
}

def decode_math_text(text):
    if not text: return text
    for enc, dec in DECODE_MAP.items():
        text = text.replace(enc, dec)
    return text

def clean_sheet_name(name, fallback="Sheet"):
    if not name: return fallback
    name = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', str(name))
    name = re.sub(r'[\\/*?:\[\]]', '', name)
    return name.strip()[:31] if name.strip() else fallback

# ⚡ [핵심] 다운로드 시 데이터가 증발하지 않도록 메모리에 안전하게 캐싱합니다.
@st.cache_data(show_spinner="🔄 PDF에서 깨진 수식을 분석하고 엑셀 파일로 변환하는 중입니다...")
def convert_pdf_to_excel_bytes(file_bytes):
    excel_buffer = io.BytesIO()
    found_text = False
    
    with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
        # 업로드된 파일의 바이트 데이터를 읽어 pdfplumber로 전달
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            for i, page in enumerate(pdf.pages):
                text = page.extract_text(layout=True)
                if text:
                    lines = text.split('\n')
                    page_rows = []
                    detected_title = None
                    
                    for line in lines:
                        if not line.strip(): continue
                        decoded_line = decode_math_text(line)
                        
                        if not detected_title and any(k in decoded_line for k in ["학습지", "계산", "학기", "혼합", "초등학교"]):
                            detected_title = decoded_line
                        
                        columns = re.split(r'\s{4,}', decoded_line.strip())
                        page_rows.append(columns)
                    
                    if page_rows:
                        df = pd.DataFrame(page_rows)
                        remove_illegal_chars = lambda val: re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', str(val)) if isinstance(val, str) else val
                        df = df.map(remove_illegal_chars) if hasattr(df, 'map') else df.applymap(remove_illegal_chars)
                        
                        sheet_title = detected_title if detected_title else f"Page_{i+1}"
                        safe_sheet_name = clean_sheet_name(sheet_title, fallback=f"Page_{i+1}")
                        
                        df.to_excel(writer, sheet_name=safe_sheet_name, index=False, header=False)
                        found_text = True
                        
    if found_text:
        return excel_buffer.getvalue()
    return None

def main():
    st.title("🚀 수학 학습지 PDF ➡️ 엑셀 복원 변환기")
    st.write("PDF 파일을 업로드하면 자동으로 암호가 해독되어 엑셀 다운로드 버튼이 생성됩니다.")
    
    uploaded_file = st.file_uploader("수학 문제지 PDF 파일을 업로드하세요", type="pdf")
    
    if uploaded_file:
        # 1. 파일의 순수 바이트 데이터 추출
        file_bytes = uploaded_file.read()
        
        # 2. 캐싱 함수를 호출하여 엑셀 바이너리 데이터 생성
        excel_data = convert_pdf_to_excel_bytes(file_bytes)
        
        if excel_data:
            st.success("🎉 수식 해독 및 엑셀 변환 완료!")
            
            # 원본 파일명에서 확장자를 제외한 이름 추출
            clean_filename = uploaded_file.name.rsplit('.', 1)[0]
            
            # 3. 렌더링 및 다운로드 (이제 새로고침되어도 절대 데이터가 깨지거나 0byte가 되지 않습니다)
            st.download_button(
                label="✨ 복원된 엑셀 파일 다운로드",
                data=excel_data,
                file_name=f"{clean_filename}_수식복원.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.error("PDF 파일에서 텍스트를 추출하지 못했습니다. 스캔된 이미지형 PDF인지 확인해 주세요.")

if __name__ == "__main__":
    main()
