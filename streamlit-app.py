import streamlit as st

# ضبط إعدادات الصفحة
st.set_page_config(page_title="محفظة الأمين 2026", page_icon="💰", layout="centered")

# إخفاء القوائم الإضافية لتقليل التشتت
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# تهيئة ذاكرة الجلسة لحفظ العمليات والأرصدة
if 'balance_yer' not in st.session_state:
    st.session_state.balance_yer = 250000.0
if 'balance_sar' not in st.session_state:
    st.session_state.balance_sar = 5000.0
if 'balance_usd' not in st.session_state:
    st.session_state.balance_usd = 1200.0

if 'transactions' not in st.session_state:
    st.session_state.transactions = []

# اختيار العملة
currency = st.radio(
    ":اختر العملة للظهور",
    ("رصيد يمني (YER) 🇾🇪", "رصيد سعودي (SAR) 🇸🇦", "رصيد دولار (USD) 🇺🇸"),
    horizontal=True
)

# عرض البطاقة بحسب العملة المختارة
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

st.markdown(f"""
    <div style="background-color: #1E40AF; padding: 25px; border-radius: 15px; text-align: center; color: white; margin-bottom: 25px;">
        <h2 style="margin: 0; font-size: 24px;">الرصيد بالعملة المختارة</h2>
        <h1 style="margin: 10px 0; font-size: 40px; font-weight: bold;">{val:,.0f} {curr_symbol}</h1>
    </div>
""", unsafe_allow_html=True)

# التبويبات
tab1, tab2, tab3 = st.tabs(["📄 كشف الحساب", "📥 إيداع رصيد", "🛒 مشتريات وتحويلات"])

with tab1:
    st.subheader("📄 كشف الحساب والعمليات المنفذة")
    
    # تصفية العمليات حسب العملة المختارة
    filtered_txs = [t for t in st.session_state.transactions if t['currency'] == curr_code]
    
    if len(filtered_txs) == 0:
        st.info(".لا توجد أي عمليات مالية منفذة حتى الآن")
    else:
        for tx in reversed(filtered_txs):
            col_a, col_b, col_c = st.columns([2, 2, 2])
            with col_a:
                st.write(f"**{tx['type']}**")
                st.caption(tx['details'])
            with col_b:
                if tx['type'] == "إيداع":
                    st.success(f"+{tx['amount']:,.0f} {curr_symbol}")
                else:
                    st.error(f"-{tx['amount']:,.0f} {curr_symbol}")
            with col_c:
                st.caption(tx['date'])
            st.divider()

with tab2:
    st.subheader("📥 إضافة إيداع جديد")
    dep_amount = st.number_input("المبلغ المراد إيداعه", min_value=1.0, step=100.0, key="dep_amt")
    dep_notes = st.text_input("ملاحظات / البيان", value="إيداع نقدي", key="dep_note")
    
    if st.button("تأكيد الإيداع", type="primary"):
        if "يمني" in currency:
            st.session_state.balance_yer += dep_amount
        elif "سعودي" in currency:
            st.session_state.balance_sar += dep_amount
        else:
            st.session_state.balance_usd += dep_amount
            
        import datetime
        now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        
        st.session_state.transactions.append({
            'type': "إيداع",
            'amount': dep_amount,
            'currency': curr_code,
            'details': dep_notes,
            'date': now_str
        })
        st.success("تم تسجيل عملية الإيداع بنجاح!")
        st.rerun()

with tab3:
    st.subheader("🛒 تسجيل عملية سحب / مشتريات")
    with_amount = st.number_input("المبلغ المسحوب", min_value=1.0, step=100.0, key="with_amt")
    with_notes = st.text_input("البيان / سبب السحب", value="سحب نقدي", key="with_note")
    
    if st.button("تأكيد العملية"):
        if "يمني" in currency:
            st.session_state.balance_yer -= with_amount
        elif "سعودي" in currency:
            st.session_state.balance_sar -= with_amount
        else:
            st.session_state.balance_usd -= with_amount
            
        import datetime
        now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        
        st.session_state.transactions.append({
            'type': "سحب / مصروفات",
            'amount': with_amount,
            'currency': curr_code,
            'details': with_notes,
            'date': now_str
        })
        st.warning("تم تسجيل العملية بنجاح!")
        st.rerun()

# الشريط السفلي
st.markdown("---")
st.markdown(
    """
    <div style="background-color: #000; color: #FFD700; text-align: center; padding: 12px; font-weight: bold; font-size: 16px; border-radius: 8px;">
        Developed by Accountant Abdulnasser | 📞 774409810
    </div>
    """,
    unsafe_allow_html=True
)
