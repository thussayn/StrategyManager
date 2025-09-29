# strategy_builder/ui/styling.py
# -*- coding: utf-8 -*-
import streamlit as st

def get_text_direction():
    """الحصول على اتجاه النص بناءً على اللغة"""
    lang = st.session_state.get("language", "ar")
    return "rtl" if lang == "ar" else "ltr"

def get_sidebar_position():
    """الحصول على موقع الشريط الجانبي بناءً على اللغة"""
    lang = st.session_state.get("language", "ar")
    return "right" if lang == "ar" else "left"

def apply_base_styles():
    """تطبيق الأنماط الأساسية للتطبيق مع دعم RTL/LTR ديناميكي"""
    direction = get_text_direction()
    sidebar_pos = get_sidebar_position()
    text_align = 'right' if direction == 'rtl' else 'left'
    
    st.markdown(f"""
    <style>
    /* ========== CSS HACK آمن - إصلاح المحاذاة فقط ========== */
    .main {{
        direction: {direction};
        text-align: {text_align};
    }}
    
    /* إصلاح كل المحاذاة الداخلية */
    label, h1, h2, h3, h4, h5, h6 {{
        text-align: {text_align} !important;
        direction: {direction} !important;
        width: 100% !important;
        display: block !important;
    }}
    
    /* تحسين الـ form labels بشكل خاص */
    .stTextInput label, 
    .stTextArea label, 
    .stSelectbox label, 
    .stRadio label, 
    .stMultiSelect label,
    .stNumberInput label,
    .stDateInput label,
    .stTimeInput label {{
        text-align: {text_align} !important;
        direction: {direction} !important;
        width: 100% !important;
        display: block !important;
        font-weight: 500 !important;
    }}
    
    /* تحسين الـ headers والعناوين */
    h1, h2, h3, h4, h5, h6 {{
        color: #1f77b4;
        font-weight: 600;
        text-align: {text_align} !important;
        direction: {direction} !important;
        width: 100% !important;
    }}
    
    /* تحسين الـ markdown texts */
    .stMarkdown, .stText {{
        text-align: {text_align} !important;
        direction: {direction} !important;
    }}
    
    /* تحسين الـ alerts والرسائل */
    .stAlert {{
        text-align: {text_align} !important;
        direction: {direction} !important;
        border-radius: 8px;
    }}
    
    /* تحسين الـ captions */
    .stCaption {{
        text-align: {text_align} !important;
        direction: {direction} !important;
    }}
    
    /* تحسين الـ radio buttons */
    div[data-testid="stRadio"] > div {{
        flex-direction: {'row-reverse' if direction == 'rtl' else 'row'} !important;
        justify-content: {'flex-end' if direction == 'rtl' else 'flex-start'} !important;
        gap: 15px !important;
    }}
    
    div[data-testid="stRadio"] > div > label {{
        text-align: {text_align} !important;
        direction: {direction} !important;
        margin-{'left' if direction == 'rtl' else 'right'}: 15px !important;
        margin-{'right' if direction == 'rtl' else 'left'}: 0 !important;
    }}
    
    /* تحسين الحقول - نص داخلي */
    .stTextInput>div>div>input, 
    .stTextArea>div>div>textarea {{
        text-align: {text_align} !important;
        direction: {direction} !important;
        border-radius: 8px;
        border: 1px solid #ddd;
        padding: 10px;
    }}
    
    /* تحسين القوائم - نص داخلي */
    .stSelectbox>div>div>select {{
        text-align: {text_align} !important;
        direction: {direction} !important;
        border-radius: 8px;
    }}
    
    /* تحسين الـ dropdown options */
    .stSelectbox>div>div>div>div {{
        text-align: {text_align} !important;
        direction: {direction} !important;
    }}
    
    /* تحسين الـ multiselect */
    .stMultiSelect>div>div>div {{
        text-align: {text_align} !important;
        direction: {direction} !important;
        border-radius: 8px;
    }}
    
    /* تحسين الأزرار */
    .stButton>button {{
        width: 100%;
        border-radius: 8px;
        font-weight: 500;
        transition: all 0.3s ease;
    }}
    
    .stButton>button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }}
    
    /* تحسين الخطوات */
    .step-pill {{
        background-color: #f0f2f6;
        border-radius: 20px;
        padding: 8px 16px;
        margin: 5px;
        text-align: center;
        font-weight: 500;
    }}
    
    .step-pill.active {{
        background-color: #1f77b4;
        color: white;
    }}
    
    .step-pill.completed {{
        background-color: #2ecc71;
        color: white;
    }}
    
    /* تحسين الجداول */
    .dataframe {{
        border-radius: 8px;
        overflow: hidden;
    }}
    
    /* تحسين الـ columns بناءً على الاتجاه */
    .row-widget.stColumns {{
        flex-direction: {'row-reverse' if direction == 'rtl' else 'row'} !important;
    }}
    
    /* تحسين محاذاة الأزرار */
    .stButton {{
        text-align: {text_align} !important;
        direction: {direction} !important;
    }}
    
    /* تحسين الـ sidebar بناءً على الاتجاه */
    section[data-testid="stSidebar"] {{
        text-align: {text_align} !important;
        direction: {direction} !important;
    }}
    
    /* تحسين محتوى الـ sidebar */
    .css-1d391kg {{
        text-align: {text_align} !important;
        direction: {direction} !important;
    }}
    
    /* تحسين الـ placeholders في الحقول */
    .stTextInput input::placeholder, 
    .stTextArea textarea::placeholder {{
        text-align: {text_align} !important;
        direction: {direction} !important;
    }}
    
    /* تحسين الـ headers في السايدبار */
    .css-1v0mbdj {{
        text-align: {text_align} !important;
        direction: {direction} !important;
    }}
    
    /* تحسين كل عناصر الـ streamlit بشكل عام */
    .element-container {{
        text-align: {text_align} !important;
        direction: {direction} !important;
    }}
    
    /* تحسين الـ info و warning messages */
    .stInfo, .stWarning, .stSuccess, .stError {{
        text-align: {text_align} !important;
        direction: {direction} !important;
    }}
    
    /* تحسين الـ json viewers */
    .stJson {{
        text-align: {text_align} !important;
        direction: {direction} !important;
    }}
    
    /* تحسين الـ expanders */
    .streamlit-expanderHeader {{
        text-align: {text_align} !important;
        direction: {direction} !important;
    }}
    
    /* تحسين الـ tabs */
    .stTabs [data-baseweb="tab-list"] {{
        flex-direction: {'row-reverse' if direction == 'rtl' else 'row'} !important;
        gap: 2px;
    }}
    
    .stTabs [data-baseweb="tab"] {{
        flex-direction: {'row-reverse' if direction == 'rtl' else 'row'} !important;
    }}
    
    /* تحسين الـ progress bars */
    .stProgress > div > div > div > div {{
        background-color: #1f77b4;
    }}
    
    /* تحسين الـ spinners */
    .stSpinner > div {{
        border-color: #1f77b4 transparent transparent transparent;
    }}
    
    /* تحسين الـ number input */
    .stNumberInput>div>div>input {{
        text-align: {text_align} !important;
        direction: {direction} !important;
    }}
    
    /* تحسين الـ date input */
    .stDateInput>div>div>input {{
        text-align: {text_align} !important;
        direction: {direction} !important;
    }}
    
    /* تحسين الـ time input */
    .stTimeInput>div>div>input {{
        text-align: {text_align} !important;
        direction: {direction} !important;
    }}
    
    /* تحسين الـ file uploader */
    .stFileUploader label {{
        text-align: {text_align} !important;
        direction: {direction} !important;
    }}
    
    /* تحسين الـ color picker */
    .stColorPicker label {{
        text-align: {text_align} !important;
        direction: {direction} !important;
    }}
    
    </style>
    """, unsafe_allow_html=True)

