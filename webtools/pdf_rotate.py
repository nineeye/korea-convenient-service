import streamlit as st
from pypdf import PdfReader, PdfWriter
import io

def rotate_pdf():
    st.subheader("🔄 PDF 특정 페이지 회전")
    uploaded_file = st.file_uploader("PDF 파일을 업로드하세요", type="pdf")
    
    if uploaded_file:
        reader = PdfReader(uploaded_file)
        num_pages = len(reader.pages)
        
        page_num = st.number_input(f"회전할 페이지 번호 (1 ~ {num_pages})", min_value=1, max_value=num_pages, value=1)
        # 시계 방향임을 명시적으로 표시
        angle = st.selectbox("회전 각도 (시계 방향)", [90, 180, 270])
        
        if st.button("회전 실행"):
            writer = PdfWriter()
            
            for i, page in enumerate(reader.pages):
                if i == page_num - 1:
                    # 선택한 각도만큼 시계 방향으로 회전
                    page.rotate(angle)
                writer.add_page(page)
            
            output = io.BytesIO()
            writer.write(output)
            output.seek(0)
            
            st.download_button("수정된 PDF 다운로드", output, "rotated_page.pdf")
            st.success(f"{page_num}페이지가 시계 방향으로 {angle}도 회전되었습니다!")
