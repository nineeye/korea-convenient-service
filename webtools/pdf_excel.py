import streamlit as st
import pdfplumber
import pandas as pd
import io
import re

def convert_pdf_to_excel():
    st.subheader("🕵️‍♂️ 실시간 글자 깨짐 추적 기능이 탑재된 수학 PDF 변환기")
    st.warning("⚠️ 현재 PDF 내 수식 폰트가 깨져서 인식되는 현상이 발견되어 '실시간 유니코드 추적 모드'를 가동합니다.")
    
    uploaded_file = st.file_uploader("수학 문제지 PDF 파일을 업로드하세요", type="pdf")
    
    if uploaded_file:
        if st.button("실시간 오류 추적 및 변환 시작"):
            try:
                # 깨진 문자 분석을 위한 로그 리스트
                analysis_logs = []
                excel_buffer = io.BytesIO()
                found_text = False
                
                with pdfplumber.open(uploaded_file) as pdf:
                    st.write("### 🔍 1페이지 글자 내부 코드 실시간 분석")
                    
                    # 1페이지만 가져와서 캐릭터 레벨로 정밀 해부
                    first_page = pdf.pages[0]
                    chars = first_page.chars
                    
                    # 수식으로 추정되는 줄(문항 번호 근처)의 글자 고유 정보 파악
                    st.info("💡 파이썬이 읽은 글자의 원본 모양과 시스템 내부 번호(Hex)를 대조합니다.")
                    
                    sample_chars = chars[:100] # 상위 100개 글자 샘플링 분석
                    char_debug_df = pd.DataFrame([{
                        "텍스트(표시)": c["text"],
                        "유니코드 번호": f"U+{ord(c['text']):04X}" if len(c["text"])==1 else "N/A",
                        "폰트 이름": c.get("fontname", "Unknown"),
                        "X좌표": round(c["x0"], 1),
                        "Y좌표": round(c["top"], 1)
                    } for c in sample_chars])
                    
                    st.dataframe(char_debug_df, use_container_width=True)
                    
                # 📊 [실제 엑셀 변환 로직 시행]
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
                                    
                                    # 깨진 유니코드 문자(제어문자 및 특수영역)가 포함되어 있는지 실시간 검사
                                    cleaned_line = ""
                                    for char in line:
                                        # 수식 특수 폰트 영역(Private Use Area 등)이나 깨진 문자 감지 시 눈에 보이게 변경
                                        code_point = ord(char)
                                        if 0xE000 <= code_point <= 0xF8FF or code_point < 32:
                                            cleaned_line += f"[U+{code_point:04X}]"
                                        else:
                                            cleaned_line += char
                                    
                                    columns = re.split(r'\s{4,}', cleaned_line.strip())
                                    page_rows.append(columns)
                                
                                if page_rows:
                                    df = pd.DataFrame(page_rows)
                                    
                                    # 엑셀 에러 방지용 세이프 가드
                                    def remove_illegal_chars(val):
                                        if isinstance(val, str):
                                            return re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', val)
                                        return val
                                    df = df.map(remove_illegal_chars) if hasattr(df, 'map') else df.applymap(remove_illegal_chars)
                                    
                                    df.to_excel(writer, sheet_name=f"Page_{i+1}", index=False, header=False)
                                    found_text = True
                
                if found_text:
                    excel_buffer.seek(0)
                    st.download_button(
                        label="추적 완료된 엑셀 다운로드",
                        data=excel_buffer,
                        file_name="tracked_output.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                    st.success("🎉 분석 및 변환이 완료되었습니다! 위 표에서 유니코드 번호 규칙을 확인해 보세요.")
                else:
                    st.error("추출할 수 있는 데이터가 없습니다.")
                    
            except Exception as e:
                st.error(f"🚨 실시간 실행 중 런타임 에러 발생: {str(e)}")
                import traceback
                st.code(traceback.format_exc(), language="python")
