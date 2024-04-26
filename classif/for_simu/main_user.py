import csv
import os

# Dossier contenant les fichiers CSV des influenceurs et leurs followers
folder_path = 'influenceurs_followers'

# Chemin du fichier de destination
destination_file = 'users.csv'

# Colonnes à extraire des fichiers source
columns_to_extract = ['ID de l\'utilisateur', 'Nom d\'utilisateur', 'followed_influenceur']

# Lire tous les fichiers CSV du dossier et écrire les données dans le fichier de destination
with open(destination_file, 'w', newline='', encoding='utf-8') as destination_csv:
    writer = csv.writer(destination_csv)
    # Écrire l'en-tête du fichier de destination
    writer.writerow(columns_to_extract + ['followed_influenceur_count'])

    # Parcourir tous les fichiers CSV dans le dossier
    for filename in os.listdir(folder_path):
        if filename.endswith('.csv'):
            source_file = os.path.join(folder_path, filename)
            with open(source_file, 'r', encoding='utf-8') as source_csv:
                reader = csv.DictReader(source_csv)
                
                for row in reader:
                    # Extraire les colonnes spécifiées
                    user_id = row['ID de l\'utilisateur']
                    username = row['Nom d\'utilisateur']
                    followed_influenceurs = row['followed_influenceur'].split(',')  # Convertir en liste
                    followed_influenceurs_count = len(followed_influenceurs)  # Calculer le nombre d'influenceurs suivis
                    # Écrire la ligne dans le fichier de destination avec followed_influenceur_count
                    writer.writerow([user_id, username, followed_influenceurs, followed_influenceurs_count])
