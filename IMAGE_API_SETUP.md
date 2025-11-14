# 🎨 إعداد API مخصص لتوليد الصور

## كيفية استخدام API مخصص لتوليد الصور

يمكنك استخدام أي API لتوليد الصور (مثل Clipdrop، Hugging Face، أو API مخصص آخر) بدلاً من Gemini Imagen.

## 🎯 استخدام Clipdrop API (موصى به)

Clipdrop يوفر جودة عالية في توليد الصور.

### إعداد Clipdrop في ملف `.env`:

```env
# Clipdrop API Key
CUSTOM_IMAGE_API_KEY=efba5c5ee632cb0e5b13ad97948a15b4f805bd948f855e7553a8693faa798b2e59fb76df19a360c015133a36926a9d7c

# تفعيل Clipdrop
USE_CLIPDROP=true
```

**ملاحظة:** عند استخدام Clipdrop، لا حاجة لإضافة `CUSTOM_IMAGE_MODEL`.

## 🔧 استخدام Hugging Face أو API آخر

### إعداد المتغيرات في ملف `.env`:

```env
# API Key المخصص
CUSTOM_IMAGE_API_KEY=your_api_key_here

# اسم النموذج (يمكن أن يكون Hugging Face model أو URL مخصص)
CUSTOM_IMAGE_MODEL=openai/gpt-oss-120b

# تأكد من عدم تفعيل Clipdrop
USE_CLIPDROP=false
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

1. **أولوية الاستخدام**:
   - إذا كان `USE_CLIPDROP=true` و `CUSTOM_IMAGE_API_KEY` موجود → استخدام Clipdrop
   - إذا كان `CUSTOM_IMAGE_API_KEY` و `CUSTOM_IMAGE_MODEL` موجودان → استخدام API المخصص
   - إذا كان `GEMINI_API_KEY` موجود فقط → استخدام Gemini Imagen
   - إذا لم يكن أي منهما → استخدام الصورة الافتراضية

2. **إذا كنت تستخدم Gemini Imagen**: لا تضيف `CUSTOM_IMAGE_API_KEY`، وسيتم استخدام Gemini تلقائياً.

3. **تنسيق الاستجابة**: الكود يدعم:
   - صور ثنائية مباشرة (binary image) - Clipdrop
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

