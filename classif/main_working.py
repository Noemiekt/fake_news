import torch
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import xgboost as xgb
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import ConfusionMatrixDisplay
from matplotlib import cm

cmap = cm.get_cmap('viridis')

df = pd.read_csv('health_dataset.csv')
df['Hyperlinks_exist'] = df['Hyperlinks_exist'].map({'no': 0, 'yes': 1})
df['Media_exists'] = df['Media_exists'].map({'no': 0, 'yes': 1})
df['Classification'] = df['Classification'].map({'Misinformation': 0, 'Information': 1})
df['Sentiment'] = df['Sentiment'].map({'negative': 0, 'neutral': 1, 'positive': 2})

# Séparer les données en deux DataFrame basés sur la classification
df_0 = df[df['Classification'] == 0]
df_1 = df[df['Classification'] == 1]

# Compter le nombre de lignes avec 0 et 1 en Classification
count_0 = df_0.shape[0]
count_1 = df_1.shape[0]

# Si le nombre de lignes avec 1 est supérieur, échantillonner aléatoirement le DataFrame de 1 pour avoir le même nombre de lignes que celui de 0
if count_1 > count_0:
    df_1_sampled = df_1.sample(n=count_0, replace=False)
    # Concaténer les deux DataFrames pour obtenir un DataFrame équilibré
    df_balanced = pd.concat([df_0, df_1_sampled])
else:
    df_balanced = pd.concat([df_0, df_1])

# Mélanger aléatoirement les lignes du DataFrame équilibré
df_balanced = df_balanced.sample(frac=1).reset_index(drop=True)

# Vérifier que les classes sont équilibrées
print(df_balanced['Classification'].value_counts())

# Enregistrer le DataFrame équilibré dans un fichier CSV
df_balanced.to_csv('health_dataset_balanced.csv', index=False)


# Mélanger aléatoirement les lignes du DataFrame
df_melange = df_balanced.sample(frac=1).reset_index(drop=True)

# Calcul de la taille de la première moitié
taille_premiere_moitie = len(df_melange) // 2

# Séparation du DataFrame en deux
train = df_melange[:taille_premiere_moitie]
test = df_melange[taille_premiere_moitie:]

# Convertir tab en DataFrame pandas
X_train = pd.DataFrame(train, columns=[
    'Favorites_count', 'Retweet_count', 'Replies count', 'Compound', 'Sentiment'
])

# X_train = pd.DataFrame(train, columns=[
#     'Favorites_count','Replies count'
# ])


# Enregistrer df_tab dans un fichier CSV
chemin_fichier_train_csv = './train_health_dataset.csv'  # Ajustez le chemin selon vos besoins
X_train.to_csv(chemin_fichier_train_csv, index=False, sep=',')

y_train = pd.DataFrame(train, columns= [
    'Classification'
])

# Convertir tab en DataFrame pandas
X_test = pd.DataFrame(test, columns= [
    'Favorites_count', 'Retweet_count', 'Replies count', 'Compound', 'Sentiment'
])
# X_test = pd.DataFrame(test, columns= [
#     'Favorites_count', 'Replies count'
# ])

# Enregistrer df_tab dans un fichier CSV
chemin_fichier_test_csv = './test_health_datatest.csv'  # Ajustez le chemin selon vos besoins
X_test.to_csv(chemin_fichier_test_csv, index=False, sep=',')

y_test = pd.DataFrame(test, columns= [
    'Classification'
])


###############################################################################
# DATA PREPROCESSING
###############################################################################
scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)


# Define the vote types you want to train separate models for
votes = ['Classification'] # Rename the repeated seizure_vote to something unique
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

    # Compute the confusion matrix
    cm = confusion_matrix(y_test[vote], y_pred)
    confusion_matrices[vote] = cm

    # Display the confusion matrix
    disp = ConfusionMatrixDisplay(confusion_matrix=cm)
    disp.plot(cmap=plt.cm.Blues)
    plt.title(f'Confusion Matrix for {vote}')
    plt.show()



# TEST
df_tab_actual_test = pd.read_csv('health_datatest.csv')
# df_tab_actual_test = pd.read_csv('top_200_instagrammers.csv')

X_actual_test = pd.DataFrame(df_tab_actual_test, columns=[
    'Favorites_count', 'Retweet_count', 'Replies count', 'Compound', 'Sentiment'
])
# X_actual_test = pd.DataFrame(df_tab_actual_test, columns=[
#     'Favorites_count', 'Replies count'
# ])

X_actual_test_scaled = scaler.transform(X_actual_test)

# Generate predictions for each vote type and store in the predictions dictionary
predictions = {}
for vote, model in models.items():
    predictions[vote] = model.predict(X_actual_test_scaled)
    
# Création du DataFrame avec les prédictions
predictions_df = pd.DataFrame(predictions)

predictions_df.insert(0, 'is_verified', df_tab_actual_test['Media_exists'])
predictions_df.insert(0, 'posts_count', df_tab_actual_test['Posts'])
predictions_df.insert(0, 'engagement_rate', df_tab_actual_test['Engagement Rate'])
predictions_df.insert(0, 'view_count', df_tab_actual_test['View_count'])
predictions_df.insert(0, 'comments_count', df_tab_actual_test['Replies count'])
predictions_df.insert(0, 'shares_count', df_tab_actual_test['Retweet_count'])
predictions_df.insert(0, 'likes_count', df_tab_actual_test['Favorite_count'])
predictions_df.insert(0, 'followers_count', df_tab_actual_test['Followers'])
predictions_df.insert(0, 'post_content', df_tab_actual_test['Post content'])
predictions_df.insert(0, 'username', df_tab_actual_test['Channel Name'])
predictions_df.insert(0, 'influencer_id', df_tab_actual_test['ID'])

# def calculate_total(row):
#     if row['Classification'] == 1:
#         return row['Classification'] + row['Sentiment'] + 3
#     else:
#         return row['Classification'] + row['Sentiment']

# predictions_df['Total_Score'] = predictions_df.apply(calculate_total, axis=1)


# Exportation des prédictions en CSV
predictions_df.to_csv('final_predictions_top_insta.csv', index=False)



reference = X_train.mean()

# Paramètres à tester
parameters = ['Favorites_count', 'Retweet_count', 'Replies count']

# Boucle sur chaque paramètre
for parameter in parameters:
    # Création de la plage de valeurs pour le paramètre
    min_value = X_train[parameter].min()
    max_value = X_train[parameter].max()
    parameter_range = np.linspace(min_value, max_value, 30)  # 100 points dans la plage

    # Stocker les prédictions pour ce paramètre
    predictions = []

    # Boucle sur chaque valeur de la plage du paramètre
    for value in parameter_range:
        temp = reference.copy()
        temp[parameter] = value  # Affectation de la valeur du paramètre
        temp_scaled = scaler.transform([temp.values])  # Assurez-vous de transformer le DataFrame correctement
        prediction = models['Classification'].predict_proba(temp_scaled)[0][1]  # Prédiction pour la classe positive
        predictions.append(prediction)

    # Tracé de la courbe pour ce paramètre
    plt.figure(figsize=(10, 6))
    plt.plot(parameter_range, predictions, label='Probabilité de Classification')
    plt.xlabel(parameter)
    plt.ylabel('Probabilité de Classification')
    plt.title(f'Impact de {parameter} sur la prédiction de Classification')
    plt.legend()
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