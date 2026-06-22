import streamlit as st
import pdfplumber
import pandas as pd
import io
import re

def convert_pdf_to_excel():
    st.subheader("📊 수학 문제지 PDF → Excel 변환 (정밀 분석 버전)")
    st.info("💡 문항 번호는 가져왔으나 수식이 빠지는 현상을 해결하기 위해 원본 추출 상태를 함께 점검합니다.")
    
    uploaded_file = st.file_uploader("PDF 파일을 업로드하세요", type="pdf")
    
    if uploaded_file:
        if st.button("변환 시작"):
            try:
                excel_buffer = io.BytesIO()
                found_text = False
                
                # 🔍 [진단 단계] 파이썬이 PDF에서 글자를 아예 읽을 수 있는지 확인합니다.
                with pdfplumber.open(uploaded_file) as pdf:
                    first_page_text = pdf.pages[0].extract_text()
                    st.write("### 👁️ 파이썬이 실제로 읽어낸 1페이지 텍스트 데이터")
                    if first_page_text:
                        st.text_area(
                            label="아래 상자 안에 '22 + 5 - 22' 같은 수식이 보이나요? 안 보인다면 PDF 자체의 인코딩 문제입니다.",
                            value=first_page_text,
                            height=250
                        )
                    else:
                        st.warning("⚠️ 1페이지에서 글자를 전혀 읽어내지 못했습니다. 이미지형 PDF일 가능성이 큽니다.")

                # 📊 [변환 및 저장 단계]
                with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                    with pdfplumber.open(uploaded_file) as pdf:
                        for i, page in enumerate(pdf.pages):
                            text = page.extract_text(layout=True)
                            
                            if text:
                                lines = text.split('\n')
                                page_rows = []
                                
                                for line in lines:
                                    if not line.strip():
                                        continue
                                    
                                    # 혹시 수식 안의 띄어쓰기 때문에 쪼개졌을 가능성을 방지하기 위해
                                    # 열 분리 기준을 '연속된 공백 4칸 이상'으로 조금 더 넓혔습니다.
                                    columns = re.split(r'\s{4,}', line.strip())
                                    page_rows.append(columns)
                                
                                if page_rows:
                                    df = pd.DataFrame(page_rows)
                                    
                                    # 엑셀 제어 문자 제거
                                    def remove_illegal_chars(val):
                                        if isinstance(val, str):
                                            return re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', val)
                                        return val
                                    
                                    df = df.map(remove_illegal_chars) if hasattr(df, 'map') else df.applymap(remove_illegal_chars)
                                    
                                    safe_sheet_name = f"Page_{i+1}"
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
                st.success("🎉 변환 및 데이터 진단이 완료되었습니다!")
                
            except Exception as e:
                st.error(f"💥 에러 발생: {str(e)}")
                import traceback
                st.code(traceback.format_exc(), language="python")
