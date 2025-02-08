import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QComboBox, QHBoxLayout, QFileDialog, QProgressBar, QRadioButton
from PyQt6.QtGui import QClipboard, QFont, QPixmap
from PyQt6.QtCore import Qt
from deep_translator import GoogleTranslator
import cv2
import numpy as np

class PromptApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("برنامه اختصاصی پرامپت نویسی عکاسی صنعتی ناین")
        self.setGeometry(100, 100, 800, 900)

        layout = QVBoxLayout()

        font = QFont("IranYekan", 12)
        self.setFont(font)

        self.title_label = QLabel("برنامه اختصاصی پرامپت نویسی عکاسی صنعتی ناین", self)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.title_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #FF6600;")
        layout.addWidget(self.title_label)

        self.description = QLabel("""این نرم‌افزار توسط تیم تخصصی استودیو ناین طراحی شده است. هدف آن تولید پرامپت‌های خلاقانه برای خلق تصاویر در پلتفرم‌های MidJourney، Firefly، Stable Diffusion و DALL·E است.""", self)
        self.description.setWordWrap(True)
        self.description.setAlignment(Qt.AlignmentFlag.AlignJustify)
        self.description.setStyleSheet("font-size: 14px; padding: 8px; color: white;")
        layout.addWidget(self.description)

        self.upload_image_button = QPushButton("آپلود تصویر برای آنالیز پرامپت", self)
        self.upload_image_button.clicked.connect(self.upload_image)
        layout.addWidget(self.upload_image_button)
        
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
        self.model_dropdown.addItems(["ChatGPT", "Llama 3", "Mistral", "Falcon", "Open-Source AI"])
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
        self.generate_button.setStyleSheet("QPushButton:hover { background-color: #FF4500; }")
        self.generate_button.clicked.connect(self.generate_prompt)
        layout.addWidget(self.generate_button)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)

        self.label_farsi = QLabel("پرامپت (فارسی):")
        layout.addWidget(self.label_farsi)
        self.output_farsi = QTextEdit(self)
        self.output_farsi.setReadOnly(True)
        layout.addWidget(self.output_farsi)
        
        self.copy_farsi_button = QPushButton("کپی پرامپت فارسی", self)
        self.copy_farsi_button.clicked.connect(lambda: self.copy_to_clipboard(self.output_farsi.toPlainText()))
        layout.addWidget(self.copy_farsi_button)

        self.label_english = QLabel("پرامپت (انگلیسی):")
        layout.addWidget(self.label_english)
        self.output_english = QTextEdit(self)
        self.output_english.setReadOnly(True)
        layout.addWidget(self.output_english)

        self.copy_button = QPushButton("کپی پرامپت انگلیسی", self)
        self.copy_button.clicked.connect(lambda: self.copy_to_clipboard(self.output_english.toPlainText()))
        layout.addWidget(self.copy_button)

        self.footer = QLabel("برنامه‌نویسی: محمد امین ابوالقاسمی", self)
        self.footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.footer.setStyleSheet("font-size: 12px; color: #555; padding: 10px;")
        layout.addWidget(self.footer)

        self.setLayout(layout)

    def upload_image(self):
        file_dialog = QFileDialog()
        image_path, _ = file_dialog.getOpenFileName(self, "انتخاب تصویر", "", "Images (*.png *.jpg *.jpeg)")
        if image_path:
            self.output_farsi.setPlainText(f"تصویر {image_path} آپلود شد. دکمه 'تولید پرامپت' را بزنید.")

    def generate_prompt(self):
        topic = self.input_topic.text().strip()
        keywords = self.input_keywords.text().strip()
        platform = self.platform_dropdown.currentText()
        aspect_ratio = self.aspect_ratio_dropdown.currentText()
        
        if keywords:
            topic += f" - {keywords}"

        prompt_template = "{topic}, cinematic lighting, highly detailed, ultra-realistic."
        prompt_template += f" --ar {aspect_ratio} --q 2 --v 5 --style 4c" if platform == "MidJourney" else ""
        
        translated_prompt = GoogleTranslator(source='fa', target='en').translate(prompt_template.format(topic=topic))
        self.output_farsi.setPlainText(prompt_template.format(topic=topic))
        self.output_english.setPlainText(translated_prompt)

    def copy_to_clipboard(self, text):
        clipboard = QApplication.clipboard()
        clipboard.setText(text, QClipboard.Mode.Clipboard)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PromptApp()
    window.show()
    sys.exit(app.exec())

