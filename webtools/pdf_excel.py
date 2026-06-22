import streamlit as st
import pdfplumber
import pandas as pd
import io

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
                                # 💡 [핵심 수정] 첫 줄 텍스트를 컬럼명(columns=...)으로 지정하지 않고,
                                # 표 전체를 순수한 '셀 데이터'로 가져옵니다.
                                df = pd.DataFrame(table)
                                
                                # 시트 이름은 가장 안전한 고정 문자열 사용
                                sheet_name = f"Page_{i+1}"
                                
                                # header=False를 추가하여 컬럼명 검증 오류를 완전히 우회합니다.
                                df.to_excel(writer, sheet_name=sheet_name, header=False, index=False)
                                found_table = True
                    
                    if not found_table:
                        st.error("PDF에서 표를 찾을 수 없습니다.")
                        return
                
                excel_buffer.seek(0)
                st.download_button(
                    label="엑셀 파일 다운로드",
                    data=excel_buffer,
                    file_name="converted_data.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
                st.success("변환 완료! 이제 다운로드 버튼을 눌러주세요.")
                
            except Exception as e:
                st.error(f"💥 변환 오류: {str(e)}")
