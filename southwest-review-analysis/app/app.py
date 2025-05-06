from flask import Flask, render_template, request, redirect, url_for
import json
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import seaborn as sns
import io
import base64
import sys
import os
from collections import Counter

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from scraper.trustpilot_scraper import scrape_trustpilot_reviews
from data.preprocessing.preprocess_reviews import preprocess_reviews
from data.sentiment_analysis.analyze_sentiment import analyze_sentiment

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/update-data", methods=["POST"])
def update_data():
    try:
        trustpilot_url = "https://www.trustpilot.com/review/www.southwest.com"
        num_reviews = int(request.form.get("num_reviews", 100))
        reviews_per_page = 20
        num_pages = (num_reviews + reviews_per_page - 1) // reviews_per_page

        raw_path = "data/raw_reviews/southwest_reviews.csv"
        cleaned_path = "data/cleaned_reviews/southwest_reviews_cleaned.csv"
        sentiment_path = "data/sentiment_analysis/sentiment_southwest_reviews.csv"

        scrape_trustpilot_reviews(trustpilot_url, num_pages=num_pages, output_file=raw_path, max_reviews=num_reviews)
        preprocess_reviews(raw_path, cleaned_path)
        analyze_sentiment(cleaned_path, sentiment_path)

        actual_review_count = sum(1 for _ in open(raw_path, encoding='utf-8')) - 1  # account for header row
        message = f"Data updated successfully! Scraped {actual_review_count} reviews."

    except Exception as e:
        message = f"An error occurred: {str(e)}"

    return sentiment_with_message(message)

def sentiment_with_message(message):
    sort = 'newest'
    sentiment_filter = 'all'
    per_page = 25
    page = 1

    df = pd.read_csv('data/sentiment_analysis/sentiment_southwest_reviews.csv')
    df['index'] = df.index

    df = df.sort_values('index', ascending=False)
    reviews = df.iloc[:per_page].to_dict(orient='records')

    total_reviews = len(df)
    total_pages = (total_reviews + per_page - 1) // per_page

    return render_template(
        'sentiment.html',
        reviews=reviews,
        sort=sort,
        sentiment_filter=sentiment_filter,
        per_page=per_page,
        page=page,
        total_pages=total_pages,
        message=message
    )

@app.route("/sentiment")
def sentiment():
    sort = request.args.get('sort', 'newest')
    sentiment_filter = request.args.get('sentiment_filter', 'all')
    per_page = int(request.args.get('per_page', 25))
    page = int(request.args.get('page', 1))
    message = request.args.get('message', '')

    df = pd.read_csv('data/sentiment_analysis/sentiment_southwest_reviews.csv')
    df['index'] = df.index

    if sentiment_filter != 'all':
        df = df[df['sentiment'] == sentiment_filter]

    df = df.sort_values('index', ascending=(sort == 'oldest'))

    total_reviews = len(df)
    total_pages = (total_reviews + per_page - 1) // per_page

    start = (page - 1) * per_page
    end = start + per_page
    reviews = df.iloc[start:end].to_dict(orient='records')

    return render_template(
        'sentiment.html',
        reviews=reviews,
        sort=sort,
        sentiment_filter=sentiment_filter,
        per_page=per_page,
        page=page,
        total_pages=total_pages,
        message=message
    )

@app.route("/visualizations")
def visualizations():
    df = pd.read_csv("data/sentiment_analysis/sentiment_southwest_reviews.csv")

    # Sentiment Distribution
    sentiment_counts = df['sentiment'].value_counts()
    fig, ax = plt.subplots()
    sns.barplot(x=sentiment_counts.index, y=sentiment_counts.values, ax=ax)
    ax.set_title("Sentiment Distribution")
    ax.set_ylabel("Number of Reviews")
    ax.set_xlabel("Sentiment")
    chart_img = io.BytesIO()
    plt.tight_layout()
    plt.savefig(chart_img, format='png')
    chart_img.seek(0)
    chart_url = base64.b64encode(chart_img.getvalue()).decode()
    plt.close()

    # Word Cloud
    text = " ".join(review for review in df["cleaned_review"].dropna())
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    wordcloud_img = io.BytesIO()
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.tight_layout(pad=0)
    plt.savefig(wordcloud_img, format='png')
    wordcloud_img.seek(0)
    wordcloud_url = base64.b64encode(wordcloud_img.getvalue()).decode()
    plt.close()

    # Most Frequent Words (Bar Chart)
    words = " ".join(df["cleaned_review"].dropna()).split()
    most_common_words = Counter(words).most_common(10)
    word_labels, word_counts = zip(*most_common_words)

    fig, ax = plt.subplots()
    sns.barplot(x=list(word_labels), y=list(word_counts), ax=ax)
    ax.set_title("Top 10 Most Frequent Words")
    ax.set_ylabel("Frequency")
    ax.set_xlabel("Words")

    # Rotate the x-axis labels for better spacing
    plt.xticks(rotation=45, ha="right")

    # Adjust layout for better spacing
    plt.tight_layout()

    # Save the figure to a BytesIO object and encode to base64
    frequent_words_img = io.BytesIO()
    plt.savefig(frequent_words_img, format='png')
    frequent_words_img.seek(0)
    frequent_words_url = base64.b64encode(frequent_words_img.getvalue()).decode()
    plt.close()


    # Sentiment Distribution by Review Length (Scatter Plot)
    df['review_length'] = df['cleaned_review'].apply(lambda x: len(str(x)) if x else 0)
    fig, ax = plt.subplots()
    sns.scatterplot(x='review_length', y='sentiment', data=df, ax=ax, hue='sentiment', palette='coolwarm')
    ax.set_title("Sentiment Distribution by Review Length")
    ax.set_xlabel("Review Length")
    ax.set_ylabel("Sentiment")
    sentiment_length_img = io.BytesIO()
    plt.tight_layout()
    plt.savefig(sentiment_length_img, format='png')
    sentiment_length_img.seek(0)
    sentiment_length_url = base64.b64encode(sentiment_length_img.getvalue()).decode()
    plt.close()

    # Sentiment Breakdown by Review Length (Box Plot)
    fig, ax = plt.subplots()
    sns.boxplot(x='sentiment', y='review_length', data=df, ax=ax)
    ax.set_title("Sentiment Breakdown by Review Length")
    ax.set_ylabel("Review Length")
    ax.set_xlabel("Sentiment")
    sentiment_box_img = io.BytesIO()
    plt.tight_layout()
    plt.savefig(sentiment_box_img, format='png')
    sentiment_box_img.seek(0)
    sentiment_box_url = base64.b64encode(sentiment_box_img.getvalue()).decode()
    plt.close()


    return render_template(
        "visualizations.html", 
        chart_url=chart_url, 
        wordcloud_url=wordcloud_url,
        frequent_words_url=frequent_words_url,
        sentiment_length_url=sentiment_length_url,
        sentiment_box_url=sentiment_box_url
    )

if __name__ == '__main__':
    app.run(debug=True)