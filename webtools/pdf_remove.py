import streamlit as st
from pypdf import PdfReader, PdfWriter
import io

def remove_pages():
    st.subheader("✂️ PDF 특정 페이지 삭제")
    uploaded_file = st.file_uploader("PDF 파일을 업로드하세요", type="pdf")
    
    if uploaded_file:
        reader = PdfReader(uploaded_file)
        num_pages = len(reader.pages)
        page_input = st.text_input(f"삭제할 페이지 번호를 입력하세요 (예: 1, 3-5) (1 ~ {num_pages})")
        
        if st.button("삭제 실행"):
            try:
                # 삭제할 페이지 번호 리스트 만들기
                remove_list = []
                for part in page_input.split(','):
                    if '-' in part:
                        start, end = map(int, part.split('-'))
                        remove_list.extend(range(start - 1, end))
                    else:
                        remove_list.append(int(part.strip()) - 1)
                
                writer = PdfWriter()
                for i, page in enumerate(reader.pages):
                    if i not in remove_list: # 삭제 대상이 아닌 페이지만 추가
                        writer.add_page(page)
                
                output = io.BytesIO()
                writer.write(output)
                output.seek(0)
                
                st.download_button("수정된 PDF 다운로드", output, "removed_pages.pdf")
                st.success("해당 페이지가 삭제되었습니다!")
            except:
                st.error("입력 형식이 잘못되었습니다. (예: 1, 3-5)")
