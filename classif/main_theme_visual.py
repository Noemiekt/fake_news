import os
import pandas as pd
import matplotlib.pyplot as plt

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

# Extraire les noms des fichiers et les moyennes pour chaque catégorie
fichiers_classif, moyennes_classif = zip(*resultats_classif_sorted)
fichiers_sentiment, moyennes_sentiment = zip(*resultats_sentiment_sorted)

# Créer les graphiques à barres
plt.figure(figsize=(10, 5))

# Graphique pour la colonne 'Classification'
plt.subplot(1, 2, 1)
plt.barh(fichiers_classif, moyennes_classif, color='skyblue')
plt.xlabel('Moyenne Classification')
plt.title('Moyenne de Classification par Fichier')

# Graphique pour la colonne 'Sentiment'
plt.subplot(1, 2, 2)
plt.barh(fichiers_sentiment, moyennes_sentiment, color='salmon')
plt.xlabel('Moyenne Sentiment')
plt.title('Moyenne de Sentiment par Fichier')

plt.tight_layout()
plt.show()
