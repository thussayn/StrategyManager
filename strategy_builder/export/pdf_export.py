# -*- coding: utf-8 -*-
import os
import streamlit as st
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_RIGHT, TA_CENTER
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import arabic_reshaper
from bidi.algorithm import get_display

SESSION_LOGO_KEY = "_logo_path"

def _register_arabic_fonts(assets_dir: str | None, preferred_family: str | None = None):
    fonts_dir = os.path.join(assets_dir or os.getcwd(), "fonts")
    search_order = [
        ("Amiri", ["Amiri-Regular.ttf", "Amiri.ttf"], ["Amiri-Bold.ttf"]),
        ("NotoNaskhArabic", ["NotoNaskhArabic-Regular.ttf", "NotoNaskhArabic.ttf"], ["NotoNaskhArabic-Bold.ttf"]),
        ("Cairo", ["Cairo-Regular.ttf", "Cairo.ttf"], ["Cairo-Bold.ttf"]),
    ]
    if preferred_family:
        search_order = [x for x in search_order if x[0] == preferred_family] + [x for x in search_order if x[0] != preferred_family]

    for fam, regs, bolds in search_order:
        for reg in regs:
            regp = os.path.join(fonts_dir, reg)
            if os.path.exists(regp):
                try:
                    pdfmetrics.registerFont(TTFont(fam, regp))
                    boldp = None
                    for b in bolds:
                        bp = os.path.join(fonts_dir, b)
                        if os.path.exists(bp):
                            boldp = bp; break
                    if boldp:
                        pdfmetrics.registerFont(TTFont(fam + "-Bold", boldp))
                        return fam, fam + "-Bold"
                    return fam, fam
                except Exception:
                    pass
    return None, None

def _ar(text):
    if not text:
        return ""
    try:
        return get_display(arabic_reshaper.reshape(str(text)))
    except Exception:
        return str(text)

def get_logo_path(assets_dir: str | None = None):
    p = st.session_state.get(SESSION_LOGO_KEY)
    if p and os.path.exists(p):
        return p
    if assets_dir:
        lp = os.path.join(assets_dir, "Full Logo.png")
        if os.path.exists(lp):
            return lp
    return None

def export_to_pdf(strategy: dict, assets_dir: str | None = None, preferred_family: str | None = None):
    fam, fam_bold = _register_arabic_fonts(assets_dir, preferred_family=preferred_family)
    if not fam:
        fam, fam_bold = "Helvetica", "Helvetica-Bold"
        st.warning("⚠️ لم يتم العثور على خط عربي (Amiri/NotoNaskhArabic/Cairo). الرجاء رفع ملفات الخط من الشريط الجانبي.")

    styles = getSampleStyleSheet()
    style_title = ParagraphStyle('ArabicTitle', parent=styles['Title'], fontName=fam_bold, alignment=TA_CENTER, leading=18, spaceAfter=12, wordWrap='RTL')
    style_h1 = ParagraphStyle('ArabicH1', parent=styles['Heading1'], fontName=fam_bold, alignment=TA_RIGHT, spaceBefore=14, spaceAfter=6, wordWrap='RTL')
    style_n = ParagraphStyle('ArabicN', parent=styles['Normal'], fontName=fam, alignment=TA_RIGHT, leading=16, wordWrap='RTL')

    story = []
    lp = get_logo_path(assets_dir)
    if lp and os.path.exists(lp):
        try:
            story.append(Image(lp, width=180, height=60))
            story.append(Spacer(1, 10))
        except Exception:
            pass

    story.append(Paragraph(_ar(strategy.get("name","")), style_title))
    story.append(Spacer(1, 6))
    story.append(Paragraph(_ar("الرؤية:"), style_h1))
    story.append(Paragraph(_ar(strategy.get('vision','') or ""), style_n))
    story.append(Paragraph(_ar("الرسالة:"), style_h1))
    story.append(Paragraph(_ar(strategy.get('message','') or ""), style_n))
    story.append(Paragraph(_ar("الأهداف:"), style_h1))
    for g in strategy.get("goals", []):
        story.append(Paragraph(_ar("• " + str(g)), style_n))
    story.append(Paragraph(_ar("القيم:"), style_h1))
    for v in strategy.get("values", []):
        story.append(Paragraph(_ar("• " + str(v)), style_n))

    fname = f"strategy_{strategy.get('id','')}.pdf"
    out_path = os.path.join(os.getcwd(), fname)
    doc = SimpleDocTemplate(out_path, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    doc.build(story)
    return out_path
