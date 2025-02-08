#!/bin/bash

echo "🚀 در حال نصب برنامه پرامپت نویسی ناین..."

# نصب Homebrew (اگر قبلاً نصب نشده باشد)
if ! command -v brew &> /dev/null; then
    echo "🔹 Homebrew یافت نشد! در حال نصب..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

# نصب Python (اگر قبلاً نصب نشده باشد)
if ! command -v python3 &> /dev/null; then
    echo "🔹 Python یافت نشد! در حال نصب..."
    brew install python
fi

# ساخت محیط مجازی
mkdir -p ~/prompt_app
cd ~/prompt_app
python3 -m venv venv
source venv/bin/activate

# نصب کتابخانه‌های موردنیاز
pip install PyQt6 deep-translator

# دانلود آخرین نسخه پروژه از GitHub
if [ -d "Prompt-Generator" ]; then
    cd Prompt-Generator && git pull
else
    git clone https://github.com/jazirehco/Prompt-Generator.git
    cd Prompt-Generator
fi

# اجرای برنامه پس از نصب
echo "✅ نصب کامل شد! برنامه در حال اجرا است..."
python3 prompt_app.py

