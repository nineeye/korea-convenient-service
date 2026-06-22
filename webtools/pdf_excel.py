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
                
                # 1. 엑셀 파일 작성자 오픈
                with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                    # 2. PDF 파일 오픈
                    with pdfplumber.open(uploaded_file) as pdf:
                        for i, page in enumerate(pdf.pages):
                            table = page.extract_table()
                            if table:
                                # PDF에서 추출한 데이터를 데이터프레임으로 변환
                                df = pd.DataFrame(table[1:], columns=table[0])
                                
                                # ✨ [핵심 수정] 시트 이름을 안전하게 Page_1, Page_2 형태로 강제 고정
                                sheet_name = f"Page_{i+1}"
                                
                                # 엑셀 파일에 시트 기록
                                df.to_excel(writer, sheet_name=sheet_name, index=False)
                                found_table = True
                    
                    if not found_table:
                        st.error("PDF에서 표를 찾을 수 없습니다.")
                        return
                
                # 3. 다운로드 버튼 생성
                excel_buffer.seek(0)
                st.download_button(
                    label="엑셀 파일 다운로드",
                    data=excel_buffer,
                    file_name="converted_data.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
                st.success("🎉 변환 완료! 다운로드 버튼을 눌러주세요.")
                
            except Exception as e:
                # 에러 발생 시 명확하게 메시지 출력
                st.error(f"💥 변경 중 오류 발생: {str(e)}")
