import streamlit as st
import io

from pypdf import PdfReader, PdfWriter

from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


# 워터마크 생성
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

    # 회색 정도
    c.setFillGray(gray_level)

    # 한글 폰트
    c.setFont(
        "Nanum",
        font_size
    )

    # 우측 하단
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

    c.rotate(
        45
    )

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


# 메인 함수
def add_watermark():

    st.title("💧 PDF 워터마크 추가")

    uploaded_file = st.file_uploader(
        "PDF 파일 업로드",
        type=["pdf"]
    )

    if uploaded_file is None:
        return

    logo_file = st.file_uploader(
    "로고 이미지(PNG)",
    type=["png"]
)

    watermark_mode = st.radio(
    "워터마크 유형",
    [
        "텍스트",
        "로고"
    ]
)
    watermark_text = st.text_input(
        "워터마크 문구",
        value="상업적 이용 불가"
    )

    col1, col2 = st.columns([1, 2])

    with col1:

        font_size = st.slider(
            "글자 크기",
            min_value=8,
            max_value=40,
            value=10
        )

        gray_level = st.slider(
            "투명도",
            min_value=0.1,
            max_value=0.95,
            value=0.65,
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

            watermark_pdf = create_watermark(
                watermark_text,
                font_size,
                gray_level,
                watermark_type
            )

            watermark_page = watermark_pdf.pages[0]

            writer = PdfWriter()

            for page in reader.pages:

                page.merge_page(watermark_page)

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
