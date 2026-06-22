import streamlit as st
import pdfplumber
import pandas as pd
import io
import os

def convert_pdf_to_excel():
    st.subheader("📊 PDF → Excel 변환 (심층 디버깅 모드)")
    
    # 🔥 [심층 추적 1] 현재 서버가 '진짜로' 실행하고 있는 파일의 소스코드를 화면에 강제 출력
    st.markdown("### 📝 [코드 추적] 현재 서버에서 실행 중인 실제 코드 확인")
    try:
        current_file_path = __file__
        with open(current_file_path, "r", encoding="utf-8") as f:
            raw_code = f.read()
        
        # 소스코드 중 to_excel이 적힌 핵심 라인 주변부만 딱 잘라서 보여주기
        st.info(f"📍 실행 중인 파일 경로: `{current_file_path}`")
        with st.expander("👀 여기를 눌러 서버의 진짜 코드를 확인하세요 (to_excel 검색용)"):
            st.code(raw_code, language="python")
    except Exception as e:
        st.error(f"코드 추적 실패: {e}")

    # --- 기존 변환 로직 ---
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
                                
                                # 변수 할당
                                safe_sheet_name = f"Page_{i+1}"
                                
                                # 🔥 [심층 추적 2] repr()를 사용해 숨겨진 공백이나 데이터 타입까지 완벽 추적
                                st.warning(f"🔍 [변수 추적] safe_sheet_name의 실제 값: {repr(safe_sheet_name)} (Type: {type(safe_sheet_name)})")
                                
                                # 실행 직전 강제 매칭
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
                # 🔥 [심층 추적 3] 에러 발생 시 시스템 내부 스택트레이스를 더 상세히 출력
                st.error(f"💥 런타임 에러 발생: {str(e)}")
                import traceback
                st.code(traceback.format_exc(), language="python")
