import csv

# Chemin du fichier source
source_file = '../final_predictions_top_insta.csv'

# Chemin du fichier de destination
destination_file = 'post.csv'

# Colonnes à extraire du fichier source
columns_to_extract = ['username', 'likes_count', 'shares_count', 'comments_count', 'Classification']

# Lire le fichier source et écrire les données dans le fichier de destination
with open(source_file, 'r', encoding='utf-8') as source_csv, \
        open(destination_file, 'w', newline='', encoding='utf-8') as destination_csv:
    reader = csv.DictReader(source_csv)
    # Définir les noms de colonnes dans le fichier de destination
    fieldnames = ['username', 'likes_count', 'shares_count', 'comments_count', 'is_a_fake_news']
    writer = csv.DictWriter(destination_csv, fieldnames=fieldnames)
    writer.writeheader()

    for row in reader:
        # Créer un dictionnaire contenant uniquement les colonnes spécifiées
        filtered_row = {key: row[key] for key in columns_to_extract}
        # Renommer la colonne is_a_fake_news en classif
        filtered_row['is_a_fake_news'] = 1 - int(filtered_row.pop('Classification'))
        writer.writerow(filtered_row)