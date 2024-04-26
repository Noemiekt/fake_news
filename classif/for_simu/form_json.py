import csv
import json

# Fonction pour lire un fichier CSV et le convertir en format JSON
def csv_to_json(csv_file):
    data = []
    # Ouvrir le fichier CSV et lire les données
    with open(csv_file, 'r') as csvfile:
        csvreader = csv.DictReader(csvfile)
        # Convertir chaque ligne en un dictionnaire et l'ajouter à la liste
        for row in csvreader:
            data.append(row)
    return data

# Charger les données des fichiers CSV
influenceurs = csv_to_json('influenceurs.csv')
posts = csv_to_json('post.csv')
users = csv_to_json('users.csv')  # Charger les données des utilisateurs

# Créer un dictionnaire pour stocker les posts par username
posts_by_username = {}
for post in posts:
    username = post['username']
    if username not in posts_by_username:
        posts_by_username[username] = []
    posts_by_username[username].append(post)

# Associer les posts aux influenceurs correspondants
for influenceur in influenceurs:
    username = influenceur['username']
    if username in posts_by_username:
        influenceur['posts'] = []
        for idx, post in enumerate(posts_by_username[username], start=1):
            post['post_id'] = idx
            influenceur['posts'].append(post)

# Écrire les données combinées des influenceurs dans un fichier JSON
with open('influenceur.json', 'w') as jsonfile:
    jsonfile.write(json.dumps(influenceurs, indent=4))

# Écrire les données des utilisateurs dans un fichier JSON
with open('users.json', 'w') as jsonfile:
    jsonfile.write(json.dumps(users, indent=4))
