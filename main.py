import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QTextEdit, QLineEdit, QPushButton
from google.cloud import translate_v2 as translate
from textblob import TextBlob
from newspaper import Article
import nltk
nltk.download('punkt')


# Google Cloud Translation API
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/ryanback/PycharmProjects/Summarize News Articles/json/galvanic-augury-344717-bed5c3b9c77e.json'

class NewsSummarizer(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('News Summarizer and Translator')

        layout = QVBoxLayout()

        self.url_label = QLabel('Article URL:')
        layout.addWidget(self.url_label)

        self.url_input = QLineEdit()
        self.url_input.setFixedHeight(30)  # Set fixed height for QLineEdit

        layout.addWidget(self.url_input)

        self.title_label = QLabel('Title:')
        layout.addWidget(self.title_label)

        self.title_output = QTextEdit()
        self.title_output.setFixedHeight(30)
        self.title_output.setReadOnly(True)
        layout.addWidget(self.title_output)

        self.author_label = QLabel('Author:')
        layout.addWidget(self.author_label)

        self.author_output = QTextEdit()
        self.author_output.setFixedHeight(30)
        self.author_output.setReadOnly(True)
        layout.addWidget(self.author_output)

        self.publication_label = QLabel('Publication Date:')
        layout.addWidget(self.publication_label)

        self.publication_output = QTextEdit()
        self.publication_output.setFixedHeight(30)
        self.publication_output.setReadOnly(True)
        layout.addWidget(self.publication_output)

        self.summary_label = QLabel('Summary:')
        layout.addWidget(self.summary_label)

        self.summary_output = QTextEdit()
        self.summary_output.setFixedHeight(80)

        self.summary_output.setReadOnly(True)
        layout.addWidget(self.summary_output)

        self.translated_summary_label = QLabel('Summary in Korean:')
        layout.addWidget(self.translated_summary_label)

        self.translated_summary_output = QTextEdit()
        self.translated_summary_output.setFixedHeight(80)

        self.translated_summary_output.setReadOnly(True)
        layout.addWidget(self.translated_summary_output)

        self.sentiment_label = QLabel('Sentiment Analysis:')
        layout.addWidget(self.sentiment_label)

        self.sentiment_output = QTextEdit()
        self.sentiment_output.setFixedHeight(30)

        self.sentiment_output.setReadOnly(True)
        layout.addWidget(self.sentiment_output)

        self.summarize_button = QPushButton('Summarize and Translate')
        self.summarize_button.clicked.connect(self.summarize)
        layout.addWidget(self.summarize_button)

        self.setLayout(layout)

    def summarize(self):
        url = self.url_input.text()
        try:
            article = Article(url)
            article.download()
            article.parse()
            article.nlp()

            self.title_output.setText(article.title)
            self.author_output.setText(', '.join(article.authors))
            self.publication_output.setText(str(article.publish_date))
            self.summary_output.setText(article.summary)

            # Sentiment Analysis
            analysis = TextBlob(article.text)
            sentiment = f'Polarity: {analysis.polarity}, Sentiment: {"positive" if analysis.polarity > 0 else "negative" if analysis.polarity < 0 else "neutral"}'
            self.sentiment_output.setText(sentiment)

            # Translate summary to Korean
            translated_summary = self.translate_text_to_korean(article.summary)
            self.translated_summary_output.setText(translated_summary)
        except Exception as e:
            print(f"An error occurred: {e}")

    def translate_text_to_korean(self, text):
        translate_client = translate.Client()
        result = translate_client.translate(text, target_language='ko')
        translated_text = result['translatedText']

        # HTML entities changes
        translated_text = translated_text.replace('&quot;', '"')
        translated_text = translated_text.replace('&#39;', "'")
        translated_text = translated_text.replace('&amp;', '&')

        return translated_text


def main():
    app = QApplication(sys.argv)
    ex = NewsSummarizer()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
