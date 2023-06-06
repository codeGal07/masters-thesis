from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from textblob import TextBlob, Word
import nltk


def evaluate_text_semantics(text):
    # TextBlob constructor performs some basic preprocessing
    # on the text by default. It includes tokenization and lowercasing.
    # These preprocessing steps are applied internally
    # by the TextBlob library when the TextBlob object is created.

    # preprocess text for semantic analysis
    text = remove_stop_words(text)
    text = lemmatization(text)

    # perform semantic analysis
    polarity = get_polarity(text)
    return polarity


def remove_stop_words(text):
    stopwords_list = stopwords.words('english')

    # Tokenize the text into words
    words = word_tokenize(text)
    filtered_words = [word for word in words if word.lower() not in stopwords_list]

    # Join the filtered words back into a sentence
    filtered_text = ' '.join(filtered_words)
    return filtered_text


def lemmatization(text):
    blob = TextBlob(text)
    lemmatized_text = " ".join([Word(word).lemmatize() for word in blob.words])

    return lemmatized_text


def get_polarity(text):
    blob = TextBlob(text)
    sentiment = blob.sentiment

    return sentiment.polarity