def apply_theme_choice(theme_choice):
    """تطبيق السمة المختارة مع الحفاظ على الاتجاه"""
    direction = get_text_direction()
    text_align = 'right' if direction == 'rtl' else 'left'
    
    if theme_choice == "داكن" or theme_choice == "Dark":
        st.markdown(f"""
        <style>
        /* أنماط السمة الداكنة مع اتجاه ديناميكي */
        .main {{
            background-color: #0e1117;
            color: #fafafa;
            direction: {direction};
            text-align: {text_align};
        }}
        
        /* الحفاظ على اتجاه labels في السمة الداكنة */
        label {{
            text-align: {text_align} !important;
            direction: {direction} !important;
            color: #fafafa !important;
        }}
        
        .stTextInput label, 
        .stTextArea label, 
        .stSelectbox label, 
        .stRadio label, 
        .stMultiSelect label {{
            text-align: {text_align} !important;
            direction: {direction} !important;
            color: #fafafa !important;
        }}
        
        h1, h2, h3, h4, h5, h6 {{
            text-align: {text_align} !important;
            direction: {direction} !important;
            color: #fafafa !important;
        }}
        
        .stButton>button {{
            background-color: #262730;
            color: #fafafa;
            border: 1px solid #555;
        }}
        
        .stTextInput>div>div>input, 
        .stTextArea>div>div>textarea {{
            background-color: #262730;
            color: #fafafa;
            border: 1px solid #555;
            text-align: {text_align} !important;
            direction: {direction} !important;
        }}
        
        .stSelectbox>div>div>select {{
            background-color: #262730;
            color: #fafafa;
            text-align: {text_align} !important;
            direction: {direction} !important;
        }}
        
        .step-pill {{
            background-color: #262730;
            color: #fafafa;
        }}
        
        /* الحفاظ على اتجاه النص في السمة الداكنة */
        .stMarkdown, .stText, .stAlert {{
            text-align: {text_align} !important;
            direction: {direction} !important;
            color: #fafafa !important;
        }}
        
        div[data-testid="stRadio"] > div {{
            flex-direction: {'row-reverse' if direction == 'rtl' else 'row'} !important;
            justify-content: {'flex-end' if direction == 'rtl' else 'flex-start'} !important;
        }}
        
        .row-widget.stColumns {{
            flex-direction: {'row-reverse' if direction == 'rtl' else 'row'} !important;
        }}
        
        /* تحسين الـ sidebar في السمة الداكنة */
        section[data-testid="stSidebar"] {{
            background-color: #0e1117 !important;
            color: #fafafa !important;
        }}
        
        </style>
        """, unsafe_allow_html=True)
    else:
        # السمة الفاتحة (الافتراضية)
        apply_base_styles()

