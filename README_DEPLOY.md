# 🌐 دليل النشر السريع | Quick Deploy Guide

## 🚀 الطريقة الأسهل: Streamlit Cloud (موصى به)

### خطوات النشر في 5 دقائق:

1. **ادفع الكود إلى GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Ready for deployment"
   git remote add origin https://github.com/yourusername/storytelling_ai.git
   git push -u origin main
   ```

2. **اذهب إلى Streamlit Cloud:**
   - https://share.streamlit.io/
   - سجل دخول بحساب GitHub

3. **اضغط "New app" واملأ:**
   - Repository: `yourusername/storytelling_ai`
   - Main file path: `streamlit_app.py`
   - Branch: `main`

4. **أضف API Keys:**
   - بعد النشر، اضغط "⋮" → "Settings" → "Secrets"
   - أضف:
     ```toml
     GEMINI_API_KEY = "your_key_here"
     ```

5. **جاهز!** 🎉
   - رابطك: `https://your-app-name.streamlit.app`

---

## 📚 للمزيد من التفاصيل

راجع [DEPLOY_ONLINE.md](DEPLOY_ONLINE.md) للطرق الأخرى:
- Railway
- Render
- VPS + Docker

---

**بعد النشر، شارك الرابط! 🚀**

