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
                
                # ExcelWriter 생성
                with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                    with pdfplumber.open(uploaded_file) as pdf:
                        for i, page in enumerate(pdf.pages):
                            table = page.extract_table()
                            if table:
                                # 데이터 프레임 생성
                                df = pd.DataFrame(table[1:], columns=table[0])
                                
                                # [핵심 해결] 시트 이름을 고정된 값으로 강제 지정하여 엑셀 규칙 준수
                                # PDF의 어떤 긴 제목이나 특수문자도 영향을 주지 않습니다.
                                sheet_name = f"Page_{i+1}"
                                
                                df.to_excel(writer, sheet_name=sheet_name, index=False)
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
                st.success("변환 완료!")
                
            except Exception as e:
                # 에러 발생 시 명확한 원인을 보여줌
                st.error(f"변환 중 오류 발생: {e}")
