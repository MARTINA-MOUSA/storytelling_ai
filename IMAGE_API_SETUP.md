# 🎨 إعداد API مخصص لتوليد الصور

## كيفية استخدام API مخصص لتوليد الصور

يمكنك استخدام أي API لتوليد الصور (مثل Hugging Face، أو API مخصص آخر) بدلاً من Gemini Imagen.

### إعداد المتغيرات في ملف `.env`

أضف المتغيرات التالية إلى ملف `.env`:

```env
# API Key المخصص
CUSTOM_IMAGE_API_KEY=FAhH7azY.U0xnGpPAaeWU1V2mKNirHnlVwSJ5bFAB

# اسم النموذج (يمكن أن يكون Hugging Face model أو URL مخصص)
CUSTOM_IMAGE_MODEL=openai/gpt-oss-120b
```

### أمثلة على الإعدادات:

#### 1. استخدام Hugging Face Model:
```env
CUSTOM_IMAGE_API_KEY=your_huggingface_token
CUSTOM_IMAGE_MODEL=stabilityai/stable-diffusion-xl-base-1.0
```

#### 2. استخدام URL مخصص:
```env
CUSTOM_IMAGE_API_KEY=your_api_key
CUSTOM_IMAGE_MODEL=https://your-custom-api.com/generate
```

#### 3. استخدام نموذج Hugging Face بدون org:
```env
CUSTOM_IMAGE_API_KEY=your_token
CUSTOM_IMAGE_MODEL=runwayml/stable-diffusion-v1-5
```

### ملاحظات مهمة:

1. **إذا كنت تستخدم Gemini Imagen**: لا تضيف `CUSTOM_IMAGE_API_KEY` و `CUSTOM_IMAGE_MODEL`، وسيتم استخدام Gemini تلقائياً.

2. **الأولوية**: إذا كانت `CUSTOM_IMAGE_API_KEY` و `CUSTOM_IMAGE_MODEL` موجودة، سيتم استخدامهما بدلاً من Gemini.

3. **تنسيق الاستجابة**: الكود يدعم:
   - صور ثنائية مباشرة (binary image)
   - JSON مع صورة base64
   - تنسيقات Hugging Face القياسية

### اختبار الإعداد:

بعد إضافة المتغيرات، أعد تشغيل التطبيق:
```bash
streamlit run frontend/app.py
```

ثم أنشئ قصة جديدة. إذا كان كل شيء مضبوطاً بشكل صحيح، ستستخدم الصور API المخصص.

---

**ملاحظة**: تأكد من أن النموذج المحدد يدعم توليد الصور. بعض النماذج مثل "gpt-oss-120b" هي نماذج نصية وليست نماذج توليد صور.

