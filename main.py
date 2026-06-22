import streamlit as st
from webtools.pdf_merge import merge_pdfs
from webtools.pdf_word import convert_pdf_to_word
from webtools.pdf_image import convert_pdf_to_image
from webtools.pdf_security import manage_pdf_security  
from webtools.pdf_compress import compress_pdf

st.sidebar.title("🛠️ PDF 도구 모음")
# 4번 메뉴 추가
menu = ["PDF 병합", "PDF → Word 변환", "PDF → 이미지 변환", "PDF 암호 설정/해제", "PDF 용량 최적화"]
choice = st.sidebar.selectbox("기능을 선택하세요", menu)

if choice == "PDF 병합":
    merge_pdfs()
elif choice == "PDF → Word 변환":
    convert_pdf_to_word()
elif choice == "PDF → 이미지 변환":
    convert_pdf_to_image()
elif choice == "PDF 암호 설정/해제": # 추가!
    manage_pdf_security()
elif choice == "PDF 용량 최적화":
    compress_pdf()
