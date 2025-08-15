# دليل تثبيت الخطوط العربية - Arabic Fonts Installation Guide

## المطلوب - Requirements

لضمان عرض النصوص العربية بشكل صحيح في التطبيق، يُرجى تثبيت الخطوط العربية المناسبة.

## مجلد الخطوط - Fonts Directory

تم إنشاء مجلد `fonts/` في جذر المشروع لحفظ الخطوط المخصصة.

```
Mobile Shop Management/
├── fonts/
│   ├── README.md
│   ├── Tahoma.ttf (ضع الخط هنا)
│   ├── Arial-Unicode-MS.ttf (ضع الخط هنا)
│   └── ... (أي خطوط عربية أخرى)
```

## الخطوط المُوصى بها - Recommended Fonts

### 1. خط تاهوما - Tahoma (الأفضل)
- الملف: `Tahoma.ttf`
- يدعم العربية بشكل ممتاز
- متوفر في Windows افتراضياً

### 2. Arial Unicode MS
- الملف: `Arial-Unicode-MS.ttf`
- يدعم جميع اللغات تقريباً
- مُوصى به كخط احتياطي

### 3. Segoe UI
- خط Windows الحديث
- دعم جيد للعربية

### 4. Noto Sans Arabic
- خط مجاني من Google
- يمكن تحميله من: https://fonts.google.com/noto/specimen/Noto+Sans+Arabic

## طريقة التثبيت - Installation Steps

### الطريقة الأولى: نسخ الخطوط إلى مجلد fonts
1. ابحث عن ملفات الخطوط في نظامك:
   - **Windows**: `C:\Windows\Fonts\`
   - **macOS**: `/System/Library/Fonts/` أو `/Library/Fonts/`
   - **Linux**: `/usr/share/fonts/` أو `~/.fonts/`

2. انسخ ملفات الخطوط المطلوبة إلى مجلد `fonts/` في المشروع

3. أعد تشغيل التطبيق

### الطريقة الثانية: تحميل خطوط مجانية
1. تحميل Noto Sans Arabic:
   ```bash
   # انتقل إلى مجلد fonts
   cd fonts/
   
   # تحميل Noto Sans Arabic
   wget https://github.com/googlefonts/noto-fonts/raw/main/hinted/ttf/NotoSansArabic/NotoSansArabic-Regular.ttf
   ```

2. أو تحميل من المتصفح:
   - اذهب إلى: https://fonts.google.com/noto/specimen/Noto+Sans+Arabic
   - اضغط "Download family"
   - استخرج الملفات وانسخ `.ttf` إلى مجلد `fonts/`

## التحقق من التثبيت - Verification

بعد إضافة الخطوط، شغّل الأمر التالي للتحقق:

```bash
python utils/font_loader.py
```

سيُظهر لك:
- قائمة بالخطوط المتاحة في النظام
- الخطوط المخصصة المُحمّلة من مجلد fonts
- الخط المُختار للتطبيق

## استكشاف الأخطاء - Troubleshooting

### مشكلة: النصوص العربية تظهر مربعات □□□
**الحل**: تأكد من وجود خط عربي صحيح في مجلد `fonts/`

### مشكلة: الخط لا يُحمّل
**الحل**: 
1. تأكد من أن امتداد الملف `.ttf` أو `.otf`
2. تأكد من أن الملف غير معطوب
3. أعد تشغيل التطبيق

### مشكلة: النص يظهر بخط إنجليزي
**الحل**: ضع خط تاهوما أو أي خط عربي في المجلد

## ملاحظات مهمة - Important Notes

- **الترخيص**: تأكد من وجود ترخيص صحيح لاستخدام الخطوط
- **الحجم**: تجنب الخطوط الكبيرة (أكثر من 5 ميجابايت)
- **التوافق**: الخطوط يجب أن تدعم Unicode العربي
- **الأولوية**: الخطوط في مجلد `fonts/` لها أولوية على خطوط النظام

## ملفات الخطوط المطلوبة - Required Font Files

قم بإضافة هذه الملفات إلى مجلد `fonts/` (اختياري):

```
fonts/
├── Tahoma.ttf                 # الأفضل للعربية
├── Arial-Unicode-MS.ttf       # دعم شامل
├── Segoe-UI.ttf              # خط Windows حديث
├── NotoSansArabic-Regular.ttf # خط مجاني
└── أي خطوط عربية أخرى...
```

بعد إضافة الخطوط، سيقوم التطبيق بالتعرف عليها تلقائياً واستخدامها في الواجهة والتقارير.