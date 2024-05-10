import torch
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import xgboost as xgb
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import ConfusionMatrixDisplay

df = pd.read_csv('fake_bot_real_account_data.csv')
df['Account type'] = df['Account type'].map({'Fake': 0, 'Bot': 0, 'Real':1})

# Mélanger aléatoirement les lignes du DataFrame
df_melange = df.sample(frac=1).reset_index(drop=True)

# Calcul de la taille de la première moitié
taille_premiere_moitie = len(df_melange) // 2

# Séparation du DataFrame en deux
train = df_melange[:taille_premiere_moitie]
test = df_melange[taille_premiere_moitie:]

# Convertir tab en DataFrame pandas
X_train = pd.DataFrame(train, columns=[
    'Followers', 'Post count','Average number of media likes', 'Followings','Bio length'
])

# X_train = pd.DataFrame(train, columns=[
#     'Favorites_count','Replies count'
# ])


# Enregistrer df_tab dans un fichier CSV
chemin_fichier_train_csv = './train_health_dataset.csv'  # Ajustez le chemin selon vos besoins
X_train.to_csv(chemin_fichier_train_csv, index=False, sep=',')

y_train = pd.DataFrame(train, columns= [
    'Account type'
])

# Convertir tab en DataFrame pandas
X_test = pd.DataFrame(test, columns= [
    'Followers', 'Post count','Average number of media likes', 'Followings','Bio length'
])
# X_test = pd.DataFrame(test, columns= [
#     'Favorites_count', 'Replies count'
# ])

# Enregistrer df_tab dans un fichier CSV
chemin_fichier_test_csv = './test_health_datatest.csv'  # Ajustez le chemin selon vos besoins
X_test.to_csv(chemin_fichier_test_csv, index=False, sep=',')

y_test = pd.DataFrame(test, columns= [
    'Account type'
])


###############################################################################
# DATA PREPROCESSING
###############################################################################
scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)


# Define the vote types you want to train separate models for
votes = ['Account type'] # Rename the repeated seizure_vote to something unique
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
df_tab_actual_test = pd.read_csv('fake_bot_datatest.csv')
# df_tab_actual_test = pd.read_csv('top_200_instagrammers.csv')

X_actual_test = pd.DataFrame(df_tab_actual_test, columns=[
    'Followers', 'Post count','Average number of media likes', 'Followings','Bio length'
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

# predictions_df.insert(0, 'is_verified', df_tab_actual_test['Media_exists'])
# predictions_df.insert(0, 'posts_count', df_tab_actual_test['Posts'])
# predictions_df.insert(0, 'comments_count', df_tab_actual_test['Replies count'])
# predictions_df.insert(0, 'shares_count', df_tab_actual_test['Retweet_count'])
# predictions_df.insert(0, 'likes_count', df_tab_actual_test['Favorite_count'])
# predictions_df.insert(0, 'followers_count', df_tab_actual_test['Followers'])
predictions_df.insert(0, 'Followings', df_tab_actual_test['Followings'])
predictions_df.insert(0, 'username', df_tab_actual_test['Channel Name'])
predictions_df.insert(0, 'influencer_id', df_tab_actual_test['ID'])

# Exportation des prédictions en CSV
predictions_df.to_csv('final_predictions_fake_bot.csv', index=False)



reference = X_train.mean()

# Paramètres à tester
parameters = ['Followers', 'Post count','Average number of media likes', 'Followings']

# Boucle sur chaque paramètre
for parameter in parameters:
    # Création de la plage de valeurs pour le paramètre
    min_value = X_train[parameter].min()
    max_value = X_train[parameter].max()
    parameter_range = np.linspace(min_value, max_value, 400)  # 100 points dans la plage

    # Stocker les prédictions pour ce paramètre
    predictions = []

    # Boucle sur chaque valeur de la plage du paramètre
    for value in parameter_range:
        temp = reference.copy()
        temp[parameter] = value  # Affectation de la valeur du paramètre
        temp_scaled = scaler.transform([temp.values])  # Assurez-vous de transformer le DataFrame correctement
        prediction = models['Account type'].predict_proba(temp_scaled)[0][1]  # Prédiction pour la classe positive
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
    plt.xlim(0,250)
    plt.ylim(min_prob - 0.1 * (max_prob - min_prob), max_prob + 0.1 * (max_prob - min_prob))
    plt.grid(True)
    plt.show()

