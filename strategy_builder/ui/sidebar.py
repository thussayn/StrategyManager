# strategy_builder/ui/sidebar.py
# -*- coding: utf-8 -*-
import os
import streamlit as st
from strategy_builder.Languages.translations import get_translation
from strategy_builder.ui.styling import get_text_direction

def tr(key: str) -> str:
    """Translation helper function"""
    lang = st.session_state.get("language", "ar")
    return get_translation(lang, key)

def sidebar_controls(assets_dir: str):
    direction = get_text_direction()
    
    # تطبيق محاذاة السايدبار بناءً على الاتجاه
    st.sidebar.markdown(f"""
    <style>
    .css-1d391kg {{
        text-align: {'right' if direction == 'rtl' else 'left'};
        direction: {direction};
    }}
    </style>
    """, unsafe_allow_html=True)
    
    # Theme only
    theme_choice = st.sidebar.selectbox(tr("theme"), [tr("light"), tr("dark")], index=0)
    st.sidebar.markdown("---")
    
    # Read-only status (loaded from config into session_state by app)
    font_pref = st.session_state.get("_pdf_font_pref")
    logo_path = st.session_state.get("_logo_path")
    if font_pref:
        st.sidebar.caption(f"{tr('pdf_font')}: {font_pref}")
    if logo_path and os.path.exists(logo_path):
        st.sidebar.caption(f"{tr('logo')}: {os.path.basename(logo_path)}")
    st.sidebar.caption(tr("change_in_settings"))
    
    return theme_choice, (font_pref or "Cairo"), (logo_path if logo_path and os.path.exists(logo_path) else None)