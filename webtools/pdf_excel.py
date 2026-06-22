import streamlit as st
import pdfplumber
import pandas as pd
import io

def convert_pdf_to_excel():
    st.subheader("📊 PDF → Excel 변환")
    
    st.info("🔍 [시스템 상태] 실시간 오류 추적 디버깅 모드가 활성화되었습니다.")
    
    uploaded_file = st.file_uploader("표가 포함된 PDF 파일을 업로드하세요", type="pdf")
    
    if uploaded_file:
        st.write(f"📁 현재 서버가 읽은 파일명: `{uploaded_file.name}`")
        
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
                                
                                # 🟢 1. 안전한 영문 시트명 생성
                                safe_sheet_name = f"Page_{i+1}"
                                
                                # 🟢 2. 화면에 시도하는 이름 중계
                                st.warning(f"⚙️ [실시간 추적] {i+1}번째 시트 이름을 다음으로 입력 시도합니다 ➡️ {safe_sheet_name}")
                                
                                # 🟢 3. [★가장 중요★] 생성한 safe_sheet_name 변수를 엑셀 시트명으로 정확히 매칭!
                                df.to_excel(writer, sheet_name=safe_sheet_name, index=False)
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
                # 에러 발생 시 원인을 아주 상세하게 화면에 출력
                st.error(f"💥 에러 발생 원인: {str(e)}")
