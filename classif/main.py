import torch
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import xgboost as xgb
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import ConfusionMatrixDisplay
from sklearn.feature_extraction.text import TfidfVectorizer
from googletrans import Translator, LANGUAGES

df = pd.read_csv('health_dataset.csv')
df['Hyperlinks_exist'] = df['Hyperlinks_exist'].map({'no': 0, 'yes': 1})
df['Media_exists'] = df['Media_exists'].map({'no': 0, 'yes': 1})
df['Classification'] = df['Classification'].map({'Misinformation': 0, 'Information': 1})
df['Sentiment'] = df['Sentiment'].map({'negative': 0, 'neutral': 1, 'positive': 2})
df['Text'] = df['Tweet content']

# Séparer les données en deux ensembles : 0 et 1
df_0 = df[df['Classification'] == 0]
df_1 = df[df['Classification'] == 1]

# Calculer le nombre minimum de lignes pour équilibrer les deux ensembles
min_samples = min(len(df_0), len(df_1))

# Échantillonner aléatoirement le même nombre de lignes pour chaque ensemble
df_0_balanced = df_0.sample(n=min_samples, random_state=42)
df_1_balanced = df_1.sample(n=min_samples, random_state=42)

# Concaténer les ensembles équilibrés pour former le dataframe final
df_balanced = pd.concat([df_0_balanced, df_1_balanced])


vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')

df_melange = df.sample(frac=1).reset_index(drop=True)

