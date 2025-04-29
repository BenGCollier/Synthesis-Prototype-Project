import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

def perform_topic_modeling(input_file, num_topics=5, num_words=10):
    # Load the cleaned reviews
    df = pd.read_csv(input_file)

    # Create a document-term matrix
    vectorizer = CountVectorizer(max_df=0.9, min_df=2, stop_words='english')
    dtm = vectorizer.fit_transform(df['cleaned_review'])

    # Fit LDA
    lda = LatentDirichletAllocation(n_components=num_topics, random_state=42)
    lda.fit(dtm)

    # Display the topics
    for idx, topic in enumerate(lda.components_):
        print(f"Topic #{idx + 1}:")
        print([vectorizer.get_feature_names_out()[i] for i in topic.argsort()[-num_words:]])
        print()

if __name__ == "__main__":
    input_file = "southwest-review-analysis/data/cleaned_reviews/southwest_reviews_cleaned.csv"
    perform_topic_modeling(input_file)