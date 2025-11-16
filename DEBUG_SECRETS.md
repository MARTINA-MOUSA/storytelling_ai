# 🔍 كيفية التحقق من أن المفاتيح موجودة

## طريقة 1: إضافة كود مؤقت للتحقق

أضف هذا الكود في بداية `streamlit_app.py` مؤقتاً:

```python
import os
import streamlit as st

# Debug section - remove after testing
st.sidebar.write("### 🔍 Debug Info")
st.sidebar.write(f"GEMINI_API_KEY exists: {bool(os.getenv('GEMINI_API_KEY'))}")
st.sidebar.write(f"All env vars with 'GEMINI': {[k for k in os.environ.keys() if 'GEMINI' in k]}")

# Check Streamlit secrets
try:
    if hasattr(st, 'secrets'):
        st.sidebar.write(f"Streamlit secrets available: {bool(st.secrets)}")
        if hasattr(st.secrets, 'get'):
            st.sidebar.write(f"GEMINI_API_KEY in secrets: {'GEMINI_API_KEY' in st.secrets}")
except Exception as e:
    st.sidebar.write(f"Secrets error: {e}")
```

## طريقة 2: التحقق من Logs

1. اذهب إلى Settings → Logs
2. ابحث عن أي أخطاء متعلقة بـ API keys
3. تحقق من أن المفاتيح موجودة في environment

## طريقة 3: التحقق من Secrets في Streamlit Cloud

1. اذهب إلى Settings → Secrets
2. تأكد أن المفاتيح موجودة بهذا الشكل:
   ```toml
   GEMINI_API_KEY = "your_key_here"
   ```
3. تأكد من:
   - استخدام `=` مع مسافات
   - استخدام علامات اقتباس `"..."`
   - لا توجد أخطاء إملائية

## طريقة 4: إعادة تشغيل التطبيق

بعد إضافة المفاتيح:
1. اضغط "Save" في Secrets
2. انتظر 30-60 ثانية
3. اضغط "Reboot app" في Settings
4. أعد تحميل الصفحة

---

**بعد التحقق، احذف كود الـ debug!**

