import streamlit as st
# webtools 폴더 내의 각 기능 모듈을 임포트합니다.
from webtools.pdf_merge import merge_pdfs
from webtools.pdf_word import convert_pdf_to_word
from webtools.pdf_image import convert_pdf_to_image

# 사이드바 메뉴 설정
st.sidebar.title("🛠 PDF 도구 모음")
menu = ["PDF 병합", "PDF → Word 변환", "PDF → 이미지 변환"]
choice = st.sidebar.selectbox("기능을 선택하세요", menu)

# 선택한 메뉴에 따라 각 기능 함수 실행
if choice == "PDF 병합":
    merge_pdfs()
elif choice == "PDF → Word 변환":
    convert_pdf_to_word()
elif choice == "PDF → 이미지 변환":
    convert_pdf_to_image()
 
