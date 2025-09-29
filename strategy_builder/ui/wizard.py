# strategy_builder/ui/wizard.py
# -*- coding: utf-8 -*-
import os
import datetime
import streamlit as st

from strategy_builder.data.db import (
    create_strategy,
    upsert_components,
    get_strategy,
    update_strategy_name,
)
from strategy_builder.data.progress import save_progress
from strategy_builder.export.word_export import export_to_word
from strategy_builder.export.pdf_export import export_to_pdf
from strategy_builder.Languages.translations import get_translation

def tr(key: str) -> str:
    """Translation helper function"""
    lang = st.session_state.get("language", "ar")
    return get_translation(lang, key)

def pill_steps(current: int):
    cols = st.columns(5)
    labels = [tr("vision"), tr("mission"), tr("goals"), tr("values"), tr("review")]
    # مع اتجاه RTL، الأعمدة تظهر من اليمين لليسار تلقائيًا، لذا لا نعكس الترتيب يدويًا.
    for i, (col, lbl) in enumerate(zip(cols, labels), start=1):
        style = "✅" if i < current else ("🔵" if i == current else "⚪")
        with col:
            st.button(
                f"{lbl} {style}",
                key=f"hdr_{i}",
                use_container_width=True,
                on_click=lambda s=i: st.session_state.update(step=s),
            )

def editable_text_list(items: list, key_prefix: str):
    edited = []
    for i, it in enumerate(items):
        val = st.text_input("", value=it, key=f"{key_prefix}_{i}")
        if val.strip():
            edited.append(val.strip())
    return edited

