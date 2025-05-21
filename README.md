# LAN Transfer - نظام نقل ملفات عبر الشبكة المحلية

**حقوق النشر (c) Hussein Yehya**  
**مرخص بموجب رخصة MIT**

## نظرة عامة

LAN Transfer هو نظام لإدارة ونقل الملفات عبر الشبكة المحلية (LAN) مع دعم لإدارة المستخدمين والصلاحيات. يتيح النظام رفع وتنزيل الملفات بسهولة بين الأجهزة المتصلة بنفس الشبكة المحلية.
**افتحه من هنا https://lantransfer.hexaloom.site/**
**الأدمن التجريبي**
- Username: hopy
- Email address: hopy@example.com
- Password: okmnji@49861
## المميزات

- دعم رفع الملفات الكبيرة حتى 5 جيجابايت
- تقسيم الملفات الكبيرة (أكبر من 10 ميجابايت) إلى أجزاء أثناء الرفع
- شريط تقدم وعرض حالة الرفع في الوقت الفعلي
- إمكانية استئناف التنزيل
- تحسينات في الأداء مع حجم قطع أكبر (128 كيلوبايت)
- تحسينات في واجهة المستخدم
- رسائل الخطأ والنجاح باللغة العربية
- إصلاح مشاكل معالجة الملفات الكبيرة

## طرق التثبيت

### 1. تثبيت كحزمة Python

```bash
# تثبيت من GitHub Packages
pip install lantransfer

# أو تثبيت من المصدر
git clone https://github.com/Husseinyehya1853/lantransfer.git
cd lantransfer
pip install -e .
```

### 2. تشغيل كتطبيق تنفيذي

1. قم بتنزيل أحدث إصدار من [صفحة الإصدارات](https://github.com/Husseinyehya1853/lantransfer/releases)
2. قم بفك ضغط الملف
3. قم بتشغيل ملف `lantransfer.bat`

### 3. تشغيل باستخدام Docker

```bash
# تشغيل باستخدام Docker Compose
git clone https://github.com/Husseinyehya1853/lantransfer.git
cd lantransfer
docker-compose up -d

# أو باستخدام Docker مباشرة
docker build -t lantransfer .
docker run -p 8000:8000 -v ./media:/app/media lantransfer
```

## بناء الحزم

### بناء حزمة Python

```bash
python -m pip install --upgrade build
python -m build
```

### بناء ملف تنفيذي

```bash
python build_executable.py
```

### بناء صورة Docker

```bash
docker build -t lantransfer .
```

## المساهمة

نرحب بمساهماتكم! يرجى قراءة [دليل المساهمة](CONTRIBUTING.md) للحصول على مزيد من المعلومات.

## الترخيص

هذا المشروع مرخص بموجب [رخصة MIT](LICENSE).
