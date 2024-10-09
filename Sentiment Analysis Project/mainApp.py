import streamlit as st
import re
import joblib
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer

# Loading the trained model and vectorizer
model = joblib.load("sentiment_trained_model.joblib")
vectorizer = joblib.load("tfidf_vectorizer.joblib")

# Initialize the Porter Stemmer
porter_stem = PorterStemmer()

# Function for stemming and preprocessing the tweet
def Stemming(content):
    stemmed_cont = re.sub('[^a-zA-Z]', ' ', content)
    stemmed_cont = stemmed_cont.lower()
    stemmed_cont = stemmed_cont.split()
    stemmed_cont = [porter_stem.stem(word) for word in stemmed_cont if not word in stopwords.words('english')]
    stemmed_cont = ' '.join(stemmed_cont)
    return stemmed_cont

# Function to predict sentiment
def result(tweet):
    p_tweet = Stemming(tweet)
    tweet_tfidf = vectorizer.transform([p_tweet])  # Transform the tweet using the trained vectorizer
    prediction = model.predict(tweet_tfidf)  # Predict sentiment
    if prediction[0] == 1:
        return "Positive"
    else:
        return "Negative"

# Streamlit app UI with emojis
def main():
    # Title with an emoji
    st.title("Sentiment Analysis App :smiley:")

    # Subtitle with an emoji
    st.subheader("Analyze the sentiment of your tweet :speech_balloon:")

    # User input for the tweet
    tweet = st.text_area("Enter a tweet:")

    # Button for prediction with an emoji
    if st.button("Analyze Sentiment :mag:"):
        if tweet:
            sentiment = result(tweet)
            if sentiment == "Positive":
                st.success(f"Positive Sentiment! :thumbsup: :smile:")  # Positive feedback with emojis
            else:
                st.error(f"Negative Sentiment! :thumbsdown: :disappointed:")  # Negative feedback with emojis
        else:
            st.warning("Please enter a valid tweet :exclamation:")

if __name__ == '__main__':
    main()
