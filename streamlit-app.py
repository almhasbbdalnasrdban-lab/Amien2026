import streamlit as st
import random
from datetime import datetime

# إعدادات الصفحة
st.set_page_config(page_title="محفظة الأمين - المحاسب عبدالناصر", page_icon="💳", layout="centered")

# تنسيقات CSS لجعل الأزرار والدوائر أنيقة وشبيهة بالتطبيقات الحديثة
st.markdown("""
<style>
    .stButton>button {
        border-radius: 20px;
        background-color: #FFD700;
        color: #3B3226;
        font-weight: bold;
        border: none;
        padding: 10px 20px;
        box-shadow: 0px 4px 6px rgba(0,0,0,0.1);
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #B8860B;
        color: white;
    }
    .balance-card {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        padding: 20px;
        border-radius: 25px;
        text-align: center;
        margin-bottom: 15px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.15);
    }
    .trans-card {
        background-color: #f8f9fa;
        border-right: 5px solid #FFD700;
        padding: 12px;
        border-radius: 10px;
        margin-bottom: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        color: #333;
    }
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #111111;
        color: #FFD700;
        text-align: center;
        padding: 8px;
        font-weight: bold;
        font-family: sans-serif;
        font-size: 14px;
        z-index: 100;
    }
</style>
""", unsafe_allow_html=True)

# التهيئة للجلسة
if 'real_transactions' not in st.session_state:
    st.session_state.real_transactions = []
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_info' not in st.session_state:
    st.session_state.user_info = {}

# الشعار والعنوان الرئيسية
st.markdown("<h1 style='text-align: center; color: #B8860B;'>💳 محفظة الأمين 💳</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: #555;'>تسهيل وحماية - خدمات مالية متكاملة</h4>", unsafe_allow_html=True)
st.divider()

# شاشة الدخول والتسجيل
if not st.session_state.logged_in:
    auth_mode = st.radio("اختر نوع الإجراء:", ["تسجيل الدخول", "فتح حساب جديد (تعبئة البيانات)"], horizontal=True)
    
    if auth_mode == "تسجيل الدخول":
        st.subheader("🔑 تسجيل الدخول")
        phone = st.text_input("رقم الجوال")
        pin = st.text_input("رمز الحماية (PIN)", type="password")
        if st.button("دخول إلى المحفظة", use_container_width=True):
            if phone.strip() != "" and pin.strip() != "":
                st.session_state.logged_in = True
                st.session_state.user_info['phone'] = phone
                st.success("تم تسجيل الدخول بنجاح!")
                st.rerun()
            else:
                st.error("الرجاء إدخال رقم الجوال ورمز الحماية!")
                
    else:
        st.subheader("📝 فتح حساب جديد وتوثيق الهوية")
        full_name = st.text_input("الاسم الرباعي الكامل")
        id_card = st.text_input("رقم الهوية / البطاقة الشخصية")
        address = st.text_input("عنوان السكن الحالي")
        user_phone = st.text_input("رقم الجوال للتواصل")
        new_pin = st.text_input("أنشئ رمز حماية (PIN)", type="password")
        
        terms = st.checkbox("أوافق على اتفاقية استخدام محفظة الأمين والشروط والأحكام المالية")
        
        if st.button("تأكيد إنشاء الحساب وتوثيقه", use_container_width=True):
            if full_name and id_card and address and user_phone and new_pin and terms:
                st.session_state.user_info = {
                    'name': full_name,
                    'id': id_card,
                    'address': address,
                    'phone': user_phone
                }
                st.session_state.logged_in = True
                st.success("تم فتح الحساب وتوثيق البيانات بنجاح!")
                st.rerun()
            else:
                st.error("يرجى تعبئة كافة البيانات والموافقة على اتفاقية الاستخدام!")