def apply_direction_styles():
    """تطبيق أنماط الاتجاه فقط - حل سريع للمشاكل"""
    direction = get_text_direction()
    text_align = 'right' if direction == 'rtl' else 'left'
    
    st.markdown(f"""
    <style>
    /* حل سريع لكل الـ labels والعناوين */
    label, h1, h2, h3, h4, h5, h6 {{
        text-align: {text_align} !important;
        direction: {direction} !important;
        width: 100% !important;
    }}
    
    /* حل سريع لكل النصوص */
    .stMarkdown, .stText, .stAlert, .stCaption {{
        text-align: {text_align} !important;
        direction: {direction} !important;
    }}
    
    /* حل سريع للحقول */
    .stTextInput>div>div>input, 
    .stTextArea>div>div>textarea,
    .stSelectbox>div>div>select {{
        text-align: {text_align} !important;
        direction: {direction} !important;
    }}
    
    /* حل سريع للـ radio buttons */
    div[data-testid="stRadio"] > div {{
        flex-direction: {'row-reverse' if direction == 'rtl' else 'row'} !important;
        justify-content: {'flex-end' if direction == 'rtl' else 'flex-start'} !important;
    }}
    
    /* حل سريع للأعمدة */
    .row-widget.stColumns {{
        flex-direction: {'row-reverse' if direction == 'rtl' else 'row'} !important;
    }}
    
    </style>
    """, unsafe_allow_html=True)

def apply_custom_styles():
    """تطبيق كل الأنماط المخصصة"""
    apply_base_styles()
    apply_direction_styles()