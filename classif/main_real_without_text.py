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

df = pd.read_csv('final_prediction_total.csv')

vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')

df_melange = df.sample(frac=1).reset_index(drop=True)

# Split the data into training and test sets
train, test = df_melange[:len(df_melange) // 2], df_melange[len(df_melange) // 2:]

train = train.reset_index(drop=True)
test = test.reset_index(drop=True)


# Convertir tab en DataFrame pandas
X_train = pd.DataFrame(train, columns=[
    'followers_count','likes_count','shares_count','comments_count','view_count','engagement_rate','posts_count','is_verified'
])

# Enregistrer df_tab dans un fichier CSV
chemin_fichier_train_csv = './train.csv'  # Ajustez le chemin selon vos besoins
X_train.to_csv(chemin_fichier_train_csv, index=False, sep=',')

y_train = pd.DataFrame(train, columns= [
    'total'
])

# Convertir tab en DataFrame pandas
X_test = pd.DataFrame(test, columns= [
    'followers_count','likes_count','shares_count','comments_count','view_count','engagement_rate','posts_count','is_verified'
])

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
scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)



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
parameters = ['followers_count', 'likes_count', 'shares_count', 'comments_count', 'view_count', 'engagement_rate', 'posts_count', 'is_verified']
# parameters = ['followers_count']

# Boucle sur chaque paramètre
for parameter in parameters:
    # Générer une plage de valeurs pour le paramètre
    parameter_range = np.linspace(df[parameter].min(), df[parameter].max(), 1000)

    # Stocker les valeurs de 'total' pour ce paramètre
    total_values = []

    # Boucle sur chaque valeur de la plage du paramètre
    for value in parameter_range:

        
        # Créer une copie de la référence et définir la valeur du paramètre
        temp = reference.copy()
        temp[parameter] = value

        # Transformation avec StandardScaler
        temp_scaled = scaler.transform([temp])
        

        # Prédiction pour la classe positive
        prediction = models['total'].predict(temp_scaled)
        total_values.append(prediction)

    # Créer une DataFrame Pandas pour stocker les valeurs de 'total'
    total_df = pd.DataFrame({'total': total_values})

    # Ajouter la DataFrame total_df à df comme une nouvelle colonne
    df[parameter + '_total'] = total_df

    # Tracé de la courbe pour ce paramètre
    plt.figure(figsize=(10, 6))
    plt.plot(parameter_range, total_values, label='Valeur de Total')
    plt.xlabel(parameter)
    plt.ylabel('Total')
    plt.title(f'Impact de {parameter} sur la prédiction de Total')
    plt.legend()
    plt.show()



# Définir les paramètres pour lesquels vous voulez créer des scatterplots
parameters = ['followers_count', 'likes_count', 'shares_count', 'comments_count', 'view_count', 'engagement_rate', 'posts_count', 'is_verified']

# Boucle sur chaque paramètre
for parameter in parameters:
    # Créer une nouvelle figure
    plt.figure(figsize=(10, 6))

    # Créer un scatterplot pour le paramètre actuel
    plt.scatter(df[parameter], df['total'], alpha=0.5, label=parameter)

    # Calculer la moyenne de 'total' pour chaque valeur de 'parameter'
    mean_total = df.groupby(parameter)['total'].mean()

    # Conversion de l'index et des valeurs en tableaux NumPy
    mean_total_index = np.array(mean_total.index)
    mean_total_values = np.array(mean_total.values)

    # Traçage de la courbe moyenne
    plt.plot(mean_total_index, mean_total_values, label=f'Moyenne de {parameter}', color='red')

    # Ajouter des étiquettes et un titre au graphique
    plt.xlabel('Valeur du Paramètre')
    plt.ylabel('Classification')
    plt.title(f'Relation entre {parameter} et la Classification avec Moyenne')
    plt.xticks(rotation=45)  # Rotation des étiquettes de l'axe des abscisses pour une meilleure lisibilité si nécessaire
    plt.grid(True)
    plt.legend()
    plt.show()