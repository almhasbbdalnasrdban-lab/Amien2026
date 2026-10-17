```python
import streamlit as st
import pandas as pd
from datetime import datetime

# إعدادات الصفحة
st.set_page_config(page_title="محفظة الأمين 2026", page_icon="💼", layout="centered")

# تحسين تنسيق CSS
st.markdown("""
    <style>
    .main { text-align: right; }
    .stApp { direction: rtl; }
    .card {
        background-color: #1E40AF;
        color: white;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #111827;
        color: #FAC213;
        text-align: center;
        padding: 10px;
        font-weight: bold;
        font-size: 14px;
        z-index: 100;
    }
    </style>
""", unsafe_allow_html=True)

# تهيئة حالة الجلسة (Session State) لحفظ البيانات أثناء الاستخدام
if "balances" not in st.session_state:
    st.session_state.balances = {
        "YER": 250000.0,
        "SAR": 1500.0,
        "USD": 400.0
    }

if "transactions" not in st.session_state:
    st.session_state.transactions = []

# شريط الترويسة والعملة
st.title("💼 محفظة الأمين 2026")
currency = st.radio(
    "اختر العملة للظهور:",
    ["🇾🇪 رصيد يمني (YER)", "🇸🇦 رصيد سعودي (SAR)", "🇺🇸 رصيد دولار (USD)"],
    horizontal=True
)

curr_code = "YER"
curr_symbol = "ر.ي"
if "سعودي" in currency:
    curr_code = "SAR"
    curr_symbol = "ر.س"
elif "دولار" in currency:
    curr_code = "USD"
    curr_symbol = "$"

# عرض بطاقة الرصيد
current_balance = st.session_state.balances[curr_code]
st.markdown(f"""
    <div class="card">
        <h2>الرصيد بالـ {currency.split('(')[0].replace('🇾🇪','').replace('🇸🇦','').replace('🇺🇸','')}</h2>
        <h1>{current_balance:,.2f} {curr_symbol}</h1>
    </div>
""", unsafe_allow_html=True)

# التبويبات للخدمات
tab1, tab2, tab3, tab4 = st.tabs(["📄 كشف الحساب", "📥 إيداع رصيد", "🛒 مشتريات وتجار", "⚡ خدمات أخرى"])

# 1. كشف الحساب
with tab1:
    st.header("📄 كشف الحساب والعمليات المنفذة")
    
    # تصفية العمليات حسب العملة المختارة
    filtered_txs = [t for t in st.session_state.transactions if t["العملة"] == curr_code]
    
    if filtered_txs:
        df = pd.DataFrame(filtered_txs)
        # إخفاء العمود المخصص للعملة عند العرض
        st.dataframe(df[["التاريخ", "نوع العملية", "المبلغ", "البيان / التفاصيل"]], use_container_width=True)
    else:
        st.info("لا توجد أي عمليات مالية منفذة حتى الآن بهذه العملة.")

# 2. إيداع رصيد
with tab2:
    st.subheader("📥 إضافة إيداع جديد")
    amount_dep = st.number_input("المبلغ المراد إيداعه:", min_value=1.0, step=100.0, key="dep_amt")
    details_dep = st.text_input("بيان الإيداع / المصدر:", key="dep_det")
    
    if st.button("تأكيد الإيداع"):
        st.session_state.balances[curr_code] += amount_dep
        new_tx = {
            "التاريخ": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "نوع العملية": "إيداع (+)",
            "المبلغ": f"{amount_dep:,.2f} {curr_symbol}",
            "البيان / التفاصيل": details_dep if details_dep else "إيداع نقدي",
            "العملة": curr_code
        }
        st.session_state.transactions.insert(0, new_tx)
        st.success("تم تسجيل الإيداع بنجاح والتحديث في الكشف!")
        st.rerun()

# 3. مشتريات وتجار
with tab3:
    st.subheader("🛒 تسجيل عملية شراء / سداد")
    amount_pay = st.number_input("المبلغ:", min_value=1.0, step=100.0, key="pay_amt")
    vendor = st.text_input("اسم التاجر / الجهة:", key="pay_ven")
    
    if st.button("تأكيد العملية"):
        if amount_pay > st.session_state.balances[curr_code]:
            st.error("الرصيد لا يكفي لإتمام هذه العملية!")
        else:
            st.session_state.balances[curr_code] -= amount_pay
            new_tx = {
                "التاريخ": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "نوع العملية": "سداد (-)",
                "المبلغ": f"{amount_pay:,.2f} {curr_symbol}",
                "البيان / التفاصيل": f"سداد لـ: {vendor}" if vendor else "مشتريات",
                "العملة": curr_code
            }
            st.session_state.transactions.insert(0, new_tx)
            st.success("تم خصم المبلغ وتسجيل العملية بنجاح!")
            st.rerun()

# 4. خدمات أخرى
with tab4:
    st.subheader("⚡ خدمات مالية ومحاسبية بسرعة")
    st.write("• تحويل بين الحسابات")
    st.write("• تسوية الفروقات والتصريف")
    st.write("• طباعة وتقارير PDF")

# الشريط السفلي (Footer)
st.markdown("""
    <div class="footer">
        Developed by Accountant Abdulnasser | 📞 774409810
    </div>
""", unsafe_allow_html=True)
```
