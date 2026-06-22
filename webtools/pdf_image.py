import streamlit as st
from pdf2image import convert_from_bytes
import io
import zipfile

def convert_pdf_to_image():
    st.subheader("PDF → 이미지 변환기")
    uploaded_file = st.file_uploader("변환할 PDF 파일을 선택하세요", type=['pdf'])
    
    if uploaded_file is not None:
        if st.button("변환 시작"):
            images = convert_from_bytes(uploaded_file.read())
            
            # 여러 페이지인 경우 zip으로 묶어서 다운로드
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, "w") as zf:
                for i, image in enumerate(images):
                    img_byte_arr = io.BytesIO()
                    image.save(img_byte_arr, format='JPEG')
                    zf.writestr(f"page_{i+1}.jpg", img_byte_arr.getvalue())
            
            st.download_button(
                label="이미지 파일들(ZIP) 다운로드",
                data=zip_buffer.getvalue(),
                file_name="converted_images.zip",
                mime="application/zip"
            )
            st.success("변환 완료!")
