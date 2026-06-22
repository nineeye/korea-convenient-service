import streamlit as st
from pypdf import PdfReader, PdfWriter
import io

def rotate_pdf():
    st.subheader("🔄 PDF 페이지 회전")
    uploaded_file = st.file_uploader("회전할 PDF 파일을 업로드하세요", type="pdf")
    
    if uploaded_file:
        angle = st.selectbox("회전 각도를 선택하세요", [90, 180, 270])
        if st.button("회전 시작"):
            reader = PdfReader(uploaded_file)
            writer = PdfWriter()
            
            for page in reader.pages:
                page.rotate(angle)
                writer.add_page(page)
            
            output = io.BytesIO()
            writer.write(output)
            output.seek(0)
            
            st.download_button("회전된 PDF 다운로드", output, "rotated.pdf")
            st.success(f"{angle}도 회전 완료!")
