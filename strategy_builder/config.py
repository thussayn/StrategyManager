# -*- coding: utf-8 -*-
import os, json, glob

CONFIG_FILENAME = "config.json"

def _config_file_path(assets_dir: str) -> str:
    os.makedirs(assets_dir, exist_ok=True)
    return os.path.join(assets_dir, CONFIG_FILENAME)

def load_config(assets_dir: str) -> dict:
    path = _config_file_path(assets_dir)
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    # default empty config
    return {}

def save_config(assets_dir: str, cfg: dict) -> None:
    path = _config_file_path(assets_dir)
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(cfg, f, ensure_ascii=False, indent=2)
    except Exception:
        pass

def discover_defaults(assets_dir: str) -> dict:
    """Try to auto-detect defaults from assets folder."""
    cfg = {}
    # Bank file
    bank_candidates = [
        os.path.join(assets_dir, "بنك_الاستراتيجية v2.0.xlsx"),
    ] + glob.glob(os.path.join(assets_dir, "*.xlsx"))
    for p in bank_candidates:
        if os.path.exists(p):
            cfg["bank_filename"] = os.path.basename(p)
            break

    # Logo
    logo_candidates = [
        os.path.join(assets_dir, "Full Logo.png"),
        os.path.join(assets_dir, "uploaded_logo.png"),
    ] + glob.glob(os.path.join(assets_dir, "*.png")) + glob.glob(os.path.join(assets_dir, "*.jpg")) + glob.glob(os.path.join(assets_dir, "*.jpeg"))
    for p in logo_candidates:
        if os.path.exists(p):
            cfg["logo_filename"] = os.path.basename(p)
            break

    # Fonts
    fonts_dir = os.path.join(assets_dir, "fonts")
    fams = {
        "Amiri": ["Amiri-Regular.ttf", "Amiri.ttf"],
        "NotoNaskhArabic": ["NotoNaskhArabic-Regular.ttf", "NotoNaskhArabic.ttf"],
        "Cairo": ["Cairo-Regular.ttf", "Cairo.ttf"],
    }
    available = []
    for fam, candidates in fams.items():
        for c in candidates:
            if os.path.exists(os.path.join(fonts_dir, c)):
                available.append(fam); break
    if available:
        cfg["pdf_font_preference"] = available[0]
    # Optional specific files if present
    for cand in ["Cairo-Regular.ttf","Amiri-Regular.ttf","NotoNaskhArabic-Regular.ttf"]:
        if os.path.exists(os.path.join(fonts_dir, cand)):
            cfg.setdefault("font_regular", cand); break
    for cand in ["Cairo-Bold.ttf","Amiri-Bold.ttf","NotoNaskhArabic-Bold.ttf"]:
        if os.path.exists(os.path.join(fonts_dir, cand)):
            cfg.setdefault("font_bold", cand); break
    return cfg

def apply_to_session_state(assets_dir: str, cfg: dict, st):
    """Populate session_state keys used by export modules."""
    # Logo path
    if cfg.get("logo_filename"):
        st.session_state["_logo_path"] = os.path.join(assets_dir, cfg["logo_filename"])
    # Preferred font
    if cfg.get("pdf_font_preference"):
        st.session_state["_pdf_font_pref"] = cfg["pdf_font_preference"]