# Split the data into training and test sets
train, test = df_melange[:len(df_melange) // 2], df_melange[len(df_melange) // 2:]

train = train.reset_index(drop=True)
test = test.reset_index(drop=True)

tweet_content_train = train['Tweet content']
tweet_content_test = test['Tweet content']

# Convertir tab en DataFrame pandas
X_train = pd.DataFrame(train, columns=[
    'Hyperlinks_exist', 'Media_exists','Favorites_count', 'Retweet_count', 'Replies count'
])

# Enregistrer df_tab dans un fichier CSV
chemin_fichier_train_csv = './train_health_dataset.csv'  # Ajustez le chemin selon vos besoins
X_train.to_csv(chemin_fichier_train_csv, index=False, sep=',')

y_train = pd.DataFrame(train, columns= [
    'Classification', 'Sentiment'
])

# Convertir tab en DataFrame pandas
X_test = pd.DataFrame(test, columns= [
    'Hyperlinks_exist', 'Media_exists','Favorites_count', 'Retweet_count', 'Replies count'
])

scaler = StandardScaler()

tweet_vectorized_train = vectorizer.fit_transform(tweet_content_train)
tweet_vectorized_train_df = pd.DataFrame(tweet_vectorized_train.toarray(), 
                                         columns=[f"word_{i}" for i in range(tweet_vectorized_train.shape[1])])

tweet_vectorized_test = vectorizer.transform(tweet_content_test)
tweet_vectorized_test_df = pd.DataFrame(tweet_vectorized_test.toarray(),
                                        columns=[f"word_{i}" for i in range(tweet_vectorized_train.shape[1])])


X_train_added = pd.concat([X_train, tweet_vectorized_train_df], axis=1)
X_test_added = pd.concat([X_test, tweet_vectorized_test_df], axis=1)

X_train_scaled = scaler.fit_transform(X_train_added)
X_test_scaled = scaler.fit_transform(X_test_added)

# Enregistrer df_tab dans un fichier CSV
chemin_fichier_test_csv = './test_health_datatest.csv'  # Ajustez le chemin selon vos besoins
X_test.to_csv(chemin_fichier_test_csv, index=False, sep=',')

y_test = pd.DataFrame(test, columns= [
    'Classification','Sentiment'
])
y_test = y_test.reset_index(drop=True)


###############################################################################
# DATA PREPROCESSING
###############################################################################



# Define the vote types you want to train separate models for
votes = ['Classification','Sentiment'] # Rename the repeated seizure_vote to something unique
models = {}  
confusion_matrices = {} 


for vote in votes:

    label_encoder = LabelEncoder()
    y_train_encoded = label_encoder.fit_transform(y_train[vote])

    # Initialize the model
    clf = xgb.XGBClassifier(objective='binary:logistic', verbosity=1, use_label_encoder=False, eval_metric='logloss')
    clf.fit(X_train_scaled, y_train_encoded)

    # Store the trained model in the models dictionary
    models[vote] = clf

    # Predict on the test data
    y_pred_encoded = clf.predict(X_test_scaled)
    y_pred = label_encoder.inverse_transform(y_pred_encoded)

    # Calcul et affichage de la matrice de confusion
    cm = confusion_matrix(y_test[vote], y_pred)
    confusion_matrices[vote] = cm
    disp = ConfusionMatrixDisplay(confusion_matrix=cm)
    disp.plot(cmap=plt.cm.Blues)
    plt.title(f'Confusion Matrix for {vote}')
    plt.show()



# TEST

# Créer un objet traducteur
translator = Translator()

# Fonction pour traduire du texte
def translate_text(text, dest_language='en'):
    try:
        # Tentative de traduction
        translation = translator.translate(text, dest=dest_language)
        return translation.text
    except Exception as e:
        print(f"Erreur de traduction: {e}")
        return text

df_tab_actual_test = pd.read_csv('health_datatest.csv')

X_actual_test = pd.DataFrame(df_tab_actual_test, columns=[
    'Hyperlinks_exist', 'Media_exists', 'Favorites_count', 'Retweet_count', 'Replies count'
])

# Traduction des tweets
df_tab_actual_test['Translated_Tweet'] = df_tab_actual_test['Tweet content'].apply(lambda x: translate_text(x, 'en'))


tweet_content_actual_test = df_tab_actual_test['Tweet content']
tweet_vectorized_actual_test = vectorizer.transform(tweet_content_actual_test)
tweet_vectorized_actual_test_df = pd.DataFrame(tweet_vectorized_actual_test.toarray(),
                                               columns=[f"word_{i}" for i in range(tweet_vectorized_train.shape[1])])

X_actual_test_added = pd.concat([X_actual_test, tweet_vectorized_actual_test_df], axis=1)

# Generate predictions for each vote type and store in the predictions dictionary
predictions = {}
for vote, model in models.items():
    predictions[vote] = model.predict(X_actual_test_added)
    
# Création du DataFrame avec les prédictions
predictions_df = pd.DataFrame(predictions)

predictions_df.insert(0, 'is_verified', df_tab_actual_test['Media_exists'])
predictions_df.insert(0, 'posts_count', df_tab_actual_test['Posts'])
predictions_df.insert(0, 'comments_count', df_tab_actual_test['Replies count'])
predictions_df.insert(0, 'shares_count', df_tab_actual_test['Retweet_count'])
predictions_df.insert(0, 'likes_count', df_tab_actual_test['Favorite_count'])
predictions_df.insert(0, 'followers_count', df_tab_actual_test['Followers'])
predictions_df.insert(0, 'Translated_Tweet', df_tab_actual_test['Translated_Tweet'])
predictions_df.insert(0, 'username', df_tab_actual_test['Channel Name'])
predictions_df.insert(0, 'influencer_id', df_tab_actual_test['ID'])

def calculate_total(row):
    if row['Classification'] == 1:
        return row['Classification'] + row['Sentiment'] + 3
    else:
        return row['Classification'] + row['Sentiment']

predictions_df['Total_Score'] = predictions_df.apply(calculate_total, axis=1)


# Exportation des prédictions en CSV
predictions_df.to_csv('final_predictions_top_insta.csv', index=False)



# Sélection d'une observation de référence
reference = X_train.mean()

# Création de points de données simulés pour l'impact de 'Favorites_count'
n_points = 100
favorites_range = np.linspace(X_train['Favorites_count'].min(), X_train['Favorites_count'].max(), n_points)
predictions = []

# Définir les paramètres pour lesquels vous voulez étudier l'impact
parameters = ['Hyperlinks_exist', 'Media_exists', 'Favorites_count', 'Retweet_count', 'Replies count']

# Boucle sur chaque paramètre
for parameter in parameters:
    # Générer une plage de valeurs pour le paramètre
    parameter_range = np.linspace(df[parameter].min(), df[parameter].max(), 100)

    # Stocker les prédictions pour ce paramètre
    predictions = []

    # Boucle sur chaque valeur de la plage du paramètre
    for value in parameter_range:
        # Créer une copie de la référence et définir la valeur du paramètre
        temp = reference.copy()
        temp[parameter] = value

        # Ajouter des placeholders pour les caractéristiques de texte vectorisées
        temp_text_features = [0] * 1000  # Placeholder pour les caractéristiques de texte vectorisées
        temp_full = np.concatenate([temp.values, temp_text_features])

        # Transformation avec StandardScaler
        temp_scaled = scaler.transform([temp_full])

        # Prédiction pour la classe positive
        prediction = models['Classification'].predict_proba(temp_scaled)[0][1]
        predictions.append(prediction)

    # Tracé de la courbe pour ce paramètre
    plt.figure(figsize=(10, 6))
    plt.plot(parameter_range, predictions, label='Probabilité de Classification')
    plt.xlabel(parameter)
    plt.ylabel('Probabilité de Classification')
    plt.title(f'Impact de {parameter} sur la prédiction de Classification')
    plt.legend()
    plt.show()


# Affichage du classement des mots les plus utilisés lorsque la classification est égale à 0
if 'Classification' in df.columns:
    # Filtrer les prédictions où la classification est égale à 0
    classification_0_df = df[df['Classification'] == 0]

    # Concaténer tous les tweets lorsque la classification est égale à 0
    all_tweets_classification_0 = " ".join(classification_0_df['Text'])

    # Vectoriser les tweets
    vectorizer_classification_0 = TfidfVectorizer(max_features=1000, stop_words='english')
    tweet_vectorized_classification_0 = vectorizer_classification_0.fit_transform([all_tweets_classification_0])

    # Obtenir les noms des mots
    feature_names = vectorizer_classification_0.get_feature_names_out()

    # Calculer les scores TF-IDF moyens pour chaque mot
    mean_tfidf_scores = np.mean(tweet_vectorized_classification_0.toarray(), axis=0)

    # Créer un DataFrame pour le classement des mots
    words_ranking_df = pd.DataFrame({'Word': feature_names, 'Mean_TFIDF_Score': mean_tfidf_scores})

    # Trier les mots par score TF-IDF moyen
    words_ranking_df = words_ranking_df.sort_values(by='Mean_TFIDF_Score', ascending=False)

    # Affichage des 10 premiers mots
    print("Classement des mots les plus utilisés lorsque la classification est égale à 0:")
    print(words_ranking_df.head(30))
