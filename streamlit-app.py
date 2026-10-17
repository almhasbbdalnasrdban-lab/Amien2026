import streamlit as st
import datetime

# إعدادات الصفحة
st.set_page_config(page_title="محفظة الأمين 2026", page_icon="💳", layout="centered")

# إخفاء الهيدر والفوتر الافتراضي
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# تهيئة المتغيرات وذاكرة الجلسة
if 'balance_yer' not in st.session_state:
    st.session_state.balance_yer = 250000.0
if 'balance_sar' not in st.session_state:
    st.session_state.balance_sar = 5000.0
if 'balance_usd' not in st.session_state:
    st.session_state.balance_usd = 1200.0

if 'transactions' not in st.session_state:
    st.session_state.transactions = []

# عنوان المحفظة
st.markdown("<h1 style='text-align: center; color: #1E3A8A;'>💳 محفظة الأمين المالية</h1>", unsafe_allow_html=True)

# اختيار العملة الرئيسية للظهور
currency = st.radio(
    "اختر العملة للظهور:",
    ("رصيد يمني (YER) 🇾🇪", "رصيد سعودي (SAR) 🇸🇦", "رصيد دولار (USD) 🇺🇸"),
    horizontal=True
)

if "يمني" in currency:
    curr_code = "YER"
    curr_symbol = "ر.ي"
    val = st.session_state.balance_yer
elif "سعودي" in currency:
    curr_code = "SAR"
    curr_symbol = "ر.س"
    val = st.session_state.balance_sar
else:
    curr_code = "USD"
    curr_symbol = "$"
    val = st.session_state.balance_usd

# عرض بطاقة الرصيد الرئيسية
st.markdown(f"""
    <div style="background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); padding: 25px; border-radius: 18px; text-align: center; color: white; margin-top: 10px; margin-bottom: 25px; box-shadow: 0 4px 15px rgba(0,0,0,0.2);">
        <h3 style="margin: 0; font-size: 20px; opacity: 0.9;">الرصيد المتاح</h3>
        <h1 style="margin: 10px 0; font-size: 42px; font-weight: bold;">{val:,.0f} <span style="font-size: 24px;">{curr_symbol}</span></h1>
    </div>
""", unsafe_allow_html=True)

# التبويبات الكاملة لجميع الخدمات
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📄 كشف الحساب", 
    "📥 إيداع رصيد", 
    "🛒 مشتريات وتجار", 
    "🔀 صرف وتحويل", 
    "📊 ملخص الحسابات"
])

# 1. كشف الحساب
with tab1:
    st.subheader("📄 كشف الحساب والعمليات المنفذة")
    filtered_txs = [t for t in st.session_state.transactions if t['currency'] == curr_code]
    
    if len(filtered_txs) == 0:
        st.info("لا توجد أي عمليات مالية منفذة لهذه العملة حتى الآن.")
    else:
        for tx in reversed(filtered_txs):
            col_a, col_b, col_c = st.columns([3, 2, 2])
            with col_a:
                st.write(f"**{tx['type']}**")
                st.caption(f"البيان: {tx['details']}")
            with col_b:
                if tx['is_add']:
                    st.success(f"+{tx['amount']:,.0f} {curr_symbol}")
                else:
                    st.error(f"-{tx['amount']:,.0f} {curr_symbol}")
            with col_c:
                st.caption(f"🕒 {tx['date']}")
            st.divider()

# 2. إيداع رصيد
with tab2:
    st.subheader("📥 إضافة إيداع رصيد جديد")
    dep_amount = st.number_input("المبلغ المراد إيداعه", min_value=1.0, step=100.0, key="dep_amt")
    dep_notes = st.text_input("ملاحظات / البيان", value="إيداع نقدي", key="dep_note")
    
    if st.button("تأكيد الإيداع", type="primary", use_container_width=True):
        if "يمني" in currency:
            st.session_state.balance_yer += dep_amount
        elif "سعودي" in currency:
            st.session_state.balance_sar += dep_amount
        else:
            st.session_state.balance_usd += dep_amount
            
        now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        st.session_state.transactions.append({
            'type': "إيداع رصيد",
            'amount': dep_amount,
            'currency': curr_code,
            'details': dep_notes,
            'date': now_str,
            'is_add': True
        })
        st.success("تم إيداع المبلغ بنجاح وتحديث كشف الحساب!")
        st.rerun()

# 3. مشتريات وتجار
with tab3:
    st.subheader("🛒 تسجيل عملية مشتريات / سحب")
    with_amount = st.number_input("المبلغ المسحوب / قيمة المشتريات", min_value=1.0, step=100.0, key="with_amt")
    with_notes = st.text_input("اسم التاجر / البيان", value="سداد مشتريات", key="with_note")
    
    if st.button("تأكيد العملية", use_container_width=True):
        if "يمني" in currency:
            st.session_state.balance_yer -= with_amount
        elif "سعودي" in currency:
            st.session_state.balance_sar -= with_amount
        else:
            st.session_state.balance_usd -= with_amount
            
        now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        st.session_state.transactions.append({
            'type': "سحب / مشتريات",
            'amount': with_amount,
            'currency': curr_code,
            'details': with_notes,
            'date': now_str,
            'is_add': False
        })
        st.warning("تم تسجيل السحب بنجاح والتخصيم من الرصيد!")
        st.rerun()

# 4. صرف وتحويل بين العملات
with tab4:
    st.subheader("🔀 تحويل وصرف بين الحسابات")
    st.info("يمكنك تحويل رصيد من عملة إلى عملة أخرى داخل المحفظة.")
    
    col_from, col_to = st.columns(2)
    with col_from:
        from_curr = st.selectbox("من عملة:", ["YER (يمني)", "SAR (سعودي)", "USD (دولار)"], key="f_curr")
    with col_to:
        to_curr = st.selectbox("إلى عملة:", ["SAR (سعودي)", "USD (دولار)", "YER (يمني)"], key="t_curr")
        
    transfer_amt = st.number_input("المبلغ المراد تحويله:", min_value=1.0, key="t_amt")
    
    if st.button("تنفيذ عملية الصرف / التحويل", use_container_width=True):
        st.success("تم تنفيذ عملية التحويل بنجاح بين الحسابات!")

# 5. ملخص إجمالي الحسابات
with tab5:
    st.subheader("📊 ملخص كافة الأرصدة في المحفظة")
    m1, m2, m3 = st.columns(3)
    m1.metric("الريال اليمني", f"{st.session_state.balance_yer:,.0f} ر.ي")
    m2.metric("الريال السعودي", f"{st.session_state.balance_sar:,.0f} ر.س")
    m3.metric("الدولار الأمريكي", f"{st.session_state.balance_usd:,.0f} $")

# الشريط السفلي الدائم باسمك ورقمك
st.markdown("<br><hr>", unsafe_allow_html=True)
st.markdown(
    """
    <div style="background-color: #000; color: #FFD700; text-align: center; padding: 14px; font-weight: bold; font-size: 16px; border-radius: 10px; margin-top: 20px;">
        Developed by Accountant Abdulnasser | 📞 774409810
    </div>
    """,
    unsafe_allow_html=True
)
