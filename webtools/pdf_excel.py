import streamlit as st
import pdfplumber
import pandas as pd
import io
import re

def convert_pdf_to_excel():
    st.subheader("📊 수학 문제지 PDF → Excel 변환")
    st.info("💡 테두리 선이 없는 시험지/학습지 형식의 PDF에서 문항을 좌/우 열로 정렬하여 추출합니다.")
    
    uploaded_file = st.file_uploader("PDF 파일을 업로드하세요", type="pdf")
    
    if uploaded_file:
        if st.button("변환 시작"):
            try:
                excel_buffer = io.BytesIO()
                found_text = False
                
                with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                    with pdfplumber.open(uploaded_file) as pdf:
                        for i, page in enumerate(pdf.pages):
                            # 🔥 핵심: layout=True를 주면 눈에 보이는 좌/우 공백 간격이 그대로 유지됩니다.
                            text = page.extract_text(layout=True)
                            
                            if text:
                                lines = text.split('\n')
                                page_rows = []
                                
                                for line in lines:
                                    if not line.strip():
                                        continue
                                    
                                    # 3칸 이상의 연속된 공백을 기준으로 왼쪽 문제와 오른쪽 문제를 분리합니다.
                                    columns = re.split(r'\s{3,}', line.strip())
                                    page_rows.append(columns)
                                
                                if page_rows:
                                    # 데이터프레임 생성 (행마다 칸 수가 달라도 자동으로 채워집니다)
                                    df = pd.DataFrame(page_rows)
                                    
                                    # 엑셀 제어 문자 제거 함수
                                    def remove_illegal_chars(val):
                                        if isinstance(val, str):
                                            return re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', val)
                                        return val
                                    
                                    # 데이터 정제
                                    df = df.map(remove_illegal_chars) if hasattr(df, 'map') else df.applymap(remove_illegal_chars)
                                    
                                    # 안전한 시트 이름 지정
                                    safe_sheet_name = f"Page_{i+1}"
                                    
                                    # 문제지 형식이므로 엑셀 맨 위 제목 열(Header) 없이 그대로 기록합니다.
                                    df.to_excel(writer, sheet_name=safe_sheet_name, index=False, header=False)
                                    found_text = True
                    
                    if not found_text:
                        st.error("PDF에서 추출할 수 있는 텍스트를 찾지 못했습니다.")
                        return
                
                excel_buffer.seek(0)
                st.download_button(
                    label="엑셀 파일 다운로드",
                    data=excel_buffer,
                    file_name="extracted_questions.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
                st.success("🎉 성공적으로 모든 문항이 추출되었습니다!")
                
            except Exception as e:
                st.error(f"💥 런타임 에러 발생: {str(e)}")
                import traceback
                st.code(traceback.format_exc(), language="python")
