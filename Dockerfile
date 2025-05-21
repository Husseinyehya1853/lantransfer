FROM python:3.9-slim

LABEL maintainer="Hussein Yehya <your-email@example.com>"
LABEL description="LAN Transfer - نظام نقل ملفات عبر الشبكة المحلية"

WORKDIR /app

# تثبيت المتطلبات
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# نسخ ملفات المشروع
COPY . .

# جمع الملفات الثابتة
RUN python manage.py collectstatic --noinput

# تعريض المنفذ 8000
EXPOSE 8000

# أمر بدء التشغيل
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]