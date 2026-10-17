import streamlit as st
import random
from datetime import datetime

# إعدادات الصفحة
st.set_page_config(page_title="محفظة الأمين", page_icon="💰", layout="centered")

# التهيئة لسجل العمليات في الجلسة
if 'real_transactions' not in st.session_state:
    st.session_state.real_transactions = []

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# الشعار والعنوان
st.markdown("<h1 style='text-align: center; color: #B8860B;'>💛 محفظة الأمين 💛</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #D4AF37;'>تسهيل وحماية</h3>", unsafe_allow_html=True)
st.divider()

# شاشة تسجيل الدخول
if not st.session_state.logged_in:
    st.subheader("🔑 تسجيل الدخول")
    phone = st.text_input("رقم الجوال")
    pin = st.text_input("رمز الحماية (PIN)", type="password")
    
    if st.button("تسجيل الدخول", use_container_width=True):
        if phone.strip() != "" and pin.strip() != "":
            st.session_state.logged_in = True
            st.success("تم تسجيل الدخول بنجاح!")
            st.rerun()
        else:
            st.error("الرجاء إدخال رقم الجوال ورمز الحماية!")

else:
    # القائمة الجانبية والمعلومات
    st.sidebar.success("تم تسجيل الدخول")
    st.sidebar.markdown("### 💰 الرصيد المتاح: **250,000 ر.ي**")
    if st.sidebar.button("🚪 تسجيل الخروج"):
        st.session_state.logged_in = False
        st.rerun()

    # خيارات الخدمات
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "💸 تحويل", 
        "📱 فواتير", 
        "📞 ثابت وإنترنت", 
        "🛒 مشتريات", 
        "📥 إيداع", 
        "📄 كشف حساب"
    ])

    # 1. تحويل أموال
    with tab1:
        st.subheader("💸 تحويل أموال")
        ep = st.text_input("رقم المستلم", key="trans_phone")
        ea = st.text_input("المبلغ (ر.ي)", key="trans_amt")
        if st.button("تأكيد التحويل", key="btn_trans", use_container_width=True):
            if ep == "" or ea == "":
                st.error("أدخل البيانات كاملة")
            else:
                trans_no = random.randint(100000, 999999)
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
                st.session_state.real_transactions.append(f"[{current_time}] تحويل {ea} ر.ي إلى {ep} (رقم: {trans_no})")
                st.success(f"تم تحويل {ea} ر.ي بنجاح إلى {ep}\n\nرقم الحوالة: {trans_no}")

    # 2. تسديد الفواتير
    with tab2:
        st.subheader("📱 تسديد الفواتير والاتصالات")
        service = st.selectbox("اختر الخدمة", ["يمن موبايل", "سبأفون", "YOU / MTN", "كهرباء / ماء"])
        eb = st.text_input("رقم الاشتراك / الهاتف", key="bill_phone")
        eamt = st.text_input("المبلغ (ر.ي)", key="bill_amt")
        if st.button("دفع الفاتورة", key="btn_bill", use_container_width=True):
            if eb == "" or eamt == "":
                st.error("أدخل بيانات الفاتورة كاملة")
            else:
                bill_no = random.randint(1000000, 9999999)
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
                st.session_state.real_transactions.append(f"[{current_time}] سداد فاتورة {service}: {eamt} ر.ي (رقم: {bill_no})")
                st.success(f"تم تسديد فاتورة ({service}) بقيمة {eamt} ر.ي بنجاح\n\nرقم عملية السداد: {bill_no}")

    # 3. الثابت والإنترنت
    with tab3:
        st.subheader("📞 خدمات الهاتف الثابت والإنترنت والبريد")
        net_service = st.selectbox("اختر الخدمة", ["إنترنت ADSL (يمن نت)", "الهاتف الثابت (منزلي)", "خدمات البريد وتوفير البريد"])
        e_num = st.text_input("رقم الحساب / الهاتف الثابت", key="net_num")
        e_amt = st.text_input("المبلغ (ر.ي)", key="net_amt")
        if st.button("تأكيد سداد الخدمة", key="btn_net", use_container_width=True):
            if e_num == "" or e_amt == "":
                st.error("الرجاء إدخال رقم الحساب والمبلغ كاملة")
            else:
                op_no = random.randint(200000, 999999)
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
                st.session_state.real_transactions.append(f"[{current_time}] سداد {net_service}: {e_amt} ر.ي (رقم: {op_no})")
                st.success(f"تم تسديد اشتراك ({net_service}) رقم: {e_num}\nالمبلغ: {e_amt} ر.ي\n\nرقم العملية: {op_no}")

    # 4. دفع المشتريات
    with tab4:
        st.subheader("🛒 دفع المشتريات والرسوم للمنشآت")
        em = st.text_input("رقم المنشأة (6 أرقام ويبدأ بـ 15)", key="merch_id")
        emoney = st.text_input("المبلغ (ر.ي)", key="merch_amt")
        if st.button("تأكيد الدفع للمنشأة", key="btn_merch", use_container_width=True):
            entered_code = em.strip()
            if entered_code == "" or emoney.strip() == "":
                st.error("الرجاء إدخال رقم المنشأة والمبلغ كاملة")
            elif not entered_code.isdigit() or len(entered_code) != 6 or not entered_code.startswith("15"):
                st.error("رقم المنشأة غير صحيح! يجب أن يتكون من 6 أرقام ويبدأ بالرمز (15).")
            else:
                pay_no = random.randint(500000, 999999)
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
                st.session_state.real_transactions.append(f"[{current_time}] دفع مشتريات منشأة {entered_code}: {emoney} ر.ي")
                st.success(f"تم دفع {emoney} ر.ي بنجاح إلى المنشأة رقم: ({entered_code})\n\nرقم عملية الشراء: {pay_no}")

    # 5. إيداع الرصيد
    with tab5:
        st.subheader("📥 إيداع رصيد للمشتركين")
        dep_phone = st.text_input("رقم جوال المودِع (المشترك)", key="dep_phone")
        ben_phone = st.text_input("رقم جوال المشترك (المستفيد)", key="ben_phone")
        amount = st.text_input("المبلغ المراد إيداعه (ر.ي)", key="dep_amt")
        if st.button("تأكيد الإيداع وإرسال الإشعار", key="btn_dep", use_container_width=True):
            if dep_phone.strip() == "" or ben_phone.strip() == "" or amount.strip() == "":
                st.error("يرجى تعبئة جميع الحقول المطلوبة")
            elif len(dep_phone.strip()) < 9 or len(ben_phone.strip()) < 9:
                st.error("يرجى كتابة أرقام جوال صحيحة ومكتملة")
            else:
                dep_no = random.randint(1000000, 9999999)
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
                st.session_state.real_transactions.append(f"[{current_time}] إيداع مبلغ {amount} ر.ي للمشترك {ben_phone} (رقم: {dep_no})")
                st.success(f"تمت عملية الإيداع بنجاح! 📥\n\n• المودِع: {dep_phone}\n• المستفيد: {ben_phone}\n• المبلغ: {amount} ر.ي\n• رقم العملية: {dep_no}")

    # 6. كشف الحساب
    with tab6:
        st.subheader("📄 كشف الحساب والعمليات")
        if len(st.session_state.real_transactions) == 0:
            st.info("لا توجد أي عمليات منفذة حتى الآن.")
        else:
            for op in reversed(st.session_state.real_transactions):
                st.write("• " + op)