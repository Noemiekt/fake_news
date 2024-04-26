import csv

# Chemin du fichier CSV d'origine
input_file = 'output.csv'
# Chemin du fichier CSV de sortie sans certaines colonnes et avec une nouvelle colonne
output_file = 'hugodecrypte.csv'

# Ouvrir le fichier CSV en lecture
with open(input_file, mode='r', encoding='utf-8') as infile, \
     open(output_file, mode='w', encoding='utf-8', newline='') as outfile:
    reader = csv.DictReader(infile)
    
    # Liste des colonnes à supprimer
    columns_to_remove = ['Suivez-vous', 'Est vérifié', 'Page d\'accueil de l\'utilisateur', 'URL de l\'avatar']
    
    # Créer une nouvelle liste des champs, excluant les colonnes à enlever et ajouter la nouvelle colonne
    fields = [field for field in reader.fieldnames if field not in columns_to_remove] + ['followed_influenceur']
    
    writer = csv.DictWriter(outfile, fieldnames=fields)
    
    # Écrire l'en-tête dans le fichier de sortie
    writer.writeheader()

    # Lire chaque ligne du fichier d'entrée
    for row in reader:
        # Supprimer les colonnes spécifiées
        for column in columns_to_remove:
            row.pop(column, None)
        
        # Ajouter la nouvelle colonne avec la valeur 'hugodecrypte'
        row['followed_influenceur'] = 'hugodecrypte'
        
        # Écrire la ligne modifiée dans le fichier de sortie
        writer.writerow(row)
