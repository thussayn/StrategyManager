# -*- coding: utf-8 -*-
import os
import streamlit as st

SESSION_LOGO_KEY = "_logo_path"

def sidebar_controls(assets_dir: str):
    # Theme only
    theme_choice = st.sidebar.selectbox("🎨 السمة", ["فاتح","داكن"], index=0)
    st.sidebar.markdown("---")
    # Read-only status (loaded from config into session_state by app)
    font_pref = st.session_state.get("_pdf_font_pref")
    logo_path = st.session_state.get(SESSION_LOGO_KEY)
    if font_pref:
        st.sidebar.caption(f"خط PDF: {font_pref}")
    if logo_path and os.path.exists(logo_path):
        st.sidebar.caption(f"الشعار: {os.path.basename(logo_path)}")
    st.sidebar.caption("للتغيير: انتقل إلى ⚙️ الإعدادات من القائمة.")
    return theme_choice, (font_pref or "Cairo"), (logo_path if logo_path and os.path.exists(logo_path) else None)
