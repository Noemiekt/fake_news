import csv

# Chemin du fichier CSV d'origine
input_file = 'demotivateur.csv'
# Chemin du fichier CSV de sortie sans doublons
output_file = 'output.csv'

# Ouvrir le fichier CSV en lecture
with open(input_file, mode='r', encoding='utf-8') as infile, \
     open(output_file, mode='w', encoding='utf-8', newline='') as outfile:
    reader = csv.DictReader(infile)
    fields = reader.fieldnames
    writer = csv.DictWriter(outfile, fieldnames=fields)
    
    # Écrire l'en-tête dans le fichier de sortie
    writer.writeheader()
    
    # Ensemble pour garder trace des noms d'utilisateur déjà vus
    seen_users = set()
    
    # Lire chaque ligne du fichier d'entrée
    for row in reader:
        user = row['Nom d\'utilisateur']
        # Ajouter la ligne au fichier de sortie si le nom d'utilisateur n'a pas été vu auparavant
        if user not in seen_users:
            writer.writerow(row)
            seen_users.add(user)
