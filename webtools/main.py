import streamlit as st

# 1. 각 도구 모듈 임포트 (파일 경로가 정확해야 합니다)
# 예를 들어 webtools 폴더 안에 pdf_word.py, pdf_image.py, pdf_merge.py가 있다고 가정합니다.
from webtools.pdf_merge import merge_pdfs
# from webtools.pdf_word import convert_pdf_to_word  # 필요시 추가
# from webtools.pdf_image import convert_pdf_to_image # 필요시 추가

# 2. 사이드바 메뉴 설정
st.sidebar.title("🛠 PDF 도구 모음")
menu = ["PDF 병합", "PDF → Word 변환", "PDF → 이미지 변환"]
choice = st.sidebar.selectbox("기능을 선택하세요", menu)

# 3. 선택한 메뉴에 따라 기능 호출
if choice == "PDF 병합":
    merge_pdfs()
elif choice == "PDF → Word 변환":
    st.write("PDF → Word 변환 기능 준비 중...")
    # convert_pdf_to_word()
elif choice == "PDF → 이미지 변환":
    st.write("PDF → 이미지 변환 기능 준비 중...")
    # convert_pdf_to_image()
