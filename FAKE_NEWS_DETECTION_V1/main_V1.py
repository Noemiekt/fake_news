import pandas as pd
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense
from tensorflow.keras.optimizers import Adam
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# Charger les données
fake_df1 = pd.read_csv('gossipcop_fake.csv')
fake_df2 = pd.read_csv('politifact_fake.csv')
real_df1 = pd.read_csv('gossipcop_real.csv')
real_df2 = pd.read_csv('politifact_real.csv')

# Utiliser la colonne 'title' pour le texte des articles
fake_df1['text'] = fake_df1['title']
fake_df2['text'] = fake_df1['title']
real_df1['text'] = real_df2['title']
real_df2['text'] = real_df2['title']

# Ajouter les étiquettes
fake_df1['label'] = 'FAKE'
fake_df2['label'] = 'FAKE'
real_df1['label'] = 'REAL'
real_df2['label'] = 'REAL'

# Fusionner les données
frames = [fake_df1, fake_df2, real_df1, real_df2]
data = pd.concat(frames, ignore_index=True)

# Prétraitement des données
texts = data['text'].apply(lambda x: str(x).lower())  # Convertir en minuscule

# Tokenisation
tokenizer = Tokenizer(num_words=10000, oov_token="<OOV>")
tokenizer.fit_on_texts(texts)
sequences = tokenizer.texts_to_sequences(texts)
padded_sequences = pad_sequences(sequences, maxlen=200, padding='post', truncating='post')

# Encodage des étiquettes
label_encoder = LabelEncoder()
labels = label_encoder.fit_transform(data['label'])

# Séparation des données en ensembles d'entraînement et de test
X_train, X_test, y_train, y_test = train_test_split(padded_sequences, labels, test_size=0.2, random_state=42)

# Construction du modèle LSTM
model = Sequential()
model.add(Embedding(10000, 64))  
model.add(LSTM(64))
model.add(Dense(1, activation='sigmoid'))


model.compile(loss='binary_crossentropy', optimizer=Adam(learning_rate=0.001), metrics=['accuracy'])

# Entraînement du modèle
model.fit(X_train, y_train, epochs=10, batch_size=32, validation_split=0.2)

# Évaluation du modèle
test_loss, test_accuracy = model.evaluate(X_test, y_test)
print(f'Test Loss: {test_loss}')
print(f'Test Accuracy: {test_accuracy}')



# Après l'évaluation du modèle, vous pouvez faire des prédictions sur l'ensemble de test
# Voici comment obtenir les prédictions pour les premières 5 entrées de l'ensemble de test
sample_test_data = X_test[:5]
sample_test_labels = y_test[:5]
predictions = model.predict(sample_test_data)

# Pour afficher les prédictions avec leurs étiquettes réelles
for i, prediction in enumerate(predictions):
    print(f'Article: {sample_test_data[i]}')
    print(f'Predicted label: {"FAKE" if prediction < 0.5 else "REAL"}, Actual label: {"FAKE" if sample_test_labels[i] == 0 else "REAL"}\n')




# # Remplacez ceci avec votre texte d'article réel pour le tester
# #real_article_title = "Scientists Confirm Earth's Inner Core Oscillates, Contradicting Previous Models"
# real_article_title = "Teen Mom Star Jenelle Evans' Wedding Dress Is Available Here for $2999"

# # Remplacez ceci avec votre texte d'article fake pour le tester
# #fake_article_title = "Celebrity Spotted Riding a Dragon in Downtown Los Angeles"
# fake_article_title = "Taylor Swift Reportedly Reacts To Tom Hiddleston’s Golden Globes Win"

# # Convertir en séquences et ajouter le padding
# real_article_sequence = tokenizer.texts_to_sequences([real_article_title])
# real_article_padded = pad_sequences(real_article_sequence, maxlen=200, padding='post', truncating='post')

# fake_article_sequence = tokenizer.texts_to_sequences([fake_article_title])
# fake_article_padded = pad_sequences(fake_article_sequence, maxlen=200, padding='post', truncating='post')

# # Faire des prédictions
# real_article_prediction = model.predict(real_article_padded)
# fake_article_prediction = model.predict(fake_article_padded)

# print(f"Le titre réel est prédit comme : {'FAKE' if real_article_prediction[0] < 0.5 else 'REAL'}")
# print(f"Le titre fake est prédit comme : {'FAKE' if fake_article_prediction[0] < 0.5 else 'REAL'}")

# Tester le modèle avec de nouveaux exemples
new_articles = [
    "Scientists Confirm Earth's Inner Core Oscillates, Contradicting Previous Models",
    "Celebrity Spotted Riding a Dragon in Downtown Los Angeles"
]

for article in new_articles:
    sequence = tokenizer.texts_to_sequences([article])
    padded = pad_sequences(sequence, maxlen=200, padding='post', truncating='post')
    prediction = model.predict(padded)
    print(f"Le titre '{article}' est prédit comme : {'FAKE' if prediction[0] < 0.5 else 'REAL'}")
