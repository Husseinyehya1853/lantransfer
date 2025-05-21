from setuptools import setup, find_packages

setup(
    name="lantransfer",
    version="0.1.0",
    author="Hussein Yehya",
    author_email="your-email@example.com",
    description="نظام نقل ملفات عبر الشبكة المحلية (LAN) مع إدارة المستخدمين والصلاحيات",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Husseinyehya1853/lantransfer",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Framework :: Django",
    ],
    python_requires=">=3.6",
    install_requires=[
        "Django>=5.2.0,<6.0.0",
        "Pillow>=10.0.0,<11.0.0",
        "python-dotenv>=1.0.0,<2.0.0",
        "django-cors-headers>=4.3.0,<5.0.0",
        "django-cleanup>=8.0.0,<9.0.0",
        "gunicorn>=21.2.0,<22.0.0",
        "whitenoise>=6.5.0,<7.0.0",
    ],
)