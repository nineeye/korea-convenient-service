import streamlit as st
import pdfplumber
import pandas as pd
import io
import re

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
                                # 1. 데이터프레임 생성
                                df = pd.DataFrame(table[1:], columns=table[0])
                                
                                # 엑셀 셀 내부의 유령 문자(제어 문자) 제거 함수
                                def remove_illegal_chars(val):
                                    if isinstance(val, str):
                                        # 엑셀 형식을 깨뜨리는 불법 제어 문자들 싹 제거
                                        return re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', val)
                                    return val
                                
                                # 데이터프레임 전체 셀에 클리닝 적용 (Pandas 버전 호환성 대응)
                                if hasattr(df, 'map'):
                                    df = df.map(remove_illegal_chars)
                                else:
                                    df = df.applymap(remove_illegal_chars)
                                
                                # 2. 안전한 시트 이름 강제 지정
                                safe_sheet_name = f"Page_{i+1}"
                                
                                # 3. 엑셀 파일에 시트 기록
                                df.to_excel(writer, sheet_name=safe_sheet_name, index=False)
                                found_table = True
                    
                    if not found_table:
                        st.error("PDF에서 表를 찾을 수 없습니다.")
                        return
                
                excel_buffer.seek(0)
                st.download_button(
                    label="엑셀 파일 다운로드",
                    data=excel_buffer,
                    file_name="converted_data.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
                st.success("🎉 성공적으로 변환되었습니다!")
                
            except Exception as e:
                st.error(f"💥 런타임 에러 발생: {str(e)}")
                import traceback
                st.code(traceback.format_exc(), language="python")
