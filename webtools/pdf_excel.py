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
                # 엑셀 저장을 위한 버퍼
                excel_buffer = io.BytesIO()
                # 표를 찾았는지 확인하기 위한 변수
                found_table = False
                
                with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                    with pdfplumber.open(uploaded_file) as pdf:
                        for i, page in enumerate(pdf.pages):
                            table = page.extract_table()
                            if table:
                                # 데이터 프레임 생성
                                df = pd.DataFrame(table[1:], columns=table[0])
                                df.to_excel(writer, sheet_name=f'Page_{i+1}', index=False)
                                found_table = True
                    
                    # 표가 없으면 오류 메시지 처리를 위해 강제로 빈 시트 제거/체크
                    if not found_table:
                        st.error("PDF에서 표를 찾을 수 없습니다. (이미지 형태의 PDF인가요?)")
                        return
                
                excel_buffer.seek(0)
                st.download_button(
                    label="엑셀 파일 다운로드",
                    data=excel_buffer,
                    file_name="converted_data.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
                st.success("변환 완료! 엑셀 파일을 다운로드하세요.")
            except Exception as e:
                st.error(f"변환 중 오류 발생: {e}")
