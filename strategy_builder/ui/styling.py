# -*- coding: utf-8 -*-
import streamlit as st

def apply_base_styles():
    st.markdown(
        '''<style>
@import url("https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700;800&display=swap");
:root { --bg:#ffffff; --text:#0f172a; --card:#ffffff; --muted:#f3f4f6; --primary:#e11d48; --border:#e5e7eb; }
html, body, [data-testid="stAppViewContainer"], .block-container {direction: rtl; text-align: right; font-family: "Cairo", sans-serif !important;}
[data-testid="stSidebar"] {direction: rtl; text-align: right;}
[data-testid="stMarkdownContainer"] {direction: rtl; text-align: right;}
.stTextInput>label, .stSelectbox>label, .stMultiSelect>label, .stTextArea>label {text-align: right; display: block;}
[data-testid="stAppViewContainer"]{ background: var(--bg); color: var(--text); }
.block-container{ color: var(--text); }
.stButton>button { background: var(--primary) !important; color: #fff !important; border: none; border-radius: 12px; padding: .55rem 1rem; }
textarea, input, .stTextInput input { color: var(--text) !important; }
.css-1r6slb0, .css-1d391kg, .stSelectbox, .stMultiSelect, .stTextInput, .stTextArea { background: var(--card) !important; }
</style>''', unsafe_allow_html=True
    )

def apply_theme_choice(choice: str):
    if choice == "فاتح":
        st.markdown('''<style>
:root { --bg:#f8fafc; --text:#0f172a; --card:#ffffff; --muted:#f3f4f6; --primary:#dc2626; --border:#e5e7eb; }
</style>''', unsafe_allow_html=True)
    else:
        st.markdown('''<style>
:root { --bg:#0b1220; --text:#e5e7eb; --card:#111827; --muted:#0f172a; --primary:#fb7185; --border:#1f2937; }
</style>''', unsafe_allow_html=True)
