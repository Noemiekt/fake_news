# Détection de Fake News

## Vue d'Ensemble
Ce projet vise à développer un modèle d'apprentissage automatique capable de classifier avec précision les articles de presse comme "FAKE" (faux) ou "REAL" (vrai). Nous utilisons un réseau LSTM (Long Short-Term Memory), qui convient bien aux problèmes de prédiction de séquences, pour traiter les données textuelles et effectuer la classification.

## Modèle LSTM

Le modèle LSTM (Long Short-Term Memory) est un type de réseau de neurones récurrents (RNN) spécialisé dans l'apprentissage de dépendances à long terme dans les données séquentielles. Contrairement aux RNNs classiques, qui peuvent souffrir de problèmes de disparition ou d'explosion du gradient sur de longues séquences, les LSTMs sont capables de conserver l'information sur de longues périodes grâce à leur architecture unique en portes :

- **Porte d'oubli (Forget Gate)** : décide de l'information à conserver ou à éliminer du contexte.
- **Porte d'entrée (Input Gate)** : met à jour l'état de la cellule avec de nouvelles informations.
- **Porte de sortie (Output Gate)** : détermine la sortie finale du réseau à l'étape courante, en fonction de l'état de la cellule actuel et du contexte.

Grâce à ces mécanismes, les LSTMs sont très efficaces pour des tâches telles que la classification de textes, la traduction automatique, la reconnaissance vocale et plus encore. Dans ce projet, nous utilisons un LSTM pour analyser les titres d'articles et apprendre à distinguer les nuances et les motifs qui peuvent indiquer s'ils sont vrais ou faux.

## Données
Le jeu de données comprend des articles de presse collectés à partir de différentes sources et étiquetés soit comme "FAKE" soit comme "REAL". Nous avons des fichiers CSV séparés pour les articles faux et réels, et les données sont structurées avec des colonnes pour l'ID de l'article, l'URL, le titre et les IDs des tweets associés.

## Méthodologie

### Prétraitement des Données
1. **Chargement des Données** : Charger les données à partir des fichiers CSV et les étiqueter correctement comme "FAKE" ou "REAL".
2. **Prétraitement du Texte** : Nettoyer les données textuelles dans la colonne `title` et les convertir en minuscules.
3. **Tokenisation** : Tokeniser le texte en utilisant le `Tokenizer` de Keras pour convertir le texte en séquences d'entiers.
4. **Padding** : Appliquer le padding pour assurer que toutes les séquences ont la même longueur pour le traitement par LSTM.

### Développement du Modèle
1. **Architecture du Modèle** : Définir un modèle `Sequential` avec les couches suivantes :
   - Une couche `Embedding` pour convertir les séquences d'entiers en vecteurs denses.
   - Une couche `LSTM` pour apprendre à partir des données de séquence.
   - Une couche `Dense` avec une fonction d'activation `sigmoid` pour la classification binaire.
2. **Compilation** : Compiler le modèle avec `binary_crossentropy` comme fonction de perte et l'optimiseur `Adam`.

### Entraînement
Entraîner le modèle sur les données textuelles prétraitées, en utilisant une partie des données pour la validation.

### Évaluation
Évaluer la performance du modèle sur un ensemble de test séparé et rapporter la précision et la perte.

### Tests
Utiliser le modèle formé pour faire des prédictions sur de nouvelles données inédites et fournir la sortie de classification.

## Utilisation
Pour exécuter le projet, vous devez exécuter le script Python qui comprend toutes les étapes, du prétraitement des données à l'entraînement et à l'évaluation du modèle. Le script contiendra également un exemple de la manière d'utiliser le modèle pour classifier de nouveaux articles.

## Dépendances
- Python 3
- TensorFlow
- Keras
- Pandas
- Scikit-learn

## Comment Exécuter
Assurez-vous d'avoir toutes les dépendances nécessaires installées. Mettez à jour les chemins dans le script pour pointer vers vos fichiers CSV et exécutez le script pour entraîner le modèle et faire des prédictions.

## Remarque
Le modèle actuel est un LSTM de base. Pour une précision améliorée, envisagez d'enrichir les données d'entraînement, d'expérimenter avec des modèles plus complexes, ou d'utiliser des modèles de langue pré-entraînés pour l'extraction de caractéristiques.

---

Pour des instructions plus détaillées, référez-vous aux commentaires dans le script lui-même, qui expliquent chaque étape et fonction dans le code.
