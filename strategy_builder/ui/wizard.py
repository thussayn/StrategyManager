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

def pill_steps(current: int):
    cols = st.columns(5)
    labels = ["الرؤية", "الرسالة", "الأهداف", "القيم", "مراجعة"]
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
    st.session_state.name = st.text_input("اسم الاستراتيجية", value=st.session_state.get("name", ""))
    if st.button("💾 حفظ الاسم"):
        nm = st.session_state.get("name", "").strip()
        if nm:
            if st.session_state.get("strategy_id"):
                update_strategy_name(st.session_state.strategy_id, nm)
                st.success("تم حفظ الاسم.")
            else:
                st.info("سيتم إنشاء الاستراتيجية عند حفظ أول خطوة.")

    # ===== الخطوة 1: الرؤية =====
    if st.session_state.step == 1:
        st.subheader("الخطوة 1: الرؤية")
        
        # اختر رؤية من الـ dropdown
        v_choice = st.selectbox("اختر رؤية من البنك", ["— اختر —"] + visions, index=0)
        
        # إذا تم اختيار رؤية من الدروب داون
        if v_choice != "— اختر —":
            st.session_state["vision"] = v_choice

        # عرض النص في text_area
        v_text = st.text_area(
            "✏️ تعديل/إدخال رؤية",
            value=st.session_state.get("vision", "")  # نعرض القيمة في session_state
        )

        # حفظ الرؤية في session_state
        vision_input = v_text.strip() or (v_choice if v_choice != "— اختر —" else "")

        col1, col2 = st.columns(2)
        if col1.button("⬅️ السابق", disabled=True):
            pass
        if col2.button("التالي ➡️", type="primary"):
            if vision_input:
                if not st.session_state.strategy_id:
                    name = st.session_state.name.strip() or f"استراتيجية {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}"
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
                st.warning("⚠️ يجب إدخال أو اختيار رؤية قبل الانتقال للخطوة التالية")

    # ===== الخطوة 2: الرسالة =====
    elif st.session_state.step == 2:
        st.subheader("الخطوة 2: الرسالة")
        msgs = vision_to_msgs.get(st.session_state.get("vision", ""), [])
        m_choice = st.selectbox("الرسائل المرتبطة بالرؤية", ["— اختر —"] + msgs, index=0)
        
        m_text = st.text_area(
            "✏️ تعديل/إدخال رسالة",
            value=st.session_state.get("message", "") or ("" if m_choice == "— اختر —" else m_choice),
        )
        
        # حفظ الرسالة في session_state
        message_input = m_text.strip() or (m_choice if m_choice != "— اختر —" else "")

        col1, col2 = st.columns(2)
        if col1.button("⬅️ السابق"):
            st.session_state.step = 1
            save_progress(st.session_state.strategy_id, st.session_state.step)
            st.rerun()
        if col2.button("التالي ➡️", type="primary"):
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
                st.warning("⚠️ يجب إدخال أو اختيار رسالة قبل الانتقال للخطوة التالية")

    # ===== الخطوة 3: الأهداف =====
    elif st.session_state.step == 3:
        st.subheader("الخطوة 3: الأهداف")
        rel_goals = msg_to_goals.get(st.session_state.get("message", ""), [])
        g1 = st.multiselect("🎯 أهداف مرتبطة بهذه الرسالة", rel_goals, key="ms_rel_goals")
        g2 = st.multiselect("📚 أهداف من بنك الأهداف (كل البنك)", all_goals, key="ms_all_goals")
        new_goal = st.text_input("➕ أضف هدف (اختياري)")

        merged = list(dict.fromkeys(st.session_state.get("goals", [])))
        for src in [g1, g2]:
            for x in src:
                if x not in merged:
                    merged.append(x)
        if new_goal.strip() and new_goal not in merged:
            merged.append(new_goal.strip())

        st.markdown("### ✏️ عدّل صياغة الأهداف المختارة")
        edited_goals = editable_text_list(merged, key_prefix="edit_goal")

        col1, col2 = st.columns(2)
        if col1.button("⬅️ السابق"):
            st.session_state.step = 2
            save_progress(st.session_state.strategy_id, st.session_state.step)
            st.rerun()
        if col2.button("التالي ➡️", type="primary"):
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
                st.warning("⚠️ يجب اختيار أو إدخال هدف واحد على الأقل")

    # ===== الخطوة 4: القيم =====
    elif st.session_state.step == 4:
        st.subheader("الخطوة 4: القيم")
        rel_vals = msg_to_values.get(st.session_state.get("message", ""), [])
        v1 = st.multiselect("⭐ قيم مرتبطة بهذه الرسالة", rel_vals, key="ms_rel_vals")
        v2 = st.multiselect("📚 قيم من بنك القيم (كل البنك)", all_values, key="ms_all_vals")
        new_val = st.text_input("➕ أضف قيمة (اختياري)")

        merged = list(dict.fromkeys(st.session_state.get("values", [])))
        for src in [v1, v2]:
            for x in src:
                if x not in merged:
                    merged.append(x)
        if new_val.strip() and new_val not in merged:
            merged.append(new_val.strip())

        st.markdown("### ✏️ عدّل صياغة القيم المختارة")
        edited_vals = editable_text_list(merged, key_prefix="edit_val")

        col1, col2 = st.columns(2)
        if col1.button("⬅️ السابق"):
            st.session_state.step = 3
            save_progress(st.session_state.strategy_id, st.session_state.step)
            st.rerun()
        if col2.button("التالي ➡️", type="primary"):
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
                st.warning("⚠️ يجب اختيار أو إدخال قيمة واحدة على الأقل")

    # ===== الخطوة 5: المراجعة والتصدير =====
    elif st.session_state.step == 5:
        st.subheader("الخطوة 5: المراجعة والتصدير")
        st.markdown(f"**الاسم:** {st.session_state.get('name','')}")
        st.markdown(f"**الرؤية:** {st.session_state.get('vision','')}")
        st.markdown(f"**الرسالة:** {st.session_state.get('message','')}")
        st.markdown("**الأهداف:**")
        st.write(st.session_state.get("goals", []))
        st.markdown("**القيم:**")
        st.write(st.session_state.get("values", []))

        col1, col2, col3 = st.columns(3)
        if col1.button("⬅️ السابق"):
            st.session_state.step = 4
            save_progress(st.session_state.strategy_id, st.session_state.step)
            st.rerun()
        if col2.button("📤 تصدير Word"):
            nm = st.session_state.get("name", "").strip()
            if nm and st.session_state.get("strategy_id"):
                update_strategy_name(st.session_state.strategy_id, nm)
            s = get_strategy(st.session_state.strategy_id)
            fname = export_to_word(s)
            with open(fname, "rb") as f:
                st.download_button("تحميل Word", f, file_name=os.path.basename(fname), key="dlw_review")
        if col3.button("📤 تصدير PDF"):
            nm = st.session_state.get("name", "").strip()
            if nm and st.session_state.get("strategy_id"):
                update_strategy_name(st.session_state.strategy_id, nm)
            s = get_strategy(st.session_state.strategy_id)
            fname = export_to_pdf(s, preferred_family=preferred_font)
            with open(fname, "rb") as f:
                st.download_button("تحميل PDF", f, file_name=os.path.basename(fname), key="dlp_review")
