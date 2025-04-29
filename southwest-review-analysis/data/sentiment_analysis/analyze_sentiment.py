import pandas as pd
from textblob import TextBlob
import nltk

nltk.download('punkt')

# Paths
input_path = "southwest-review-analysis/data/cleaned_reviews/southwest_reviews_cleaned.csv"
output_path = "southwest-review-analysis/data/sentiment_analysis/sentiment_southwest_reviews.csv"

def get_sentiment(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity > 0:
        return "positive"
    elif polarity < 0:
        return "negative"
    else:
        return "neutral"

def analyze_sentiment(input_path, output_path):
    df = pd.read_csv(input_path)
    
    # Apply sentiment analysis
    df["sentiment"] = df["cleaned_review"].apply(get_sentiment)
    
    # Save to new file
    df.to_csv(output_path, index=False)
    print(f"Sentiment analysis completed and saved to {output_path}")

if __name__ == "__main__":
    analyze_sentiment(input_path, output_path)
