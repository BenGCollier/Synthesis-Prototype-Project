from flask import Flask, render_template
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64

app = Flask(__name__)

@app.route('/sentiment')
def sentiment():
    df = pd.read_csv('southwest-review-analysis/data/sentiment_analysis/sentiment_southwest_reviews.csv')
    reviews = df.to_dict(orient='records')
    return render_template('sentiment.html', reviews=reviews)

if __name__ == '__main__':
    app.run(debug=True)

@app.route("/charts")
def sentiment_chart():
    df = pd.read_csv("southwest-review-analysis/data/sentiment_analysis/sentiment_southwest_reviews.csv")
    sentiment_counts = df['sentiment'].value_counts()

    # Plot
    fig, ax = plt.subplots()
    sns.barplot(x=sentiment_counts.index, y=sentiment_counts.values, ax=ax)
    ax.set_title("Sentiment Distribution")
    ax.set_ylabel("Number of Reviews")
    ax.set_xlabel("Sentiment")

    # Convert plot to PNG image
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()

    return render_template("chart.html", plot_url=plot_url)
