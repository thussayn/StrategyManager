# app.py
# -*- coding: utf-8 -*-
import os
import datetime
import streamlit as st

from strategy_builder.ui.styling import apply_base_styles, apply_theme_choice, apply_direction_styles
from strategy_builder.ui.sidebar import sidebar_controls
from strategy_builder.ui.wizard import run_wizard
from strategy_builder.ui.settings import render_settings
from strategy_builder.data.db import init_db, list_strategies, get_strategy, delete_strategy, clone_strategy
from strategy_builder.data.progress import load_progress, save_progress
from strategy_builder.data.excel_bank import load_bank, build_relations
from strategy_builder.export.word_export import export_to_word
from strategy_builder.export.pdf_export import export_to_pdf
from strategy_builder.config import load_config, save_config, discover_defaults, apply_to_session_state
from strategy_builder.Languages.translations import get_translation, get_available_languages

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "strategy_builder", "assets")
DEFAULT_BANK_PATH = os.path.join(ASSETS_DIR, "بنك_الاستراتيجية v2.0.xlsx")

def tr(key: str) -> str:
    """Translation helper function"""
    lang = st.session_state.get("language", "ar")
    return get_translation(lang, key)

def main():
    # تحميل الإعدادات أولاً لتحديد اللغة
    cfg = load_config(ASSETS_DIR)
    if not cfg:
        cfg = discover_defaults(ASSETS_DIR)
        if cfg:
            save_config(ASSETS_DIR, cfg)
    
    # تحديد اتجاه الصفحة بناءً على اللغة
    current_lang = cfg.get("language", "ar")
    initial_sidebar_state = "expanded"
    
    # إعداد الصفحة مع اتجاه sidebar صحيح
    st.set_page_config(
        page_title=tr("app_title"), 
        layout="wide",
        initial_sidebar_state=initial_sidebar_state
    )
    
    # الآن تطبيق الأنماط
    apply_base_styles()
    apply_direction_styles()

    # Ensure DB exists
    _ = init_db()

    # تطبيق الإعدادات على session state
    apply_to_session_state(ASSETS_DIR, cfg, st)
    
    # Initialize language in session state
    if "language" not in st.session_state:
        st.session_state.language = current_lang

    # Sidebar UI (theme + status)
    theme_choice, preferred_font, logo_p = sidebar_controls(ASSETS_DIR)
    apply_theme_choice(theme_choice)

    # Header (logo + title) - عكس الأعمدة بناءً على اللغة
    lang = st.session_state.get("language", "ar")
    if lang == "ar":
        col_t, col_l = st.columns([8, 2])  # الصورة على اليمين
    else:
        col_l, col_t = st.columns([2, 8])  # الصورة على اليسار
        
    with col_l:
        if logo_p and os.path.exists(logo_p):
            st.image(logo_p, use_container_width=True)
    with col_t:
        st.title(tr("app_title"))
        if cfg.get("logo_filename"):
            st.caption(f"{tr('current_logo')} {cfg.get('logo_filename')}")
        if cfg.get("pdf_font_preference"):
            st.caption(f"{tr('preferred_font')} {cfg.get('pdf_font_preference')}")

    # ---- Navigation ----
    st.sidebar.header(tr("choose_option"))
    options = [
        tr("new_strategy"),
        tr("browse_strategies"), 
        tr("resume_session"),
        tr("settings")
    ]

    if "pending_nav" in st.session_state:
        st.session_state["nav_radio"] = st.session_state["pending_nav"]
        del st.session_state["pending_nav"]

    mode = st.sidebar.radio(tr("choose_option"), options, key="nav_radio")

    # Open settings page early
    if mode == tr("settings"):
        render_settings(ASSETS_DIR)
        return

    # Load bank (must exist for other modes)
    bank_path = None
    if cfg.get('bank_filename'):
        possible = os.path.join(ASSETS_DIR, cfg['bank_filename'])
        if os.path.exists(possible):
            bank_path = possible
            st.info(f"{tr('using_bank')} **{os.path.basename(bank_path)}**")
    if not bank_path and os.path.exists(DEFAULT_BANK_PATH):
        bank_path = DEFAULT_BANK_PATH
        st.info(f"{tr('using_bank')} **{os.path.basename(bank_path)}**")
    if not bank_path:
        st.warning(tr("bank_not_found"))
        return

    df = load_bank(bank_path)
    visions, vision_to_msgs, msg_to_goals, msg_to_values, all_goals, all_values = build_relations(df)

    # ---- Modes ----
    if mode == tr("resume_session"):
        prog = load_progress()
        if not prog:
            st.info(tr("no_saved_session"))
            return
        s = get_strategy(prog.get("strategy_id", -1))
        if not s:
            st.warning(tr("strategy_not_found"))
            return

        # Preload to session_state
        st.session_state.strategy_id = s["id"]
        st.session_state.name = s["name"]
        st.session_state.vision = s["vision"]
        st.session_state.message = s["message"]
        st.session_state.goals = s["goals"]
        st.session_state["values"] = s["values"]
        st.session_state.step = int(prog.get("step", 1))

        run_wizard(visions, vision_to_msgs, msg_to_goals, msg_to_values, all_goals, all_values, preferred_font)
        return

    if mode == tr("new_strategy"):
        action_options = [tr("create_new"), tr("load_existing")]

        # ✅ لو في جلسة تعديل، نخلي الافتراضي "تحميل استراتيجية محفوظة للتعديل"
        if "force_edit_mode" in st.session_state and st.session_state["force_edit_mode"]:
            default_action = tr("load_existing")
        else:
            default_action = action_options[0]

        action = st.radio(
            tr("choose_action"),
            action_options,
            index=action_options.index(default_action),
            horizontal=True
        )

        # 👇 لو المستخدم غيّر يدويًا إلى "إنشاء"، نلغي وضع التعديل
        if action == tr("create_new") and "force_edit_mode" in st.session_state:
            st.session_state["force_edit_mode"] = False

        if action == tr("create_new"):
            # Reset once
            if st.session_state.get("_new_init_done") is not True:
                for k in ["strategy_id", "name", "vision", "message", "goals", "values", "step"]:
                    st.session_state.pop(k, None)
                st.session_state.step = 1
                st.session_state._new_init_done = True
                st.session_state._loaded_id = None
                save_progress(-1, 1)

            if st.button(tr("start_over")):
                for k in ["strategy_id", "name", "vision", "message", "goals", "values", "step"]:
                    st.session_state.pop(k, None)
                st.session_state.step = 1
                st.session_state._new_init_done = True
                st.session_state._loaded_id = None
                save_progress(-1, 1)
                st.rerun()

            run_wizard(visions, vision_to_msgs, msg_to_goals, msg_to_values, all_goals, all_values, preferred_font)

        else:
            strategies = list_strategies()
            if not strategies:
                st.info(tr("no_strategies"))
                return

            options_list = [f"{s['id']} - {s['name']} ({s['created_at']})" for s in strategies]

            # ✅ اختيار الاستراتيجية الافتراضي لو جاي من زر تعديل
            if "strategy_id" in st.session_state:
                try:
                    default_index = next(i for i, s in enumerate(strategies) if s["id"] == st.session_state["strategy_id"])
                except StopIteration:
                    default_index = 0
            else:
                default_index = 0

            choice = st.selectbox(tr("choose_strategy"), options_list, index=default_index)

            if choice:
                sid = int(choice.split("-")[0].strip())
                if st.session_state.get("_loaded_id") != sid:
                    s = get_strategy(sid)
                    st.session_state.strategy_id = s["id"]
                    st.session_state.name = s["name"]
                    st.session_state.vision = s["vision"]
                    st.session_state.message = s["message"]
                    st.session_state.goals = s["goals"]
                    st.session_state["values"] = s["values"]
                    st.session_state.step = 1
                    st.session_state._loaded_id = sid
                    st.session_state._new_init_done = False
                    save_progress(sid, 1)

            run_wizard(visions, vision_to_msgs, msg_to_goals, msg_to_values, all_goals, all_values, preferred_font)

    if mode == tr("browse_strategies"):
        st.subheader(tr("saved_strategies"))
        strategies = list_strategies()
        if not strategies:
            st.info(tr("no_strategies"))
            return

        colf1, colf2, colf3 = st.columns(3)
        with colf1:
            q = st.text_input(tr("search"))
        with colf2:
            min_date = st.date_input(tr("filter_date"), value=datetime.date(2000, 1, 1))
        with colf3:
            sort_options = [tr("newest_first"), tr("oldest_first"), tr("name_az"), tr("name_za")]
            sort_opt = st.selectbox(tr("sort_by"), sort_options)

        filtered = []
        for s in strategies:
            ok_q = (not q.strip()) or (q.strip().lower() in s["name"].lower())
            ok_d = datetime.date.fromisoformat(s["created_at"][:10]) >= min_date
            if ok_q and ok_d:
                filtered.append(s)

        if sort_opt == tr("newest_first"):
            filtered = sorted(filtered, key=lambda x: x["created_at"], reverse=True)
        elif sort_opt == tr("oldest_first"):
            filtered = sorted(filtered, key=lambda x: x["created_at"])
        elif sort_opt == tr("name_az"):
            filtered = sorted(filtered, key=lambda x: x["name"].lower())
        else:
            filtered = sorted(filtered, key=lambda x: x["name"].lower(), reverse=True)

        if not filtered:
            st.warning(tr("no_results"))
            return

        choice = st.selectbox(tr("choose_strategy"), [f"{s['id']} - {s['name']} ({s['created_at']})" for s in filtered])
        sid = int(choice.split("-")[0].strip())
        data = get_strategy(sid)

        st.markdown(f"### 📄 {data['name']}")
        st.markdown(f"**{tr('vision')}:** {data['vision']}")
        st.markdown(f"**{tr('mission')}:** {data['message']}")
        st.markdown(f"**{tr('goals')}:**")
        st.write(data["goals"])
        st.markdown(f"**{tr('values')}:**")
        st.write(data["values"])

        c1, c2, c3, c4, c5 = st.columns(5)
        with c1:
            if st.button(tr("edit")):
                st.session_state.strategy_id = data["id"]
                st.session_state.name = data["name"]
                st.session_state.vision = data["vision"]
                st.session_state.message = data["message"]
                st.session_state.goals = data["goals"]
                st.session_state["values"] = data["values"]
                st.session_state.step = 1
                st.session_state._loaded_id = data["id"]
                st.session_state._new_init_done = False
                save_progress(data["id"], 1)

                st.session_state["force_edit_mode"] = True
                st.session_state["pending_nav"] = tr("new_strategy")
                st.rerun()

        with c2:
            if st.button(tr("delete")):
                delete_strategy(sid)
                st.warning(tr("strategy_deleted"))
                st.rerun()
        with c3:
            if st.button(tr("clone")):
                new_id = clone_strategy(sid)
                if new_id:
                    st.success(f"{tr('strategy_cloned')} (ID: {new_id})")
                    st.rerun()
        with c4:
            if st.button(tr("export_word")):
                fname = export_to_word(data, assets_dir=ASSETS_DIR)
                with open(fname, "rb") as f:
                    st.download_button(tr("download"), f, file_name=os.path.basename(fname), key="dlw_list")
        with c5:
            if st.button(tr("export_pdf")):
                fname = export_to_pdf(data, assets_dir=ASSETS_DIR, preferred_family=preferred_font)
                with open(fname, "rb") as f:
                    st.download_button(tr("download"), f, file_name=os.path.basename(fname), key="dlp_list")

if __name__ == "__main__":
    main()