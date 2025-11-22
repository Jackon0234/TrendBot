import os
import logging
from datetime import datetime
from typing import Optional, Dict, Any
import telebot
from pytrends.request import TrendReq
from fpdf import FPDF

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class StringUtils:
    @staticmethod
    def sanitize_text(text: str) -> str:
        if not isinstance(text, str):
            return str(text)
        mapping = {
            'ğ': 'g', 'Ğ': 'G', 'ü': 'u', 'Ü': 'U',
            'ş': 's', 'Ş': 'S', 'ı': 'i', 'İ': 'I',
            'ö': 'o', 'Ö': 'O', 'ç': 'c', 'Ç': 'C'
        }
        for k, v in mapping.items():
            text = text.replace(k, v)
        return text

class PDFReportGenerator(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'Google Trends Analiz Raporu', 0, 1, 'C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Sayfa {self.page_no()}', 0, 0, 'C')

    def add_section(self, title: str, data_frame: Any):
        clean_title = StringUtils.sanitize_text(title)
        self.set_font('Arial', 'B', 12)
        self.set_fill_color(230, 230, 230)
        self.cell(0, 10, clean_title, 0, 1, 'L', 1)
        self.ln(2)
        
        self.set_font('Arial', '', 11)
        
        if data_frame is not None and not data_frame.empty:
            for index, row in data_frame.head(10).iterrows():
                content = f"{index + 1}. {row['query']} ({row['value']})"
                self.cell(0, 8, StringUtils.sanitize_text(content), 0, 1)
        else:
            self.cell(0, 8, "Veri bulunamadi.", 0, 1)
        self.ln(5)

class TrendManager:
    def __init__(self, language: str = 'tr-TR', timezone: int = 180):
        self.pytrends = TrendReq(hl=language, tz=timezone)

    def fetch_data(self, keyword: str) -> Optional[Dict[str, Any]]:
        try:
            self.pytrends.build_payload([keyword], cat=0, timeframe='today 12-m', geo='TR')
            related_queries = self.pytrends.related_queries()
            return related_queries.get(keyword)
        except Exception as e:
            logger.error(f"API Error: {e}")
            return None

class BotService:
    def __init__(self, token: str):
        self.bot = telebot.TeleBot(token, threaded=False)
        self.trend_manager = TrendManager()
        self.is_running = False
        self._register_handlers()

    def _register_handlers(self):
        @self.bot.message_handler(commands=['start', 'help'])
        def send_welcome(message):
            self.bot.reply_to(message, "Analiz edilecek anahtar kelimeyi gonderin.")

        @self.bot.message_handler(func=lambda message: True)
        def handle_keyword(message):
            self.process_request(message)

    def create_report(self, keyword: str, data: Dict[str, Any], chat_id: int) -> str:
        filename = f"report_{chat_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
        pdf = PDFReportGenerator()
        pdf.add_page()
        pdf.set_font("Arial", size=10)
        pdf.cell(0, 10, f"Tarih: {datetime.now().strftime('%d-%m-%Y')}", ln=True)
        pdf.cell(0, 10, StringUtils.sanitize_text(f"Kelime: {keyword}"), ln=True)
        pdf.ln(5)

        pdf.add_section("En Populer (Top)", data.get('top'))
        pdf.add_section("Yukselenler (Rising)", data.get('rising'))
        
        pdf.output(filename)
        return filename

    def process_request(self, message):
        chat_id = message.chat.id
        keyword = message.text.strip()
        if len(keyword) < 2:
            self.bot.send_message(chat_id, "Lutfen gecerli bir kelime girin.")
            return
        
        wait_msg = self.bot.send_message(chat_id, "Veriler cekiliyor...")
        
        data = self.trend_manager.fetch_data(keyword)
        if not data:
            self.bot.edit_message_text("Veri bulunamadi veya API hatasi.", chat_id, wait_msg.message_id)
            return
        try:
            pdf_path = self.create_report(keyword, data, chat_id)
            with open(pdf_path, 'rb') as doc:
                self.bot.send_document(chat_id, doc)
            os.remove(pdf_path)
            self.bot.delete_message(chat_id, wait_msg.message_id)
        except Exception as e:
            logger.error(f"Process Error: {e}")
            self.bot.send_message(chat_id, "Rapor olusturulurken hata meydana geldi.")

    def start(self):
        self.is_running = True
        logger.info("Bot baslatildi.")
        try:
            self.bot.infinity_polling()
        except Exception as e:
            logger.error(f"Polling Error: {e}")
            self.is_running = False

    def stop(self):
        if self.is_running:
            self.bot.stop_polling()
            self.is_running = False
            logger.info("Bot durduruldu.")