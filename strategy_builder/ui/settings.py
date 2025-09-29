# strategy_builder/ui/settings.py
# -*- coding: utf-8 -*-
import os
import streamlit as st
from strategy_builder.config import load_config, save_config
from strategy_builder.Languages.translations import get_translation, get_available_languages

def tr(key: str) -> str:
    """Translation helper function"""
    lang = st.session_state.get("language", "ar")
    return get_translation(lang, key)

def render_settings(assets_dir: str):
    st.header("⚙️ " + tr("settings"))
    
    # تحميل الإعدادات الحالية
    cfg = load_config(assets_dir)
    
    # قسم إعدادات اللغة
    st.subheader("🌐 " + tr("language_settings"))
    
    available_langs = get_available_languages()
    current_lang = st.session_state.get("language", cfg.get("language", "ar"))
    
    # Language selector مع أعلام
    lang_display = {
        "ar": "🇸🇦 العربية",
        "en": "🇺🇸 English"
    }
    
    selected_lang = st.selectbox(
        tr("choose_language"),
        options=list(available_langs.keys()),
        format_func=lambda x: lang_display[x],
        index=list(available_langs.keys()).index(current_lang) if current_lang in available_langs else 0,
        key="language_settings_selector"
    )
    
    # رسالة توضيحية عن الـ sidebar
    if selected_lang != current_lang:
        st.warning("🔄 **ملاحظة:** لتطبيق تغيير مكان الشريط الجانبي، يرجى إعادة تشغيل التطبيق")

    # تحديث اللغة إذا تغيرت
    if selected_lang != st.session_state.get("language"):
        st.session_state.language = selected_lang
        cfg["language"] = selected_lang
        save_config(assets_dir, cfg)
        st.success(tr("language_updated"))
        st.rerun()
    
    st.markdown("---")
    
    # باقي إعدادات المظهر (الموجودة حالياً)
    st.subheader("🎨 " + tr("appearance_settings"))
    
    # Theme settings
    theme_options = [tr("light"), tr("dark")]
    current_theme = cfg.get("theme", tr("light"))
    theme_index = theme_options.index(current_theme) if current_theme in theme_options else 0
    theme_choice = st.selectbox(tr("theme"), theme_options, index=theme_index)
    cfg["theme"] = theme_choice
    
    # Logo upload
    st.markdown("### 🖼️ " + tr("upload_logo"))
    uploaded_logo = st.file_uploader(tr("browse_files"), type=['png', 'jpg', 'jpeg'], key="logo_upload")
    if uploaded_logo is not None:
        logo_path = os.path.join(assets_dir, "uploaded_logo.png")
        with open(logo_path, "wb") as f:
            f.write(uploaded_logo.getbuffer())
        cfg["logo_filename"] = "uploaded_logo.png"
        st.success(tr("logo_upload_success"))
    
    st.markdown("---")
    
    # إعدادات التصدير
    st.subheader("📤 " + tr("export_settings"))
    
    # Font selection for PDF
    fonts_dir = os.path.join(assets_dir, "fonts")
    available_fonts = []
    if os.path.exists(fonts_dir):
        font_files = os.listdir(fonts_dir)
        if "Cairo-Regular.ttf" in font_files:
            available_fonts.append("Cairo")
        if "Amiri-Regular.ttf" in font_files:
            available_fonts.append("Amiri")
        if "NotoNaskhArabic-Regular.ttf" in font_files:
            available_fonts.append("NotoNaskhArabic")
    
    if available_fonts:
        current_font = cfg.get("pdf_font_preference", available_fonts[0])
        font_choice = st.selectbox(tr("select_font"), available_fonts, 
                                 index=available_fonts.index(current_font) if current_font in available_fonts else 0)
        cfg["pdf_font_preference"] = font_choice
    else:
        st.warning(tr("no_fonts_available"))
    
    st.markdown("---")
    
    # Bank file upload
    st.subheader("📊 " + tr("upload_bank"))
    uploaded_bank = st.file_uploader(tr("browse_files") + " (Excel)", type=['xlsx'], key="bank_upload")
    if uploaded_bank is not None:
        bank_path = os.path.join(assets_dir, uploaded_bank.name)
        with open(bank_path, "wb") as f:
            f.write(uploaded_bank.getbuffer())
        cfg["bank_filename"] = uploaded_bank.name
        st.success(tr("bank_upload_success"))
    
    # حفظ كل الإعدادات
    if st.button("💾 " + tr("save_settings")):
        save_config(assets_dir, cfg)
        st.success(tr("settings_saved"))
        
        # تحديث session state
        if cfg.get("logo_filename"):
            st.session_state["_logo_path"] = os.path.join(assets_dir, cfg["logo_filename"])
        if cfg.get("pdf_font_preference"):
            st.session_state["_pdf_font_pref"] = cfg["pdf_font_preference"]
        if cfg.get("language"):
            st.session_state["language"] = cfg["language"]
        
        st.rerun()