import pandas as pd
from textblob import TextBlob
import nltk

nltk.download('punkt')

# Paths
input_path = "data/cleaned_reviews/southwest_reviews_cleaned.csv"
output_path = "data/sentiment_analysis/sentiment_southwest_reviews.csv"

def get_sentiment(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity

    # Expanded sentiment scale
    if polarity >= 0.6:
        return "very positive"
    elif polarity > 0.1:
        return "positive"
    elif polarity >= -0.1:
        return "neutral"
    elif polarity > -0.6:
        return "negative"
    else:
        return "very negative"

def analyze_sentiment(input_path, output_path):
    df = pd.read_csv(input_path)

    # Apply enhanced sentiment analysis
    df["sentiment"] = df["cleaned_review"].apply(get_sentiment)

    # Save to new file
    df.to_csv(output_path, index=False)
    print(f"Sentiment analysis completed and saved to {output_path}")

if __name__ == "__main__":
    analyze_sentiment(input_path, output_path)

