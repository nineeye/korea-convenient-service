import streamlit as st
from pypdf import PdfReader, PdfWriter
import io

def rotate_pdf():
    st.subheader("🔄 PDF 특정 페이지 회전 (다중 선택 가능)")
    uploaded_file = st.file_uploader("PDF 파일을 업로드하세요", type="pdf")
    
    if uploaded_file:
        reader = PdfReader(uploaded_file)
        num_pages = len(reader.pages)
        
        # 쉼표로 페이지 번호를 입력받음
        page_input = st.text_input(f"회전할 페이지 번호를 쉼표로 구분하여 입력하세요 (예: 1, 3, 5) (1 ~ {num_pages})")
        angle = st.selectbox("회전 각도 (시계 방향)", [90, 180, 270])
        
        if st.button("회전 실행"):
            try:
                # 입력값 파싱 및 유효성 검사
                target_pages = [int(p.strip()) - 1 for p in page_input.split(',')]
                
                # 범위 체크
                if any(p < 0 or p >= num_pages for p in target_pages):
                    st.error(f"입력하신 페이지 중 범위를 벗어난 번호가 있습니다. (1 ~ {num_pages} 사이로 입력하세요)")
                    return

                writer = PdfWriter()
                for i, page in enumerate(reader.pages):
                    if i in target_pages:
                        page.rotate(angle)
                    writer.add_page(page)
                
                output = io.BytesIO()
                writer.write(output)
                output.seek(0)
                
                st.download_button("수정된 PDF 다운로드", output, "rotated_pages.pdf")
                st.success(f"{page_input} 페이지가 시계 방향으로 {angle}도 회전되었습니다!")

            except ValueError:
                # 숫자가 아닌 값이 입력되었을 때 안내 메시지
                st.error("잘못된 입력입니다. 페이지 번호는 숫자와 쉼표(,)만 사용하여 입력해 주세요. (예: 1, 2, 4)")
