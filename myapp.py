from flask import Flask, request, render_template
from newspaper import Article
from textblob import TextBlob
from google.cloud import translate_v2 as translate
import os
import nltk

nltk.download('punkt')
# Google Cloud Translation API 
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/ryanback/PycharmProjects/Summarize News Articles/json/galvanic-augury-344717-bed5c3b9c77e.json'

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/summarize', methods=['POST'])
def summarize():
    url = request.form['url']
    try:
        article = Article(url)
        article.download()
        article.parse()
        article.nlp()

        title = article.title
        authors = ', '.join(article.authors)
        publication_date = str(article.publish_date)
        summary = article.summary

        # Sentiment Analysis
        analysis = TextBlob(article.text)
        sentiment = f'Polarity: {analysis.polarity}, Sentiment: {"positive" if analysis.polarity > 0 else "negative" if analysis.polarity < 0 else "neutral"}'

        # Translate summary to Korean
        translate_client = translate.Client()
        result = translate_client.translate(summary, target_language='ko')
        translated_summary = result['translatedText'].replace('&quot;', '"').replace('&#39;', "'").replace('&amp;', '&')

        return render_template('summary.html', title=title, authors=authors, publication_date=publication_date, summary=summary, sentiment=sentiment, translated_summary=translated_summary)
    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == '__main__':
    app.run(debug=True)
