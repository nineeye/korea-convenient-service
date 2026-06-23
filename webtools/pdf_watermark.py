import streamlit as st
import io

from pypdf import PdfReader, PdfWriter

from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from PIL import Image
from reportlab.lib.utils import ImageReader

def add_watermark():
    st.title("5단계 성공")
