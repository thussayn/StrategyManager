# -*- coding: utf-8 -*-
import os, shutil
import streamlit as st
from strategy_builder.config import load_config, save_config, discover_defaults, apply_to_session_state

def _fonts_dir(assets_dir: str) -> str:
    p = os.path.join(assets_dir, "fonts")
    os.makedirs(p, exist_ok=True)
    return p

def render_settings(assets_dir: str):
    st.header("⚙️ الإعدادات")

    cfg = load_config(assets_dir)
    if not cfg:
        # try to detect existing files on first run
        cfg = discover_defaults(assets_dir)
        if cfg:
            save_config(assets_dir, cfg)

    # Current status
    st.subheader("الحالة الحالية")
    st.write({
        "bank_file": cfg.get("bank_filename", "— غير محدد —"),
        "logo_file": cfg.get("logo_filename", "— غير محدد —"),
        "pdf_font_preference": cfg.get("pdf_font_preference", "— غير محدد —"),
        "font_regular": cfg.get("font_regular", "—"),
        "font_bold": cfg.get("font_bold", "—"),
    })

    st.markdown("---")
    st.subheader("📚 بنك الاستراتيجية")
    bank_upl = st.file_uploader("رفع ملف Excel للبنك", type=["xlsx"], key="bank_upl_settings")
    if bank_upl is not None:
        out_name = bank_upl.name
        out_path = os.path.join(assets_dir, out_name)
        with open(out_path, "wb") as f:
            f.write(bank_upl.read())
        cfg["bank_filename"] = out_name
        save_config(assets_dir, cfg)
        st.success(f"تم حفظ البنك: {out_name}")

    st.markdown("---")
    st.subheader("🏷️ الشعار")
    logo_upl = st.file_uploader("رفع شعار (PNG/JPG)", type=["png","jpg","jpeg"], key="logo_upl_settings")
    if logo_upl is not None:
        out_name = logo_upl.name
        out_path = os.path.join(assets_dir, out_name)
        with open(out_path, "wb") as f:
            f.write(logo_upl.read())
        cfg["logo_filename"] = out_name
        save_config(assets_dir, cfg)
        st.success(f"تم حفظ الشعار: {out_name}")

    st.markdown("---")
    st.subheader("🅰️ خطوط PDF العربية")
    fonts_dir = _fonts_dir(assets_dir)
    up_reg = st.file_uploader("رفع خط Regular (TTF)", type=["ttf"], key="font_reg_settings")
    up_bold = st.file_uploader("رفع خط Bold (TTF)", type=["ttf"], key="font_bold_settings")

    if up_reg is not None:
        out_name = up_reg.name
        with open(os.path.join(fonts_dir, out_name), "wb") as f:
            f.write(up_reg.read())
        cfg["font_regular"] = out_name
        save_config(assets_dir, cfg)
        st.success(f"تم حفظ خط Regular: {out_name}")

    if up_bold is not None:
        out_name = up_bold.name
        with open(os.path.join(fonts_dir, out_name), "wb") as f:
            f.write(up_bold.read())
        cfg["font_bold"] = out_name
        save_config(assets_dir, cfg)
        st.success(f"تم حفظ خط Bold: {out_name}")

    # Choose preferred font family
    candidates_map = {
        "Amiri": ["Amiri-Regular.ttf", "Amiri.ttf"],
        "NotoNaskhArabic": ["NotoNaskhArabic-Regular.ttf", "NotoNaskhArabic.ttf"],
        "Cairo": ["Cairo-Regular.ttf", "Cairo.ttf"],
    }
    available_fonts = []
    for fam, candidates in candidates_map.items():
        for c in candidates:
            if os.path.exists(os.path.join(fonts_dir, c)):
                available_fonts.append(fam); break
    pref = st.selectbox("اختيار العائلة المفضلة لـ PDF", options=(available_fonts or ["Amiri","NotoNaskhArabic","Cairo"]), index=0 if available_fonts else 2)
    if st.button("💾 حفظ تفضيل الخط"):
        cfg["pdf_font_preference"] = pref
        save_config(assets_dir, cfg)
        st.success(f"تم حفظ تفضيل الخط: {pref}")

    st.markdown("---")
    if st.button("تطبيق الإعدادات على الجلسة الحالية"):
        apply_to_session_state(assets_dir, cfg, st)
        st.success("تم تطبيق الإعدادات على الجلسة.")

    st.info("تُحفظ الإعدادات في ملف config.json داخل مجلد assets.")