def run_wizard(visions, vision_to_msgs, msg_to_goals, msg_to_values, all_goals, all_values, preferred_font: str):
    # تهيئة الحالة
    if "step" not in st.session_state:
        st.session_state.step = 1
    if "strategy_id" not in st.session_state:
        st.session_state.strategy_id = None
    if "name" not in st.session_state:
        st.session_state.name = ""

    pill_steps(st.session_state.step)

    # اسم الاستراتيجية + زر حفظ
    st.session_state.name = st.text_input(tr("strategy_name"), value=st.session_state.get("name", ""))
    if st.button(tr("save_name")):
        nm = st.session_state.get("name", "").strip()
        if nm:
            if st.session_state.get("strategy_id"):
                update_strategy_name(st.session_state.strategy_id, nm)
                st.success(tr("name_saved"))
            else:
                st.info(tr("strategy_will_create"))

    # ===== الخطوة 1: الرؤية =====
    if st.session_state.step == 1:
        st.subheader(f"{tr('step')} 1: {tr('vision')}")
        
        # اختر رؤية من الـ dropdown
        v_choice = st.selectbox(tr("select_vision_from_bank"), ["— " + tr("select") + " —"] + visions, index=0)
        
        # إذا تم اختيار رؤية من الدروب داون
        if v_choice != "— " + tr("select") + " —":
            st.session_state["vision"] = v_choice

        # عرض النص في text_area
        v_text = st.text_area(
            tr("edit_enter_vision"),
            value=st.session_state.get("vision", "")  # نعرض القيمة في session_state
        )

        # حفظ الرؤية في session_state
        vision_input = v_text.strip() or (v_choice if v_choice != "— " + tr("select") + " —" else "")

        col1, col2 = st.columns(2)
        if col1.button("⬅️ " + tr("back"), disabled=True):
            pass
        if col2.button(tr("next") + " ➡️", type="primary"):
            if vision_input:
                if not st.session_state.strategy_id:
                    name = st.session_state.name.strip() or tr("default_strategy_name") + f" {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}"
                    st.session_state.strategy_id = create_strategy(name)
                    st.session_state.name = name

                # عند اختيار رؤية جديدة، نحتفظ ببقية القيم (الرسالة، الأهداف، القيم) كما هي
                st.session_state.vision = vision_input
                st.session_state.message = st.session_state.get("message", "")
                st.session_state.goals = st.session_state.get("goals", [])
                st.session_state.values = st.session_state.get("values", [])

                # حفظ الاسم إن وجد ID
                nm = st.session_state.get("name", "").strip()
                if nm and st.session_state.get("strategy_id"):
                    update_strategy_name(st.session_state.strategy_id, nm)

                st.session_state.step = 2
                save_progress(st.session_state.get("strategy_id", -1), 2)

                # حفظ الاستراتيجية مع الرؤية الجديدة
                upsert_components(
                    st.session_state.strategy_id,
                    st.session_state["vision"],
                    st.session_state.get("message", ""),
                    st.session_state.get("goals", []),
                    st.session_state.get("values", []),
                )
                st.rerun()
            else:
                st.warning(tr("vision_required"))

    # ===== الخطوة 2: الرسالة =====
    elif st.session_state.step == 2:
        st.subheader(f"{tr('step')} 2: {tr('mission')}")
        msgs = vision_to_msgs.get(st.session_state.get("vision", ""), [])
        m_choice = st.selectbox(tr("missions_linked_to_vision"), ["— " + tr("select") + " —"] + msgs, index=0)
        
        m_text = st.text_area(
            tr("edit_enter_mission"),
            value=st.session_state.get("message", "") or ("" if m_choice == "— " + tr("select") + " —" else m_choice),
        )
        
        # حفظ الرسالة في session_state
        message_input = m_text.strip() or (m_choice if m_choice != "— " + tr("select") + " —" else "")

        col1, col2 = st.columns(2)
        if col1.button("⬅️ " + tr("back")):
            st.session_state.step = 1
            save_progress(st.session_state.strategy_id, st.session_state.step)
            st.rerun()
        if col2.button(tr("next") + " ➡️", type="primary"):
            if message_input:
                st.session_state.message = message_input

                nm = st.session_state.get("name", "").strip()
                if nm and st.session_state.get("strategy_id"):
                    update_strategy_name(st.session_state.strategy_id, nm)

                st.session_state.step = 3
                save_progress(st.session_state.strategy_id, st.session_state.step)

                # حفظ المكونات بما فيها الرسالة
                upsert_components(
                    st.session_state.strategy_id,
                    st.session_state.get("vision", ""),
                    st.session_state.message,
                    st.session_state.get("goals", []),
                    st.session_state.get("values", []),
                )
                st.rerun()
            else:
                st.warning(tr("mission_required"))

    # ===== الخطوة 3: الأهداف =====
    elif st.session_state.step == 3:
        st.subheader(f"{tr('step')} 3: {tr('goals')}")
        rel_goals = msg_to_goals.get(st.session_state.get("message", ""), [])
        g1 = st.multiselect(tr("goals_linked_to_mission"), rel_goals, key="ms_rel_goals")
        g2 = st.multiselect(tr("goals_from_bank"), all_goals, key="ms_all_goals")
        new_goal = st.text_input(tr("add_new_goal"))

        merged = list(dict.fromkeys(st.session_state.get("goals", [])))
        for src in [g1, g2]:
            for x in src:
                if x not in merged:
                    merged.append(x)
        if new_goal.strip() and new_goal not in merged:
            merged.append(new_goal.strip())

        st.markdown(f"### {tr('edit_selected_goals')}")
        edited_goals = editable_text_list(merged, key_prefix="edit_goal")

        col1, col2 = st.columns(2)
        if col1.button("⬅️ " + tr("back")):
            st.session_state.step = 2
            save_progress(st.session_state.strategy_id, st.session_state.step)
            st.rerun()
        if col2.button(tr("next") + " ➡️", type="primary"):
            edited_goals = [g.strip() for g in edited_goals if g.strip()]
            if edited_goals:
                st.session_state.goals = edited_goals

                nm = st.session_state.get("name", "").strip()
                if nm and st.session_state.get("strategy_id"):
                    update_strategy_name(st.session_state.strategy_id, nm)

                st.session_state.step = 4
                save_progress(st.session_state.strategy_id, st.session_state.step)

                # حفظ المكونات بما فيها الأهداف
                upsert_components(
                    st.session_state.strategy_id,
                    st.session_state.get("vision", ""),
                    st.session_state.get("message", ""),
                    st.session_state.goals,
                    [],
                )
                st.rerun()
            else:
                st.warning(tr("at_least_one_goal"))

    # ===== الخطوة 4: القيم =====
    elif st.session_state.step == 4:
        st.subheader(f"{tr('step')} 4: {tr('values')}")
        rel_vals = msg_to_values.get(st.session_state.get("message", ""), [])
        v1 = st.multiselect(tr("values_linked_to_mission"), rel_vals, key="ms_rel_vals")
        v2 = st.multiselect(tr("values_from_bank"), all_values, key="ms_all_vals")
        new_val = st.text_input(tr("add_new_value"))

        merged = list(dict.fromkeys(st.session_state.get("values", [])))
        for src in [v1, v2]:
            for x in src:
                if x not in merged:
                    merged.append(x)
        if new_val.strip() and new_val not in merged:
            merged.append(new_val.strip())

        st.markdown(f"### {tr('edit_selected_values')}")
        edited_vals = editable_text_list(merged, key_prefix="edit_val")

        col1, col2 = st.columns(2)
        if col1.button("⬅️ " + tr("back")):
            st.session_state.step = 3
            save_progress(st.session_state.strategy_id, st.session_state.step)
            st.rerun()
        if col2.button(tr("next") + " ➡️", type="primary"):
            edited_vals = [v.strip() for v in edited_vals if v.strip()]
            if edited_vals:
                st.session_state["values"] = edited_vals

                nm = st.session_state.get("name", "").strip()
                if nm and st.session_state.get("strategy_id"):
                    update_strategy_name(st.session_state.strategy_id, nm)

                st.session_state.step = 5
                save_progress(st.session_state.strategy_id, st.session_state.step)

                # حفظ المكونات بما فيها القيم
                upsert_components(
                    st.session_state.strategy_id,
                    st.session_state.get("vision", ""),
                    st.session_state.get("message", ""),
                    st.session_state.get("goals", []),
                    st.session_state["values"],
                )
                st.rerun()
            else:
                st.warning(tr("at_least_one_value"))

    # ===== الخطوة 5: المراجعة والتصدير =====
    elif st.session_state.step == 5:
        st.subheader(f"{tr('step')} 5: {tr('review_export')}")
        st.markdown(f"**{tr('strategy_name')}:** {st.session_state.get('name','')}")
        st.markdown(f"**{tr('vision')}:** {st.session_state.get('vision','')}")
        st.markdown(f"**{tr('mission')}:** {st.session_state.get('message','')}")
        st.markdown(f"**{tr('goals')}:**")
        st.write(st.session_state.get("goals", []))
        st.markdown(f"**{tr('values')}:**")
        st.write(st.session_state.get("values", []))

        col1, col2, col3 = st.columns(3)
        if col1.button("⬅️ " + tr("back")):
            st.session_state.step = 4
            save_progress(st.session_state.strategy_id, st.session_state.step)
            st.rerun()
        if col2.button("📤 " + tr("export_word")):
            nm = st.session_state.get("name", "").strip()
            if nm and st.session_state.get("strategy_id"):
                update_strategy_name(st.session_state.strategy_id, nm)
            s = get_strategy(st.session_state.strategy_id)
            fname = export_to_word(s)
            with open(fname, "rb") as f:
                st.download_button(tr("download_word"), f, file_name=os.path.basename(fname), key="dlw_review")
        if col3.button("📤 " + tr("export_pdf")):
            nm = st.session_state.get("name", "").strip()
            if nm and st.session_state.get("strategy_id"):
                update_strategy_name(st.session_state.strategy_id, nm)
            s = get_strategy(st.session_state.strategy_id)
            fname = export_to_pdf(s, preferred_family=preferred_font)
            with open(fname, "rb") as f:
                st.download_button(tr("download_pdf"), f, file_name=os.path.basename(fname), key="dlp_review")