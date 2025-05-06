from flask import Flask, render_template, request
import json
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend suitable for servers
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import seaborn as sns
import io
import base64

app = Flask(__name__)

@app.route('/')
@app.route('/sentiment')
def sentiment():
    sort = request.args.get('sort', 'newest')
    sentiment_filter = request.args.get('sentiment_filter', 'all')

    df = pd.read_csv('data/sentiment_analysis/sentiment_southwest_reviews.csv')

    # Optional: ensure there's a date column, or use index as a proxy timestamp
    df['index'] = df.index  # mimic timestamp for sorting if no date present

    # Apply filter
    if sentiment_filter != 'all':
        df = df[df['sentiment'] == sentiment_filter]

    # Apply sorting
    if sort == 'oldest':
        df = df.sort_values('index', ascending=True)
    else:  # default to newest
        df = df.sort_values('index', ascending=False)

    reviews = df.to_dict(orient='records')
    return render_template('sentiment.html', reviews=reviews, sort=sort, sentiment_filter=sentiment_filter)

@app.route("/visualizations")
def visualizations():
    df = pd.read_csv("data/sentiment_analysis/sentiment_southwest_reviews.csv")

    # Generate Sentiment Chart
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

    # Generate Word Cloud
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
    plt.close()  # Prevent matplotlib memory leaks

    return render_template("visualizations.html", chart_url=chart_url, wordcloud_url=wordcloud_url)

if __name__ == '__main__':
    app.run(debug=True)