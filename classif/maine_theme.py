import torch
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import xgboost as xgb
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import ConfusionMatrixDisplay

# df = pd.read_csv('dataset/crisis_dataset.csv')
# df['Hyperlinks_exist'] = df['Hyperlinks_exist'].map({'no': 0, 'yes': 1})
# df['Media_exists'] = df['Media_exists'].map({'no': 0, 'yes': 1})
# df['Classification'] = df['Classification'].map({'Misinformation': 0, 'Information': 1})
# df['Sentiment'] = df['Sentiment'].map({'negative': 0, 'neutral': 1, 'positive': 2})

# moyenne_classif = df['Classification'].mean()
# moyenne_sentiment = df['Sentiment'].mean()

# print("La moyenne de la colonne 'Classification' est :", moyenne_classif)
# print("La moyenne de la colonne 'Sentiment' est :", moyenne_sentiment)


folder = "dataset/"
resultats_classif = []
resultats_sentiment = []

# Boucler sur tous les fichiers dans le dossier
for fichier in os.listdir(folder):
    if fichier.endswith('.csv'):
        complet_path = os.path.join(folder, fichier)
        df = pd.read_csv(complet_path, encoding='latin1')
        df['Hyperlinks_exist'] = df['Hyperlinks_exist'].map({'no': 0, 'yes': 1})
        df['Media_exists'] = df['Media_exists'].map({'no': 0, 'yes': 1})
        df['Classification'] = df['Classification'].map({'Misinformation': 0, 'Information': 1})
        df['Sentiment'] = df['Sentiment'].map({'negative': 0, 'neutral': 1, 'positive': 2})

        moyenne_classif = df['Classification'].mean()
        moyenne_sentiment = df['Sentiment'].mean()
        
        resultats_classif.append((fichier, moyenne_classif))
        resultats_sentiment.append((fichier, moyenne_sentiment))

# Trier les résultats par moyenne
resultats_classif_sorted = sorted(resultats_classif, key=lambda x: x[1], reverse=False)
resultats_sentiment_sorted = sorted(resultats_sentiment, key=lambda x: x[1], reverse=False)

# Afficher les résultats
for fichier, moyenne_classif in resultats_classif_sorted:
    print(f"La moyenne de la colonne 'Classification' dans {fichier} est : {moyenne_classif}")
for fichier, moyenne_sentiment in resultats_sentiment_sorted:
    print(f"La moyenne de la colonne 'Sentiment' dans {fichier} est : {moyenne_sentiment}")