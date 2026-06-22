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
                                df = pd.DataFrame(table[1:], columns=table[0])
                                
                                # [강제 고정] 절대 PDF 제목을 쓰지 않고 무조건 'Page_1' 형식 사용
                                sheet_name = f"Page_{i+1}"
                                
                                # 💡 실시간 확인용 디버깅 메세지 (화면에 강제로 찍어봅니다)
                                st.info(f"⚙️ [디버깅] 현재 설정하려는 시트 이름은 무조건 문자가 고정됩니다: {sheet_name}")
                                
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
                # 에러 추적을 위해 문구를 완전히 새로 변경했습니다.
                st.error(f"💥 [최종 추적] 에러가 발생한 지점의 메시지: {str(e)}")
