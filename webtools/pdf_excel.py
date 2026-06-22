import streamlit as st
import pdfplumber
import pandas as pd
import io
import re

# 🔑 유니코드 매핑 테이블
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

def convert_pdf_to_excel():
    st.subheader("🚀 수식 암호 복원 기능 탑재 변환기 (안정화 버전)")
    
    # 💾 [핵심] 다운로드할 파일 데이터를 저장할 세션 상태 초기화
    if 'excel_data' not in st.session_state:
        st.session_state['excel_data'] = None
    if 'file_name' not in st.session_state:
        st.session_state['file_name'] = ""

    uploaded_file = st.file_uploader("수학 문제지 PDF 파일을 업로드하세요", type="pdf")
    
    if uploaded_file:
        # 새 파일이 업로드되면 기존에 변환된 데이터는 초기화
        if st.session_state['file_name'] != uploaded_file.name:
            st.session_state['excel_data'] = None
            st.session_state['file_name'] = uploaded_file.name

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
                    # 💾 [핵심] 변환된 파일 바이너리를 세션 상태에 안전하게 기록
                    st.session_state['excel_data'] = excel_buffer.getvalue()
                    st.success("🎉 변환이 완료되었습니다! 아래 다운로드 버튼을 눌러주세요.")
                else:
                    st.error("PDF에서 추출할 수 있는 텍스트를 찾지 못했습니다.")
                    
            except Exception as e:
                st.error(f"🚨 오류 발생: {str(e)}")

        # 🎯 [핵심] 변환 버튼 외부에서 세션 데이터를 확인하여 다운로드 버튼을 렌더링 (0byte 방지)
        if st.session_state['excel_data'] is not None:
            st.write("---")
            st.download_button(
                label="✨ 복원된 엑셀 파일 다운로드",
                data=st.session_state['excel_data'],
                file_name="math_questions_restored.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

if __name__ == "__main__":
    convert_pdf_to_excel()
