# -*- coding: utf-8 -*-
import os
import datetime
import streamlit as st

from strategy_builder.ui.styling import apply_base_styles, apply_theme_choice
from strategy_builder.ui.sidebar import sidebar_controls
from strategy_builder.ui.wizard import run_wizard
from strategy_builder.ui.settings import render_settings
from strategy_builder.data.db import init_db, list_strategies, get_strategy, delete_strategy, clone_strategy
from strategy_builder.data.progress import load_progress, save_progress
from strategy_builder.data.excel_bank import load_bank, build_relations
from strategy_builder.export.word_export import export_to_word
from strategy_builder.export.pdf_export import export_to_pdf
from strategy_builder.config import load_config, save_config, discover_defaults, apply_to_session_state

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "strategy_builder", "assets")
DEFAULT_BANK_PATH = os.path.join(ASSETS_DIR, "بنك_الاستراتيجية v2.0.xlsx")

def main():
    st.set_page_config(page_title="مدير الاستراتيجيات", layout="wide")
    apply_base_styles()

    # Ensure DB exists
    _ = init_db()

    # Load persisted config and seed session state
    cfg = load_config(ASSETS_DIR)
    if not cfg:
        cfg = discover_defaults(ASSETS_DIR)
        if cfg:
            save_config(ASSETS_DIR, cfg)
    apply_to_session_state(ASSETS_DIR, cfg, st)

    # Sidebar UI (theme + status)
    theme_choice, preferred_font, logo_p = sidebar_controls(ASSETS_DIR)
    apply_theme_choice(theme_choice)

    # Header (logo + title)
    col_t, col_l = st.columns([8, 2])
    with col_l:
        if logo_p and os.path.exists(logo_p):
            st.image(logo_p, use_container_width=True)
    with col_t:
        st.title("🗂️ مدير الاستراتيجيات")
        if cfg.get("logo_filename"):
            st.caption(f"الشعار الحالي: {cfg.get('logo_filename')}")
        if cfg.get("pdf_font_preference"):
            st.caption(f"خط PDF المفضل: {cfg.get('pdf_font_preference')}")

    # ---- Navigation ----
    st.sidebar.header("القائمة")
    options = ["🏗️ بناء/تعديل استراتيجية", "📂 استعراض/إدارة الاستراتيجيات", "⏯️ استكمال آخر جلسة", "⚙️ الإعدادات"]

    if "pending_nav" in st.session_state:
        st.session_state["nav_radio"] = st.session_state["pending_nav"]
        del st.session_state["pending_nav"]

    mode = st.sidebar.radio("اختر:", options, key="nav_radio")

    # Open settings page early
    if mode == "⚙️ الإعدادات":
        render_settings(ASSETS_DIR)
        return

    # Load bank (must exist for other modes)
    bank_path = None
    if cfg.get('bank_filename'):
        possible = os.path.join(ASSETS_DIR, cfg['bank_filename'])
        if os.path.exists(possible):
            bank_path = possible
            st.info(f"سيتم استخدام بنك الاستراتيجية: **{os.path.basename(bank_path)}**")
    if not bank_path and os.path.exists(DEFAULT_BANK_PATH):
        bank_path = DEFAULT_BANK_PATH
        st.info(f"سيتم استخدام بنك الاستراتيجية: **{os.path.basename(bank_path)}**")
    if not bank_path:
        st.warning("⚠️ لم يتم العثور على ملف بنك الاستراتيجية داخل assets. توجه إلى صفحة الإعدادات (⚙️) لرفعه.")
        return

    df = load_bank(bank_path)
    visions, vision_to_msgs, msg_to_goals, msg_to_values, all_goals, all_values = build_relations(df)

    # ---- Modes ----
    if mode == "⏯️ استكمال آخر جلسة":
        prog = load_progress()
        if not prog:
            st.info("لا توجد جلسة محفوظة.")
            return
        s = get_strategy(prog.get("strategy_id", -1))
        if not s:
            st.warning("لم يتم العثور على الاستراتيجية الأخيرة.")
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

    if mode == "🏗️ بناء/تعديل استراتيجية":
        action_options = ["إنشاء استراتيجية جديدة", "تحميل استراتيجية محفوظة للتعديل"]

        # ✅ لو في جلسة تعديل، نخلي الافتراضي "تحميل استراتيجية محفوظة للتعديل"
        if "force_edit_mode" in st.session_state and st.session_state["force_edit_mode"]:
            default_action = "تحميل استراتيجية محفوظة للتعديل"
        else:
            default_action = action_options[0]

        action = st.radio(
            "اختيار الإجراء:",
            action_options,
            index=action_options.index(default_action),
            horizontal=True
        )

        # 👇 لو المستخدم غيّر يدويًا إلى "إنشاء"، نلغي وضع التعديل
        if action == "إنشاء استراتيجية جديدة" and "force_edit_mode" in st.session_state:
            st.session_state["force_edit_mode"] = False

        if action == "إنشاء استراتيجية جديدة":
            # Reset once
            if st.session_state.get("_new_init_done") is not True:
                for k in ["strategy_id", "name", "vision", "message", "goals", "values", "step"]:
                    st.session_state.pop(k, None)
                st.session_state.step = 1
                st.session_state._new_init_done = True
                st.session_state._loaded_id = None
                save_progress(-1, 1)

            if st.button("🔄 ابدأ من جديد"):
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
                st.info("لا توجد استراتيجيات محفوظة بعد.")
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

            choice = st.selectbox("اختر استراتيجية", options_list, index=default_index)

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

    if mode == "📂 استعراض/إدارة الاستراتيجيات":
        st.subheader("📂 الاستراتيجيات المحفوظة")
        strategies = list_strategies()
        if not strategies:
            st.info("لا توجد استراتيجيات محفوظة.")
            return

        colf1, colf2, colf3 = st.columns(3)
        with colf1:
            q = st.text_input("🔎 بحث بالاسم")
        with colf2:
            min_date = st.date_input("📅 من تاريخ", value=datetime.date(2000, 1, 1))
        with colf3:
            sort_opt = st.selectbox("📊 ترتيب حسب", ["🆕 الأحدث أولًا", "🕰️ الأقدم أولًا", "🔤 الاسم (A→Z)", "🔤 الاسم (Z→A)"])

        filtered = []
        for s in strategies:
            ok_q = (not q.strip()) or (q.strip().lower() in s["name"].lower())
            ok_d = datetime.date.fromisoformat(s["created_at"][:10]) >= min_date
            if ok_q and ok_d:
                filtered.append(s)

        if sort_opt == "🆕 الأحدث أولًا":
            filtered = sorted(filtered, key=lambda x: x["created_at"], reverse=True)
        elif sort_opt == "🕰️ الأقدم أولًا":
            filtered = sorted(filtered, key=lambda x: x["created_at"])
        elif sort_opt == "🔤 الاسم (A→Z)":
            filtered = sorted(filtered, key=lambda x: x["name"].lower())
        else:
            filtered = sorted(filtered, key=lambda x: x["name"].lower(), reverse=True)

        if not filtered:
            st.warning("لا توجد نتائج مطابقة.")
            return

        choice = st.selectbox("اختر استراتيجية", [f"{s['id']} - {s['name']} ({s['created_at']})" for s in filtered])
        sid = int(choice.split("-")[0].strip())
        data = get_strategy(sid)

        st.markdown(f"### 📄 {data['name']}")
        st.markdown(f"**الرؤية:** {data['vision']}")
        st.markdown(f"**الرسالة:** {data['message']}")
        st.markdown("**الأهداف:**")
        st.write(data["goals"])
        st.markdown("**القيم:**")
        st.write(data["values"])

        c1, c2, c3, c4, c5 = st.columns(5)
        with c1:
            if st.button("✏️ تعديل"):
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
                st.session_state["pending_nav"] = "🏗️ بناء/تعديل استراتيجية"
                st.rerun()

        with c2:
            if st.button("🗑️ حذف"):
                delete_strategy(sid)
                st.warning("🚮 تم حذف الاستراتيجية")
                st.rerun()
        with c3:
            if st.button("📄 نسخ (Clone)"):
                new_id = clone_strategy(sid)
                if new_id:
                    st.success(f"✅ تم إنشاء نسخة (ID: {new_id})")
                    st.rerun()
        with c4:
            if st.button("📤 تصدير Word"):
                fname = export_to_word(data, assets_dir=ASSETS_DIR)
                with open(fname, "rb") as f:
                    st.download_button("تحميل Word", f, file_name=os.path.basename(fname), key="dlw_list")
        with c5:
            if st.button("📤 تصدير PDF"):
                fname = export_to_pdf(data, assets_dir=ASSETS_DIR, preferred_family=preferred_font)
                with open(fname, "rb") as f:
                    st.download_button("تحميل PDF", f, file_name=os.path.basename(fname), key="dlp_list")

if __name__ == "__main__":
    main()
