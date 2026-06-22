import streamlit as st
import pdfplumber
import pandas as pd
import io
import re

def clean_sheet_name(name):
    # 1. 시트 이름에서 허용되지 않는 문자 제거
    name = re.sub(r'[:\\/?*\[\]]', '', name)
    # 2. 31자까지만 자르기
    return name[:31]

def convert_pdf_to_excel():
    st.subheader("📊 PDF → Excel 변환")
    uploaded_file = st.file_uploader("표가 포함된 PDF 파일을 업로드하세요", type="pdf")
    
    if uploaded_file:
        if st.button("변환 시작"):
            try:
                excel_buffer = io.BytesIO()
                found_table = False
                
                with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                    with pdfplumber.open(uploaded_file) as pdf:
                        for i, page in enumerate(pdf.pages):
                            table = page.extract_table()
                            if table:
                                df = pd.DataFrame(table[1:], columns=table[0])
                                # 시트 이름을 안전하게 정제
                                sheet_name = clean_sheet_name(f"Page_{i+1}")
                                df.to_excel(writer, sheet_name=sheet_name, index=False)
                                found_table = True
                    
                    if not found_table:
                        st.error("PDF에서 표를 찾을 수 없습니다.")
                        return
                
                excel_buffer.seek(0)
                st.download_button("엑셀 파일 다운로드", excel_buffer, "converted_data.xlsx")
                st.success("변환 완료!")
            except Exception as e:
                st.error(f"변환 중 오류 발생: {e}")
