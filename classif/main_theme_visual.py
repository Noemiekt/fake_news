import os
import pandas as pd
import matplotlib.pyplot as plt

folder = "dataset/"
resultats_classif = []
resultats_sentiment = []

# Map file names to categories
categories = {
    "war_dataset.csv": "War",
    "crisis_dataset.csv": "Economic crisis",
    "politics_dataset.csv": "Politic",
    "health_dataset.csv": "Health",
    "religion_dataset.csv": "Religion"
}

# Loop through all files in the folder
for fichier, categorie in categories.items():
    complet_path = os.path.join(folder, fichier)
    df = pd.read_csv(complet_path, encoding='latin1')
    df['Hyperlinks_exist'] = df['Hyperlinks_exist'].map({'no': 0, 'yes': 1})
    df['Media_exists'] = df['Media_exists'].map({'no': 0, 'yes': 1})
    df['Classification'] = df['Classification'].map({'Misinformation': 0, 'Information': 1})
    df['Sentiment'] = df['Sentiment'].map({'negative': 0, 'neutral': 1, 'positive': 2})

    moyenne_classif = df['Classification'].mean()
    moyenne_sentiment = df['Sentiment'].mean()
    
    resultats_classif.append((categorie, moyenne_classif))
    resultats_sentiment.append((categorie, moyenne_sentiment))

# Sort results by mean
resultats_classif_sorted = sorted(resultats_classif, key=lambda x: x[1], reverse=False)
resultats_sentiment_sorted = sorted(resultats_sentiment, key=lambda x: x[1], reverse=False)

# Extract file names and means for each category
categories_classif, moyennes_classif = zip(*resultats_classif_sorted)
categories_sentiment, moyennes_sentiment = zip(*resultats_sentiment_sorted)

# Create bar plots
plt.figure(figsize=(10, 5))

# Plot for the 'Classification' column
plt.subplot(1, 2, 1)
plt.barh(categories_classif, moyennes_classif, color='skyblue')
plt.xlabel('Mean Classification')
plt.title('Mean classification by theme')

# Plot for the 'Sentiment' column
plt.subplot(1, 2, 2)
plt.barh(categories_sentiment, moyennes_sentiment, color='salmon')
plt.xlabel('Mean Sentiment')
plt.title('Mean sentiment by theme')

plt.tight_layout()
plt.show()