else:
    # القائمة الجانبية ومعلومات التواصل
    st.sidebar.title("👤 حساب المشترك")
    if 'name' in st.session_state.user_info:
        st.sidebar.info(f"**المستخدم:** {st.session_state.user_info['name']}")
    st.sidebar.write(f"**رقم الجوال:** {st.session_state.user_info.get('phone', 'غير محدد')}")
    st.sidebar.divider()
    
    st.sidebar.subheader("📞 الدعم والاستفسارات")
    st.sidebar.success("للتواصل المباشر مع إدارة المحفظة:")
    st.sidebar.markdown("📱 **774409810**")
    
    if st.sidebar.button("🚪 تسجيل الخروج", use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()

    # شاشة الأرصدة المتناقلة (دوائر/بطاقات)
    st.subheader("💰 الأرصدة المتاحة")
    curr_tab = st.radio("اختر العملة للظهور:", ["🇾🇪 رصيد يمني (YER)", "🇸🇦 رصيد سعودي (SAR)", "🇺🇸 رصيد دولار (USD)"], horizontal=True)
    
    if "يمني" in curr_tab:
        st.markdown("<div class='balance-card'><h3>الرصيد بالريال اليمني</h3><h2>250,000 ر.ي</h2></div>", unsafe_allow_html=True)
    elif "سعودي" in curr_tab:
        st.markdown("<div class='balance-card'><h3>الرصيد بالريال السعودي</h3><h2>3,500 ر.س</h2></div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='balance-card'><h3>الرصيد بالدولار الأمريكي</h3><h2>1,000 $</h2></div>", unsafe_allow_html=True)

    # التبويبات والخدمات المالية المكتملة
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "💸 تحويل أموال", 
        "📱 فواتير واتصالات", 
        "📞 ثابت وإنترنت", 
        "🛒 مشتريات وتجار", 
        "📥 إيداع رصيد", 
        "📄 كشف الحساب"
    ])

    # 1. تحويل أموال
    with tab1:
        st.subheader("💸 خدمة التحويلات المالية")
        ep = st.text_input("رقم مستلم الحوالة", key="trans_phone")
        ea = st.text_input("المبلغ المراد تحويله", key="trans_amt")
        curr = st.selectbox("العملة", ["ريال يمني", "ريال سعودي", "دولار أمريكي"], key="c1")
        if st.button("تأكيد إرسال الحوالة", key="btn_trans", use_container_width=True):
            if ep == "" or ea == "":
                st.error("أدخل بيانات التحويل كاملة")
            else:
                trans_no = random.randint(100000, 999999)
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
                st.session_state.real_transactions.append(f"[{current_time}] تحويل مبلغ {ea} {curr} إلى المستلم ({ep}) - رقم العملية: #{trans_no}")
                st.success(f"تم تحويل {ea} {curr} بنجاح إلى {ep}\n\nرقم الحوالة المعتمد: {trans_no}")

    # 2. تسديد الفواتير والاتصالات
    with tab2:
        st.subheader("📱 سداد فواتير الشحن والاتصالات")
        service = st.selectbox("اختر الشركة / الخدمة", ["يمن موبايل (باقات/رصيد)", "سبأفون", "YOU / MTN", "واي (Y)", "كهرباء / ماء"])
        eb = st.text_input("رقم الهاتف / رقم الاشتراك", key="bill_phone")
        eamt = st.text_input("المبلغ (ر.ي)", key="bill_amt")
        if st.button("تأكيد دفع الفاتورة", key="btn_bill", use_container_width=True):
            if eb == "" or eamt == "":
                st.error("يرجى إكمال بيانات السداد")
            else:
                bill_no = random.randint(1000000, 9999999)
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
                st.session_state.real_transactions.append(f"[{current_time}] سداد فاتورة {service} الرقم ({eb}) بمبلغ {eamt} ر.ي - رقم العملية: #{bill_no}")
                st.success(f"تم تسديد فاتورة ({service}) للرقم {eb} بقيمة {eamt} ر.ي بنجاح.\nرقم المرجع: {bill_no}")

    # 3. الهاتف الثابت والإنترنت
    with tab3:
        st.subheader("📞 خدمات الهاتف الثابت والإنترنت والبريد")
        net_service = st.selectbox("اختر نوع الخدمة", ["إنترنت ADSL (يمن نت)", "الهاتف الثابت المنزلي", "خدمات البريد وتوفير البريد", "عدن نت"])
        e_num = st.text_input("رقم الحساب / الرقم الثابت", key="net_num")
        e_amt = st.text_input("المبلغ المراد سداده", key="net_amt")
        if st.button("تأكيد سداد الاشتراك", key="btn_net", use_container_width=True):
            if e_num == "" or e_amt == "":
                st.error("الرجاء إدخال البيانات كاملة")
            else:
                op_no = random.randint(200000, 999999)
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
                st.session_state.real_transactions.append(f"[{current_time}] سداد اشتراك {net_service} للرقم ({e_num}) بمبلغ {e_amt} ر.ي - رقم السداد: #{op_no}")
                st.success(f"تم سداد {net_service} بنجاح للرقم {e_num}\nالمبلغ: {e_amt} ر.ي (رقم العملية: {op_no})")

    # 4. دفع المشتريات
    with tab4:
        st.subheader("🛒 دفع المشتريات والرسوم للمنشآت والجامعات")
        em = st.text_input("رقم المنشأة / رمز التاجر (6 أرقام ويبدأ بـ 15)", key="merch_id")
        emoney = st.text_input("المبلغ (ر.ي)", key="merch_amt")
        if st.button("تأكيد عملية الدفع للتاجر", key="btn_merch", use_container_width=True):
            entered_code = em.strip()
            if entered_code == "" or emoney.strip() == "":
                st.error("الرجاء إدخال رقم المنشأة والمبلغ")
            elif not entered_code.isdigit() or len(entered_code) != 6 or not entered_code.startswith("15"):
                st.error("رقم المنشأة غير صحيح! يجب أن يتكون من 6 أرقام ويبدأ بالرمز (15).")
            else:
                pay_no = random.randint(500000, 999999)
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
                st.session_state.real_transactions.append(f"[{current_time}] دفع مشتريات للمنشأة رقم ({entered_code}) بمبلغ {emoney} ر.ي - مرجع: #{pay_no}")
                st.success(f"تم دفع {emoney} ر.ي بنجاح للرمز: ({entered_code})\nرقم العملية: {pay_no}")

    # 5. إيداع الرصيد
    with tab5:
        st.subheader("📥 إيداع رصيد وحوالات واردة")
        dep_phone = st.text_input("رقم جوال المودِع", key="dep_phone")
        ben_phone = st.text_input("رقم حساب المستفيد", key="ben_phone")
        amount = st.text_input("المبلغ المراد إيداعه", key="dep_amt")
        if st.button("تأكيد الإيداع وإرسال الإشعار", key="btn_dep", use_container_width=True):
            if dep_phone.strip() == "" or ben_phone.strip() == "" or amount.strip() == "":
                st.error("يرجى تعبئة كافة البيانات")
            else:
                dep_no = random.randint(1000000, 9999999)
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
                st.session_state.real_transactions.append(f"[{current_time}] إيداع مبلغ {amount} ر.ي للحساب ({ben_phone}) من المودع ({dep_phone}) - مرجع: #{dep_no}")
                st.success(f"تمت عملية الإيداع بنجاح 📥\nالمستفيد: {ben_phone}\nالمبلغ: {amount} ر.ي\nرقم العملية: {dep_no}")

    # 6. كشف الحساب الواضح والكامل
    with tab6:
        st.subheader("📄 كشف الحساب والعمليات المنفذة")
        if len(st.session_state.real_transactions) == 0:
            st.info("لا توجد أي عمليات مالية منفذة حتى الآن.")
        else:
            for op in reversed(st.session_state.real_transactions):
                st.markdown(f"<div class='trans-card'>📌 {op}</div>", unsafe_allow_html=True)

# الشريط السفلي الدائم باسم المحاسب
st.markdown("<div class='footer'>Developed by Accountant Abdulnasser</div>", unsafe_allow_html=True)
