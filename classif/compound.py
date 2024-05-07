from deep_translator import GoogleTranslator
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd

# Load the dataset (replace with your actual file path)
df = pd.read_csv('health_datatest_nocompound.csv')

# Initialize the VADER sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

# Function to analyze sentiment after translation
def analyze_french_sentiment(text):
    # Translate French to English using Google Translator via deep-translator
    translated_text = GoogleTranslator(source='fr', target='en').translate(text)
    # Analyze sentiment using VADER
    scores = analyzer.polarity_scores(translated_text)
    # Determine sentiment label based on compound score
    if scores['compound'] < 0:
        sentiment = 0  # Negative
    elif scores['compound'] == 0:
        sentiment = 1  # Neutral
    else:
        sentiment = 2  # Positive
    # Return the compound score and the sentiment label
    return scores['compound'], sentiment

# Ensure the column name matches your dataset
df[['Compound', 'Sentiment']] = df['Post content'].apply(analyze_french_sentiment).apply(pd.Series)

output_path = 'health_datatest.csv'  # Change this to your desired file name/path
df.to_csv(output_path, index=False)
