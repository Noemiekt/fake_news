import torch
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import xgboost as xgb
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import ConfusionMatrixDisplay

# Charger le fichier CSV
df = pd.read_csv('crisis_dataset.csv')

# Supprimer la première colonne
df = df.iloc[:, 1:]  # iloc[:, 1:] sélectionne toutes les lignes et les colonnes à partir de la deuxième

# Sauvegarder le nouveau DataFrame dans un nouveau fichier CSV
df.to_csv('crisis_dataset.csv', index=False)

df = pd.read_csv('health_dataset.csv')
df['Hyperlinks_exist'] = df['Hyperlinks_exist'].map({'no': 0, 'yes': 1})
df['Media_exists'] = df['Media_exists'].map({'no': 0, 'yes': 1})
df['Classification'] = df['Classification'].map({'Misinformation': 0, 'Information': 1})
df['Subjectivity'] = df['Subjectivity'].map({'negative': 0, 'neutral': 1, 'positive': 2})

# Mélanger aléatoirement les lignes du DataFrame
df_melange = df.sample(frac=1).reset_index(drop=True)

# Calcul de la taille de la première moitié
taille_premiere_moitie = len(df_melange) // 2

# Séparation du DataFrame en deux
train = df_melange[:taille_premiere_moitie]
test = df_melange[taille_premiere_moitie:]

# Convertir tab en DataFrame pandas
X_train = pd.DataFrame(train, columns=[
    'ID','Hyperlinks_exist', 'Media_exists','Subjectivity','Favorites_count', 'Retweet_count', 'Replies count'
])


# Enregistrer df_tab dans un fichier CSV
chemin_fichier_train_csv = './train_health_dataset.csv'  # Ajustez le chemin selon vos besoins
X_train.to_csv(chemin_fichier_train_csv, index=False, sep=',')

y_train = pd.DataFrame(train, columns= [
    'Classification', 'Subjectivity'
])

# Convertir tab en DataFrame pandas
X_test = pd.DataFrame(test, columns= [
    'ID','Hyperlinks_exist', 'Media_exists','Subjectivity','Favorites_count', 'Retweet_count', 'Replies count'
])
# Enregistrer df_tab dans un fichier CSV
chemin_fichier_test_csv = './test_health_datatest.csv'  # Ajustez le chemin selon vos besoins
X_test.to_csv(chemin_fichier_test_csv, index=False, sep=',')

y_test = pd.DataFrame(test, columns= [
    'Classification','Subjectivity'
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

X_actual_test = pd.DataFrame(df_tab_actual_test, columns=[
    'ID','Hyperlinks_exist', 'Media_exists', 'Subjectivity', 'Favorites_count', 'Retweet_count', 'Replies count'
])
X_actual_test_scaled = scaler.transform(X_actual_test)

# Generate predictions for each vote type and store in the predictions dictionary
predictions = {}
for vote, model in models.items():
    predictions[vote] = model.predict(X_actual_test_scaled)
    
# Création du DataFrame avec les prédictions
predictions_df = pd.DataFrame(predictions)
predictions_df.insert(0, 'ID', df_tab_actual_test['ID'])

# Affichage des premières lignes pour vérification
print(predictions_df.head())

# Exportation des prédictions en CSV
predictions_df.to_csv('final_predictions.csv', index=False)
