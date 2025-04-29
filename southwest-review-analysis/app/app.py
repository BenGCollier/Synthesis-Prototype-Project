from flask import Flask, render_template
import json
import pandas as pd

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/sentiment')
def sentiment():
    df = pd.read_csv('southwest-review-analysis/data/sentiment_analysis/sentiment_southwest_reviews.csv')
    reviews = df.to_dict(orient='records')  # Converts rows into a list of dictionaries
    return render_template('sentiment.html', reviews=reviews)

if __name__ == '__main__':
    app.run(debug=True)