import streamlit as st
from pdf2docx import Converter
import os

st.set_page_config(page_title="Professional PDF to Word", layout="centered")

st.markdown("""
# 📄 Professional PDF Converter
고품질 PDF -> Word 변환 서비스입니다.
""")

uploaded_file = st.file_uploader("PDF 파일을 업로드하세요.", type=["pdf"])

if uploaded_file:
    if st.button("변환 시작하기"):
        with st.spinner("변환 중입니다. 잠시만 기다려주세요..."):
            try:
                # 파일 저장 및 변환
                pdf_path = "input.pdf"
                docx_path = "output.docx"
                with open(pdf_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                cv = Converter(pdf_path)
                cv.convert(docx_path, start=0, end=None)
                cv.close()
                
                with open(docx_path, "rb") as f:
                    st.download_button("결과물 다운로드", f, "result.docx")
                st.success("완벽하게 변환되었습니다!")
                
            except Exception as e:
                st.error("변환 과정에서 오류가 발생했습니다. 파일을 다시 확인해주세요.")
