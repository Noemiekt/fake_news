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
from matplotlib import cm

cmap = cm.get_cmap('viridis')


df = pd.read_csv('final_prediction_total.csv')
df['Text'] = df['post_content']

vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')

df_melange = df.sample(frac=1).reset_index(drop=True)

# Split the data into training and test sets
train, test = df_melange[:len(df_melange) // 2], df_melange[len(df_melange) // 2:]

train = train.reset_index(drop=True)
test = test.reset_index(drop=True)

tweet_content_train = train['post_content']
tweet_content_test = test['post_content']

# Convertir tab en DataFrame pandas
X_train = pd.DataFrame(train, columns=[
    'followers_count','likes_count','shares_count','comments_count','view_count','engagement_rate','posts_count','sentiment'
])

# Enregistrer df_tab dans un fichier CSV
chemin_fichier_train_csv = './train.csv'  # Ajustez le chemin selon vos besoins
X_train.to_csv(chemin_fichier_train_csv, index=False, sep=',')

y_train = pd.DataFrame(train, columns= [
    'total'
])

# Convertir tab en DataFrame pandas
X_test = pd.DataFrame(test, columns= [
    'followers_count','likes_count','shares_count','comments_count','view_count','engagement_rate','posts_count','sentiment'
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
chemin_fichier_test_csv = './test.csv'  # Ajustez le chemin selon vos besoins
X_test.to_csv(chemin_fichier_test_csv, index=False, sep=',')

y_test = pd.DataFrame(test, columns= [
    'total'
])
y_test = y_test.reset_index(drop=True)


###############################################################################
# DATA PREPROCESSING
###############################################################################



# Define the vote types you want to train separate models for
votes = ['total'] # Rename the repeated seizure_vote to something unique
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


# Sélection d'une observation de référence
reference = X_train.mean()

# Définir les paramètres pour lesquels vous voulez étudier l'impact
parameters = ['followers_count','likes_count','shares_count','comments_count','view_count','engagement_rate','posts_count','sentiment']

# Boucle sur chaque paramètre
for parameter in parameters:
    # Générer une plage de valeurs pour le paramètre
    parameter_range = np.linspace(df[parameter].min(), df[parameter].max(), 31)

    # Stocker les prédictions pour ce paramètre
    predictions = []

    # Boucle sur chaque valeur de la plage du paramètre
    for value in parameter_range:
        # Créer une copie de la référence et définir la valeur du paramètre
        temp = reference.copy()
        temp[parameter] = value


        # Ajouter des placeholders pour les caractéristiques de texte vectorisées
        num_text_features = len(tweet_vectorized_train_df.columns)
        temp_text_features = [0] * num_text_features
        temp_full = np.concatenate([temp.values, temp_text_features])

        # Transformation avec StandardScaler
        temp_scaled = scaler.transform([temp_full])

        prediction = models['total'].predict_proba(temp_scaled)[0][2]  # Prédiction pour la classe positive
        print(prediction)
        predictions.append(prediction)

        # Prédiction pour la classe positive)
        # if (models['total'].predict_proba(temp_scaled).shape[1] >= 6 ):
        #     prediction1 = models['total'].predict_proba(temp_scaled)[0][4]
        #     prediction2 = models['total'].predict_proba(temp_scaled)[0][5]
        #     prediction3 = models['total'].predict_proba(temp_scaled)[0][3]

        #     # print((prediction1+prediction2+prediction3))

        #     predictions.append((prediction1+prediction2+prediction3))
        # else :
        #     predictions.append([])

       
        
    # Tracé de la courbe pour ce paramètre
    plt.figure(figsize=(10, 6))
    plt.plot(parameter_range, predictions, label='Probabilité de Classification')
    plt.xlabel(parameter)
    plt.ylabel('Probabilité de Classification')
    plt.title(f'Impact de {parameter} sur la prédiction de Classification')
    plt.legend()
    # plt.ylim(0, 1)  # Définition de l'intervalle de l'axe des ordonnées
    plt.show()

    # Tracé de l'histogramme pour ce paramètre
    plt.figure(figsize=(10, 6)) 
    bar_width = 0.9 * (parameter_range[1] - parameter_range[0])

    # Création d'un colormap et normalisation
    cmap = plt.get_cmap('coolwarm')  # Essayez 'coolwarm', 'cividis', ou 'spring' pour des effets différents
    norm = plt.Normalize(min(predictions), max(predictions))

    bars = plt.bar(parameter_range, predictions, width=bar_width, color=cmap(norm(predictions)))

    plt.xlabel('Likes Count')  # Remplacer par le nom de votre paramètre
    plt.ylabel('Probabilité de Classification')
    plt.title(f'Impact de {parameter} sur la prédiction de Classification')
    min_prob = min(predictions)
    max_prob = max(predictions)
    plt.ylim(min_prob - 0.1 * (max_prob - min_prob), max_prob + 0.1 * (max_prob - min_prob))
    plt.grid(True)
    plt.show()

# Affichage du classement des mots les plus utilisés lorsque la classification est égale à 0
if 'total' in df.columns:
    # Filtrer les prédictions où la classification est égale à 0
    classification_0_df = df[df['total'] == 0]

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

    # Filtrer les mots ayant plus de 4 lettres
    words_ranking_df = words_ranking_df[words_ranking_df['Word'].apply(lambda x: len(x) >= 4)]

    # Trier les mots par score TF-IDF moyen
    words_ranking_df = words_ranking_df.sort_values(by='Mean_TFIDF_Score', ascending=False)

    # Affichage des 10 premiers mots
    print("Classement des mots les plus utilisés lorsque la classification est égale à 0 avec plus de 4 lettres:")
    print(words_ranking_df.head(30))

