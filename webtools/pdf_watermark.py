import streamlit as st
import io

from pypdf import PdfReader, PdfWriter

from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image
from reportlab.lib.utils import ImageReader


def create_watermark(
    text,
    font_size,
    gray_level,
    watermark_type
):

    packet = io.BytesIO()

    pdfmetrics.registerFont(
        TTFont(
            "Nanum",
            "fonts/NanumGothic.ttf"
        )
    )

    c = canvas.Canvas(packet)

    c.setFillGray(gray_level)
    c.setFont("Nanum", font_size)

    if watermark_type == "하단 우측":

        c.drawRightString(
            560,
            20,
            text
        )

    elif watermark_type == "상단 우측":

        c.drawRightString(
            560,
            800,
            text
        )

    elif watermark_type == "하단 좌측":

        c.drawString(
            20,
            20,
            text
        )

    elif watermark_type == "상단 좌측":

        c.drawString(
            20,
            800,
            text
        )

    elif watermark_type == "중앙":

        c.drawCentredString(
            300,
            400,
            text
        )

    elif watermark_type == "대각선":

        c.saveState()

        c.translate(
            300,
            400
        )

        c.rotate(45)

        c.drawCentredString(
            0,
            0,
            text
        )

        c.restoreState()

    elif watermark_type == "반복":

        c.saveState()

        c.rotate(35)

        for x in range(-200, 900, 250):

            for y in range(-200, 900, 180):

                c.drawString(
                    x,
                    y,
                    text
                )

        c.restoreState()

    c.save()

    packet.seek(0)

    return PdfReader(packet)


def add_watermark():

    st.title("💧 PDF 워터마크 추가")

    uploaded_file = st.file_uploader(
        "PDF 파일 업로드",
        type=["pdf"]
    )

    if uploaded_file is None:
        return

    watermark_mode = st.radio(
    "워터마크 종류",
    [
        "텍스트",
        "로고"
    ]
)

    if watermark_mode == "텍스트":

    watermark_text = st.text_input(
        "워터마크 문구",
        value="상업적 이용 불가"
    )

    else:

    logo_file = st.file_uploader(
        "회사 로고 PNG 업로드",
        type=["png"]
    )

    if logo_file:

        st.image(
            logo_file,
            caption="로고 미리보기",
            width=200
        )

    watermark_type = st.selectbox(
    "위치",
    [
        "하단 우측",
        "상단 우측",
        "하단 좌측",
        "상단 좌측",
        "중앙"
    ]
)

    col1, col2 = st.columns([1, 2])

    with col1:

        if watermark_mode == "로고":

    logo_size = st.slider(
        "로고 크기",
        30,
        300,
        100
    )

        gray_level = st.slider(
            "회색 정도",
            0.1,
            0.95,
            0.65,
            step=0.05
        )

    with col2:

        preview_opacity = 1 - gray_level

        st.markdown(
            f"""
            <div style="
                border:1px solid #cccccc;
                border-radius:8px;
                padding:20px;
                height:120px;
                position:relative;
                background:#fafafa;
            ">
                <div style="
                    position:absolute;
                    right:15px;
                    bottom:10px;
                    font-size:{font_size}px;
                    color:rgba(0,0,0,{preview_opacity});
                ">
                    {watermark_text}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.caption("실제 적용될 워터마크 미리보기")

    st.divider()

    if st.button("💧 워터마크 적용"):

        try:

            reader = PdfReader(uploaded_file)

            if watermark_mode == "텍스트":

    watermark_pdf = create_watermark(
        watermark_text,
        font_size,
        gray_level,
        watermark_type
    )

else:

    if logo_file is None:

        st.error("로고 PNG를 업로드해주세요.")
        return

    watermark_pdf = create_logo_watermark(
        logo_file,
        logo_size,
        watermark_type
    )
            def create_logo_watermark(
    logo_file,
    size,
    position
):

    packet = io.BytesIO()

    c = canvas.Canvas(packet)

    logo = Image.open(logo_file)

    if position == "하단 우측":

        x = 470
        y = 20

    elif position == "상단 우측":

        x = 470
        y = 700

    elif position == "하단 좌측":

        x = 20
        y = 20

    elif position == "상단 좌측":

        x = 20
        y = 700

    else:

        x = 250
        y = 350

    c.drawImage(
        ImageReader(logo),
        x,
        y,
        width=size,
        height=size,
        mask="auto"
    )

    c.save()

    packet.seek(0)

    return PdfReader(packet)

            watermark_page = watermark_pdf.pages[0]

            writer = PdfWriter()

            for page in reader.pages:

                page.merge_page(
                    watermark_page
                )

                writer.add_page(page)

            output = io.BytesIO()

            writer.write(output)

            output.seek(0)

            st.success("워터마크 적용 완료!")

            st.download_button(
                "📥 워터마크 PDF 다운로드",
                data=output,
                file_name="watermarked.pdf",
                mime="application/pdf"
            )

        except Exception as e:

            st.error(
                f"오류 발생: {str(e)}"
            )
