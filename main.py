import os
import tkinter as tk
from tkinter import messagebox
from google.cloud import translate_v2 as translate
from textblob import TextBlob
from newspaper import Article
import nltk

# Ensure necessary NLTK data is downloaded
nltk.download('punkt')

# Set up Google Cloud Translation
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/ryanback/PycharmProjects/Summarize News Articles/json/galvanic-augury-344717-bed5c3b9c77e.json'

# Function to translate text to Korean using Google Cloud Translation API
def translate_text_to_korean(text):
    translate_client = translate.Client()
    result = translate_client.translate(text, target_language='ko')
    translated_text = result['translatedText']
    # Replace HTML entities with normal quotes
    translated_text = translated_text.replace('&quot;', '"')
    return translated_text

# Function to summarize the article
def summarize():
    url = utext.get('1.0', "end").strip()
    if not url.startswith('http://') and not url.startswith('https://'):
        messagebox.showerror("Error", "Please enter a valid URL.")
        return

    try:
        article = Article(url)
        article.download()
        article.parse()
        article.nlp()

        title.config(state='normal')
        author.config(state='normal')
        publication.config(state='normal')
        summary.config(state='normal')
        translated_summary.config(state='normal')
        sentiment.config(state='normal')

        title.delete('1.0','end')
        author.delete('1.0','end')
        publication.delete('1.0','end')
        summary.delete('1.0','end')
        translated_summary.delete('1.0','end')
        sentiment.delete('1.0', 'end')

        title.insert('1.0', article.title)
        author.insert('1.0', ', '.join(article.authors))
        publication.insert('1.0', str(article.publish_date))
        summary.insert('1.0', article.summary)
        translated_summary.insert('1.0', translate_text_to_korean(article.summary))

        analysis = TextBlob(article.text)
        sentiment.insert('1.0', f'Polarity: {analysis.polarity}, Sentiment: {"positive" if analysis.polarity > 0 else "negative" if analysis.polarity < 0 else "neutral"}')

        title.config(state='disabled')
        author.config(state='disabled')
        publication.config(state='disabled')
        summary.config(state='disabled')
        translated_summary.config(state='disabled')
        sentiment.config(state='disabled')

    except Exception as e:
        messagebox.showerror("Error", "Failed to process the article. Please check the URL or your internet connection.")

# GUI Setup
root = tk.Tk()
root.title("News Summarizer")
root.geometry('800x600')

tlabel = tk.Label(root, text="Title:")
tlabel.pack()

title = tk.Text(root, height=1, width=100)
title.config(state='disabled', bg='#dddddd')
title.pack()

alabel = tk.Label(root, text="Author(s):")
alabel.pack()

author = tk.Text(root, height=1, width=100)
author.config(state='disabled', bg='#dddddd')
author.pack()

plabel = tk.Label(root, text="Publication Date:")
plabel.pack()

publication = tk.Text(root, height=1, width=100)
publication.config(state='disabled', bg='#dddddd')
publication.pack()

slable = tk.Label(root, text="Summary:")
slable.pack()

summary = tk.Text(root, height=10, width=100)
summary.config(state='disabled', bg='#dddddd')
summary.pack()

tslabel = tk.Label(root, text="Summary in Korean:")
tslabel.pack()

translated_summary = tk.Text(root, height=10, width=100)
translated_summary.config(state='disabled', bg='#dddddd')
translated_summary.pack()

selabel = tk.Label(root, text="Sentiment Analysis:")
selabel.pack()

sentiment = tk.Text(root, height=1, width=100)
sentiment.config(state='disabled', bg='#dddddd')
sentiment.pack()

ulabel = tk.Label(root, text="URL:")
ulabel.pack()

utext = tk.Text(root, height=1, width=100)
utext.pack()

btn = tk.Button(root, text="Summarize", command=summarize)
btn.pack()

root.mainloop()
