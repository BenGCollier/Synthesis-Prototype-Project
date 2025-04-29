import pandas as pd
import re
import nltk
from nltk.corpus import stopwords

# Download stopwords once
nltk.download('stopwords')

def clean_text(text):
    # Lowercase
    text = text.lower()
    # Remove punctuation and numbers
    text = re.sub(r'[^a-z\s]', '', text)
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    words = text.split()
    words = [word for word in words if word not in stop_words]
    cleaned_text = ' '.join(words)
    return cleaned_text

def preprocess_reviews(input_file, output_file):
    df = pd.read_csv(input_file)
    
    # Apply cleaning to the 'review' column
    df["cleaned_review"] = df["Review"].apply(clean_text)
    
    # Save the cleaned data
    df.to_csv(output_file, index=False)
    print(f"Cleaned data saved to {output_file}")

if __name__ == "__main__":
    input_path = "southwest-review-analysis/data/raw_reviews/southwest_reviews.csv"
    output_path = "southwest-review-analysis/data/cleaned_reviews/southwest_reviews_cleaned.csv"
    preprocess_reviews(input_path, output_path)
