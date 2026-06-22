import streamlit as st
import pdfplumber
import pandas as pd
import io

def convert_pdf_to_excel():
    st.subheader("📊 PDF → Excel 변환")
    
    # 🔵 [테스트 포인트 1] 이 파란색 박스가 화면에 나타나야 "진짜 최신 코드"가 반영된 것입니다!
    st.info("🔍 [시스템 상태] 실시간 오류 추적 디버깅 모드가 활성화되었습니다.")
    
    uploaded_file = st.file_uploader("표가 포함된 PDF 파일을 업로드하세요", type="pdf")
    
    if uploaded_file:
        # 🔵 [테스트 포인트 2] 스트림릿 서버가 인식한 파일명을 실시간으로 화면에 출력
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
                                
                                # 💡 강제로 영문 안전 시트명 설정
                                sheet_name = f"Page_{i+1}"
                                
                                # 🔵 [테스트 포인트 3] 엑셀 라이브러리에 넘기기 직전의 시트 이름을 주황색 박스로 화면에 강제 중계
                                st.warning(f"⚙️ [실시간 추적] {i+1}번째 시트 이름을 다음으로 입력 시도합니다 ➡️ `{sheet_name}`")
                                
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
                # 에러 발생 시 원인을 아주 상세하게 화면에 출력
                st.error(f"💥 [오류 포착 지점]: {str(e)}")
                st.info("💡 Tip: 만약 에러 창에 여전히 '초등학교...' 한글 문구가 나온다면, 깃허브 저장 버튼은 누르셨으나 스트림릿 서버가 아직 새 코드를 불러오지 못하고 옛날 코드를 붙잡고 있는 상태(배포 지연)인 것을 의미합니다.")
