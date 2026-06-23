import streamlit as st
import io

from pypdf import PdfReader, PdfWriter

from reportlab.pdfgen import canvas

def add_watermark():
    st.title("2단계 성공")
