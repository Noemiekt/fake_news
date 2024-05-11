from deep_translator import GoogleTranslator
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd
from textblob import TextBlob

# Charger le dataset
df = pd.read_csv('health_datatest_nocompound.csv')

# Initialiser l'analyseur de sentiment VADER
analyzer = SentimentIntensityAnalyzer()

# Fonction pour analyser le sentiment après traduction
def analyze_french_sentiment(text):
    # Traduire le français en anglais
    translated_text = GoogleTranslator(source='fr', target='en').translate(text)
    # Analyser le sentiment avec VADER
    scores = analyzer.polarity_scores(translated_text)
    # Déterminer l'étiquette de sentiment basée sur le score composé
    sentiment = 2 if scores['compound'] > 0 else (0 if scores['compound'] < 0 else 1)
    # Créer un objet TextBlob avec le texte traduit
    blob = TextBlob(translated_text)
    # Calculer la subjectivité
    subjectivity = blob.sentiment.subjectivity
    # Retourner le score composé, l'étiquette de sentiment, et la subjectivité
    return scores['compound'], sentiment, subjectivity

# Appliquer la fonction et séparer les résultats en trois colonnes
df[['Compound', 'Sentiment', 'Subjectivity']] = df['Post content'].apply(analyze_french_sentiment).apply(pd.Series)

# Enregistrer le DataFrame modifié
output_path = 'health_datatest.csv'
df.to_csv(output_path, index=False)