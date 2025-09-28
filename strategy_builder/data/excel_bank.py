# -*- coding: utf-8 -*-
import pandas as pd
import streamlit as st

@st.cache_data(show_spinner=False)
def load_bank(path_or_file):
    df = pd.read_excel(path_or_file, sheet_name="بنك الاستراتيجية")
    for col in ["الرؤية","الرسالة","الهدف","القيمة"]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()
    return df

def build_relations(df: pd.DataFrame):
    visions = sorted([x for x in df["الرؤية"].dropna().unique().tolist() if x and x!="nan"])
    vision_to_msgs, msg_to_goals, msg_to_values = {}, {}, {}

    for v in visions:
        msgs = df.loc[df["الرؤية"]==v,"الرسالة"].dropna().unique().tolist()
        vision_to_msgs[v] = sorted(list({m for m in msgs if m and m!="nan"}))

    all_msgs = sorted(df["الرسالة"].dropna().unique().tolist())
    for m in all_msgs:
        gl = df.loc[df["الرسالة"]==m,"الهدف"].dropna().unique().tolist()
        msg_to_goals[m] = sorted(list({g for g in gl if g and g!="nan"}))
        vl = df.loc[df["الرسالة"]==m,"القيمة"].dropna().unique().tolist()
        msg_to_values[m] = sorted(list({v for v in vl if v and v!="nan"}))

    all_goals = sorted(list({g for g in df["الهدف"].dropna().unique().tolist() if g and g!="nan"}))
    all_values = sorted(list({v for v in df["القيمة"].dropna().unique().tolist() if v and v!="nan"}))
    return visions, vision_to_msgs, msg_to_goals, msg_to_values, all_goals, all_values
