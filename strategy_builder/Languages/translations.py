# strategy_builder/Languages/translations.py
# -*- coding: utf-8 -*-
"""
نظام الترجمة متعدد اللغات
"""

TRANSLATIONS = {
    "ar": {
        # القائمة الرئيسية
        "app_title": "🗂️ مدير الاستراتيجيات",
        "new_strategy": "🏗️ بناء/تعديل استراتيجية",
        "browse_strategies": "📂 استعراض/إدارة الاستراتيجيات",
        "resume_session": "⏯️ استكمال آخر جلسة",
        "settings": "⚙️ الإعدادات",
        "choose_option": "اختر:",
        
        # الإجراءات
        "create_new": "إنشاء استراتيجية جديدة",
        "load_existing": "تحميل استراتيجية محفوظة للتعديل",
        "choose_action": "اختيار الإجراء:",
        "start_over": "🔄 ابدأ من جديد",
        
        # الاستراتيجيات
        "no_strategies": "لا توجد استراتيجيات محفوظة بعد.",
        "choose_strategy": "اختر استراتيجية",
        "saved_strategies": "📂 الاستراتيجيات المحفوظة",
        "strategy_name": "اسم الاستراتيجية",
        "creation_date": "تاريخ الإنشاء",
        "vision": "الرؤية",
        "mission": "الرسالة",
        "goals": "الأهداف",
        "values": "القيم",
        
        # الأزرار
        "edit": "✏️ تعديل",
        "delete": "🗑️ حذف",
        "clone": "📄 نسخ (Clone)",
        "export_word": "📤 تصدير Word",
        "export_pdf": "📤 تصدير PDF",
        "download": "تحميل",
        
        # البحث والتصفية
        "search": "🔎 بحث بالاسم",
        "filter_date": "📅 من تاريخ",
        "sort_by": "📊 ترتيب حسب",
        "newest_first": "🆕 الأحدث أولًا",
        "oldest_first": "🕰️ الأقدم أولًا",
        "name_az": "🔤 الاسم (A→Z)",
        "name_za": "🔤 الاسم (Z→A)",
        "no_results": "لا توجد نتائج مطابقة.",
        
        # الرسائل
        "strategy_deleted": "🚮 تم حذف الاستراتيجية",
        "strategy_cloned": "✅ تم إنشاء نسخة",
        "no_saved_session": "لا توجد جلسة محفوظة.",
        "strategy_not_found": "لم يتم العثور على الاستراتيجية الأخيرة.",
        
        # معلومات النظام
        "current_logo": "الشعار الحالي:",
        "preferred_font": "خط PDF المفضل:",
        "using_bank": "سيتم استخدام بنك الاستراتيجية:",
        "bank_not_found": "⚠️ لم يتم العثور على ملف بنك الاستراتيجية داخل assets. توجه إلى صفحة الإعدادات (⚙️) لرفعه.",

        # السايدبار والإعدادات
        "theme": "🎨 السمة",
        "light": "فاتح", 
        "dark": "داكن",
        "pdf_font": "خط PDF",
        "logo": "الشعار",
        "change_in_settings": "للتغيير: انتقل إلى ⚙️ الإعدادات من القائمة.",

        # الويزارد
        "step": "الخطوة",
        "save_name": "💾 حفظ الاسم",
        "name_saved": "تم حفظ الاسم.",
        "strategy_will_create": "سيتم إنشاء الاستراتيجية عند حفظ أول خطوة.",

        "select_vision_from_bank": "اختر رؤية من البنك",
        "select": "اختر",
        "edit_enter_vision": "✏️ تعديل/إدخال رؤية",
        "back": "السابق",
        "next": "التالي",
        "default_strategy_name": "استراتيجية",
        "vision_required": "⚠️ يجب إدخال أو اختيار رؤية قبل الانتقال للخطوة التالية",

        "missions_linked_to_vision": "الرسائل المرتبطة بالرؤية", 
        "edit_enter_mission": "✏️ تعديل/إدخال رسالة",
        "mission_required": "⚠️ يجب إدخال أو اختيار رسالة قبل الانتقال للخطوة التالية",

        "goals_linked_to_mission": "🎯 أهداف مرتبطة بهذه الرسالة",
        "goals_from_bank": "📚 أهداف من بنك الأهداف (كل البنك)",
        "add_new_goal": "➕ أضف هدف (اختياري)",
        "edit_selected_goals": "✏️ عدّل صياغة الأهداف المختارة", 
        "at_least_one_goal": "⚠️ يجب اختيار أو إدخال هدف واحد على الأقل",

        "values_linked_to_mission": "⭐ قيم مرتبطة بهذه الرسالة",
        "values_from_bank": "📚 قيم من بنك القيم (كل البنك)",
        "add_new_value": "➕ أضف قيمة (اختياري)",
        "edit_selected_values": "✏️ عدّل صياغة القيم المختارة",
        "at_least_one_value": "⚠️ يجب اختيار أو إدخال قيمة واحدة على الأقل",

        "review": "مراجعة",
        "review_export": "المراجعة والتصدير",
        "download_word": "تحميل Word",
        "download_pdf": "تحميل PDF",

        # التصدير
        "export_success": "تم التصدير بنجاح",
        "export_error": "حدث خطأ أثناء التصدير",

        # الإعدادات
        "language_settings": "إعدادات اللغة",
        "appearance_settings": "إعدادات المظهر",
        "export_settings": "إعدادات التصدير",
        "upload_bank": "رفع ملف البنك",
        "upload_logo": "رفع شعار",
        "select_font": "اختر خط PDF",
        "save_settings": "💾 حفظ الإعدادات",
        "settings_saved": "تم حفظ الإعدادات بنجاح",
        "browse_files": "تصفح الملفات",
        "drag_drop": "اسحب وأفلت الملف هنا",
        "supported_formats": "الصيغ المدعومة",
        "choose_language": "اختر اللغة",
        "language_updated": "تم تحديث اللغة بنجاح",
        "logo_upload_success": "تم رفع الشعار بنجاح",
        "bank_upload_success": "تم رفع ملف البنك بنجاح",
        "no_fonts_available": "⚠️ لا توجد خطوط متاحة في مجلد fonts",

        # رسائل التأكيد
        "confirm_delete": "هل أنت متأكد من الحذف؟",
        "yes": "نعم",
        "no": "لا",
        "cancel": "إلغاء",
        "confirm": "تأكيد",

        # حالات النظام
        "loading": "جاري التحميل...",
        "saving": "جاري الحفظ...",
        "processing": "جاري المعالجة...",
        "success": "تم بنجاح",
        "error": "خطأ",
        "warning": "تحذير",
        "info": "معلومة"
    },
    "en": {
        # Main Menu
        "app_title": "🗂️ Strategy Manager",
        "new_strategy": "🏗️ Build/Edit Strategy",
        "browse_strategies": "📂 Browse/Manage Strategies",
        "resume_session": "⏯️ Resume Last Session",
        "settings": "⚙️ Settings",
        "choose_option": "Choose:",
        
        # Actions
        "create_new": "Create New Strategy",
        "load_existing": "Load Saved Strategy for Editing",
        "choose_action": "Choose Action:",
        "start_over": "🔄 Start Over",
        
        # Strategies
        "no_strategies": "No saved strategies yet.",
        "choose_strategy": "Choose Strategy",
        "saved_strategies": "📂 Saved Strategies",
        "strategy_name": "Strategy Name",
        "creation_date": "Creation Date",
        "vision": "Vision",
        "mission": "Mission",
        "goals": "Goals",
        "values": "Values",
        
        # Buttons
        "edit": "✏️ Edit",
        "delete": "🗑️ Delete",
        "clone": "📄 Clone",
        "export_word": "📤 Export Word",
        "export_pdf": "📤 Export PDF",
        "download": "Download",
        
        # Search & Filter
        "search": "🔎 Search by Name",
        "filter_date": "📅 From Date",
        "sort_by": "📊 Sort By",
        "newest_first": "🆕 Newest First",
        "oldest_first": "🕰️ Oldest First",
        "name_az": "🔤 Name (A→Z)",
        "name_za": "🔤 Name (Z→A)",
        "no_results": "No matching results.",
        
        # Messages
        "strategy_deleted": "🚮 Strategy deleted",
        "strategy_cloned": "✅ Copy created",
        "no_saved_session": "No saved session.",
        "strategy_not_found": "Last strategy not found.",
        
        # System Info
        "current_logo": "Current Logo:",
        "preferred_font": "Preferred PDF Font:",
        "using_bank": "Using strategy bank:",
        "bank_not_found": "⚠️ Strategy bank file not found in assets. Go to Settings (⚙️) to upload.",

        # Sidebar & Settings
        "theme": "🎨 Theme",
        "light": "Light",
        "dark": "Dark",
        "pdf_font": "PDF Font",
        "logo": "Logo",
        "change_in_settings": "To change: go to ⚙️ Settings from the menu.",

        # Wizard
        "step": "Step",
        "save_name": "💾 Save Name",
        "name_saved": "Name saved.",
        "strategy_will_create": "Strategy will be created when saving first step.",

        "select_vision_from_bank": "Select vision from bank",
        "select": "Select",
        "edit_enter_vision": "✏️ Edit/Enter vision",
        "back": "Back",
        "next": "Next",
        "default_strategy_name": "Strategy",
        "vision_required": "⚠️ Must enter or select a vision before proceeding",

        "missions_linked_to_vision": "Missions linked to vision",
        "edit_enter_mission": "✏️ Edit/Enter mission",
        "mission_required": "⚠️ Must enter or select a mission before proceeding",

        "goals_linked_to_mission": "🎯 Goals linked to this mission",
        "goals_from_bank": "📚 Goals from goals bank (all bank)",
        "add_new_goal": "➕ Add new goal (optional)",
        "edit_selected_goals": "✏️ Edit selected goals wording",
        "at_least_one_goal": "⚠️ Must select or enter at least one goal",

        "values_linked_to_mission": "⭐ Values linked to this mission",
        "values_from_bank": "📚 Values from values bank (all bank)",
        "add_new_value": "➕ Add new value (optional)",
        "edit_selected_values": "✏️ Edit selected values wording",
        "at_least_one_value": "⚠️ Must select or enter at least one value",

        "review": "Review",
        "review_export": "Review & Export",
        "download_word": "Download Word",
        "download_pdf": "Download PDF",

        # Export
        "export_success": "Export completed successfully",
        "export_error": "Error occurred during export",

        # Settings
        "language_settings": "Language Settings",
        "appearance_settings": "Appearance Settings",
        "export_settings": "Export Settings",
        "upload_bank": "Upload Bank File",
        "upload_logo": "Upload Logo",
        "select_font": "Select PDF Font",
        "save_settings": "💾 Save Settings",
        "settings_saved": "Settings saved successfully",
        "browse_files": "Browse Files",
        "drag_drop": "Drag and drop file here",
        "supported_formats": "Supported formats",
        "choose_language": "Choose Language",
        "language_updated": "Language updated successfully",
        "logo_upload_success": "Logo uploaded successfully",
        "bank_upload_success": "Bank file uploaded successfully",
        "no_fonts_available": "⚠️ No fonts available in fonts folder",

        # Confirmation Messages
        "confirm_delete": "Are you sure you want to delete?",
        "yes": "Yes",
        "no": "No",
        "cancel": "Cancel",
        "confirm": "Confirm",

        # System Status
        "loading": "Loading...",
        "saving": "Saving...",
        "processing": "Processing...",
        "success": "Success",
        "error": "Error",
        "warning": "Warning",
        "info": "Info"
    }
}

SUPPORTED_LANGUAGES = {
    "ar": "العربية",
    "en": "English"
}

def get_translation(lang: str, key: str) -> str:
    """Get translation for key in specified language"""
    return TRANSLATIONS.get(lang, {}).get(key, key)

def get_available_languages():
    """Get supported languages"""
    return SUPPORTED_LANGUAGES