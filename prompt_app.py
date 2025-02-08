import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QComboBox, QHBoxLayout, QFrame
from PyQt6.QtGui import QClipboard, QFont
from PyQt6.QtCore import Qt
from deep_translator import GoogleTranslator
import random

class PromptApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("برنامه اختصاصی پرامپت نویسی عکاسی صنعتی ناین")
        self.setGeometry(100, 100, 700, 700)

        layout = QVBoxLayout()

        font = QFont("IranYekan", 12)
        self.setFont(font)

        # تیتر برنامه
        self.title_label = QLabel("برنامه اختصاصی پرامپت نویسی عکاسی صنعتی ناین", self)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.title_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #FF6600;")
        layout.addWidget(self.title_label)

        # توضیح برنامه
        self.description = QLabel(" ""این نرم‌افزار به‌طور انحصاری توسط تیم تخصصی برنامه‌نویسی استودیو ناین طراحی و توسعه یافته است. \n"
            "هدف اصلی آن ارائه راهکاری هوشمند برای تولید پرامپت‌های خلاقانه به منظور خلق تصاویر در بسترهایی همچون MidJourney، Firefly، Stable Diffusion و DALL·E می‌باشد. \n"
            "با بهره‌گیری از الگوریتم‌های پیشرفته هوش مصنوعی، این برنامه فراتر از محدودیت‌های معمول چت‌جی‌پی‌تی عمل می‌کند و تجربه‌ای نوین در زمینه پرامپت‌نویسی به کاربران ارائه می‌دهد. \n"
            "تنها کافی است موضوع یا کلمات کلیدی مدنظر خود را وارد کنید، مدل هوش مصنوعی مناسب را انتخاب نمایید و تنظیمات تصویر دلخواه را اعمال کنید تا پرامپت نهایی به‌راحتی تولید شود.",
            self)
        self.description.setWordWrap(True)
        self.description.setAlignment(Qt.AlignmentFlag.AlignJustify)
        self.description.setAlignment(Qt.AlignmentFlag.AlignJustify)
        self.description.setStyleSheet("font-size: 14px; padding: 8px; color: white; text-align: justify;")
        layout.addWidget(self.description)

        self.label_topic = QLabel("موضوع تصویر را وارد کنید:")
        layout.addWidget(self.label_topic)

        self.input_topic = QLineEdit(self)
        layout.addWidget(self.input_topic)

        self.label_keywords = QLabel("یا کلمات کلیدی را وارد کنید (با خط فاصله جدا کنید):")
        layout.addWidget(self.label_keywords)

        self.input_keywords = QLineEdit(self)
        layout.addWidget(self.input_keywords)

        self.label_model = QLabel("مدل هوش مصنوعی برای تولید پرامپت:")
        layout.addWidget(self.label_model)

        self.model_dropdown = QComboBox(self)
        self.model_dropdown.addItems(["Llama 3", "Mistral", "Falcon", "Open-Source AI"])
        layout.addWidget(self.model_dropdown)

        self.label_platform = QLabel("پلتفرم تولید تصویر را انتخاب کنید:")
        layout.addWidget(self.label_platform)

        self.platform_dropdown = QComboBox(self)
        self.platform_dropdown.addItems(["MidJourney", "Firefly", "Stable Diffusion", "DALL·E"])
        layout.addWidget(self.platform_dropdown)

        self.label_quality = QLabel("تنظیمات تصویر:")
        layout.addWidget(self.label_quality)

        self.quality_dropdown = QComboBox(self)
        self.quality_dropdown.addItems(["SD", "HD", "4K", "8K"])
        layout.addWidget(self.quality_dropdown)

        self.aspect_ratio_dropdown = QComboBox(self)
        self.aspect_ratio_dropdown.addItems(["1:1", "16:9", "4:5", "9:16"])
        layout.addWidget(self.aspect_ratio_dropdown)

        self.generate_button = QPushButton("تولید پرامپت", self)
        self.generate_button.setStyleSheet("background-color: #FF6600; color: white; font-size: 14px; padding: 8px; border-radius: 5px;")
        self.generate_button.clicked.connect(self.generate_prompt)
        layout.addWidget(self.generate_button)

        self.label_english = QLabel("پرامپت (فارسی):")
        layout.addWidget(self.label_english)

        self.output_english = QTextEdit(self)
        self.output_english.setReadOnly(True)
        layout.addWidget(self.output_english)

        self.copy_english_button = QPushButton("کپی پرامپت", self)
        self.copy_english_button.clicked.connect(lambda: self.copy_to_clipboard(self.output_english.toPlainText()))
        layout.addWidget(self.copy_english_button)

        # اضافه کردن نام برنامه‌نویس
        self.footer = QLabel("برنامه‌نویسی: محمد امین ابوالقاسمی", self)
        self.footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.footer.setStyleSheet("font-size: 12px; color: #555; padding: 10px;")
        layout.addWidget(self.footer)

        self.setLayout(layout)

    def generate_prompt(self):
        topic = self.input_topic.text().strip()
        keywords = self.input_keywords.text().strip()
        selected_model = self.model_dropdown.currentText()

        if keywords:
            topic = " - ".join(keywords.split("-"))

        prompt_templates = {
            "Llama 3": "جزئیات بالا، نورپردازی سینمایی، واقعی‌گرایانه: {topic}",
            "Mistral": "رندرینگ هنری و سورئال: {topic}",
            "Falcon": "تولید پرامپت بر اساس مدل‌های تحقیقاتی: {topic}",
            "Open-Source AI": "پرامپت تولید شده با هوش مصنوعی آزاد: {topic}"
        }

        selected_prompt_template = prompt_templates.get(selected_model, "پرامپت استاندارد: {topic}")
        base_prompt = selected_prompt_template.format(topic=topic)

        translated_prompt = GoogleTranslator(source='fa', target='en').translate(base_prompt)
        self.output_english.setPlainText(translated_prompt)

    def copy_to_clipboard(self, text):
        clipboard = QApplication.clipboard()
        clipboard.setText(text, QClipboard.Mode.Clipboard)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PromptApp()
    window.show()
    sys.exit(app.exec())

