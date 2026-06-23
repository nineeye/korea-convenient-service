import streamlit as st
import io

from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


def create_watermark(text):

    packet = io.BytesIO()

    pdfmetrics.registerFont(
        TTFont("Nanum", "fonts/NanumGothic.ttf")
    )

    c = canvas.Canvas(packet)

    # 연한 회색
    c.setFillGray(0.75)

    # 한글 폰트
    c.setFont("Nanum", 12)

    # 하단 우측에 출력
    c.drawRightString(
        560,
        20,
        text
    )

    c.save()

    packet.seek(0)

    return PdfReader(packet)

def add_watermark():

    st.title("💧 PDF 워터마크 추가")

    uploaded_file = st.file_uploader(
        "PDF 업로드",
        type=["pdf"]
    )

    if uploaded_file is None:
        return

    position = st.selectbox(
    "워터마크 위치",
    [
        "하단 우측",
        "상단 우측",
        "하단 좌측",
        "상단 좌측"
    ]
)

    watermark_text = st.text_input(
        "워터마크 문구",
        value="CONFIDENTIAL"
    )

    font_size = st.slider(
        "글자 크기",
        8,
        30,
        10
    )
    
    gray_level = st.slider(
        "투명도",
        0.3,
        0.9,
        0.65
    )
    
    if st.button("워터마크 적용"):

        try:

            reader = PdfReader(uploaded_file)

            watermark_pdf = create_watermark(watermark_text)

            watermark_page = watermark_pdf.pages[0]

            writer = PdfWriter()

            for page in reader.pages:

                page.merge_page(watermark_page)

                writer.add_page(page)

            output = io.BytesIO()

            writer.write(output)

            output.seek(0)

            st.success("완료!")

            st.download_button(
                "📥 워터마크 PDF 다운로드",
                output,
                file_name="watermarked.pdf",
                mime="application/pdf"
            )

        except Exception as e:
            st.error(str(e))
