import torch
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import xgboost as xgb
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import ConfusionMatrixDisplay

df = pd.read_csv('train_insta.csv')

# Mélanger aléatoirement les lignes du DataFrame
df_melange = df.sample(frac=1).reset_index(drop=True)

# Calcul de la taille de la première moitié
taille_premiere_moitie = len(df_melange) // 2

# Séparation du DataFrame en deux
train = df_melange[:taille_premiere_moitie]
test = df_melange[taille_premiere_moitie:]

# Convertir tab en DataFrame pandas
X_train = pd.DataFrame(train, columns=[
    '#posts','#followers','#follows'
])


# Enregistrer df_tab dans un fichier CSV
chemin_fichier_train_csv = './train_health_dataset.csv'  # Ajustez le chemin selon vos besoins
X_train.to_csv(chemin_fichier_train_csv, index=False, sep=',')

y_train = pd.DataFrame(train, columns= [
    'fake'
])

# Convertir tab en DataFrame pandas
X_test = pd.DataFrame(test, columns= [
    '#posts','#followers','#follows'
])
# X_test = pd.DataFrame(test, columns= [
#     'Favorites_count', 'Replies count'
# ])

# Enregistrer df_tab dans un fichier CSV
chemin_fichier_test_csv = './test_health_datatest.csv'  # Ajustez le chemin selon vos besoins
X_test.to_csv(chemin_fichier_test_csv, index=False, sep=',')

y_test = pd.DataFrame(test, columns= [
    'fake'
])


###############################################################################
# DATA PREPROCESSING
###############################################################################
scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)


# Define the vote types you want to train separate models for
votes = [ 'fake'] # Rename the repeated seizure_vote to something unique
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
    '#posts','#followers','#follows'
])

X_actual_test_scaled = scaler.transform(X_actual_test)

# Generate predictions for each vote type and store in the predictions dictionary
predictions = {}
for vote, model in models.items():
    predictions[vote] = model.predict(X_actual_test_scaled)
    
# Création du DataFrame avec les prédictions
predictions_df = pd.DataFrame(predictions)

predictions_df.insert(0, 'influencer_id', df_tab_actual_test['ID'])

# Exportation des prédictions en CSV
predictions_df.to_csv('final_predictions_train_insta.csv', index=False)





reference = X_train.mean()
n_points = 100
favorites_range = np.linspace(X_train['#followers'].min(), X_train['#followers'].max(), n_points)

predictions = []
for fav in favorites_range:
    temp = reference.copy()
    temp['#followers'] = fav
    temp_scaled = scaler.transform([temp])
    prediction = models['fake'].predict_proba(temp_scaled)[0][1]  # prédiction pour la classe positive
    predictions.append(prediction)

# Tracé de la courbe
plt.figure(figsize=(10, 6))
plt.plot(favorites_range, predictions, label='Probabilité de Classification')
plt.xlabel('Favorites_count')
plt.ylabel('Probabilité de Classification')
plt.title('Impact de Favorites_count sur la prédiction de Classification')
plt.legend()
plt.show()