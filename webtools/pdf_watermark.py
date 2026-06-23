import streamlit as st
import io

from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter


def create_watermark(text):

    packet = io.BytesIO()

    c = canvas.Canvas(packet, pagesize=letter)

    c.setFont("Helvetica", 40)

    c.saveState()

    c.translate(300, 400)

    c.rotate(45)

    c.drawCentredString(0, 0, text)

    c.restoreState()

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

    watermark_text = st.text_input(
        "워터마크 문구",
        value="CONFIDENTIAL"
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
