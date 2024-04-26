# import csv
# import json

# # Fonction pour lire un fichier CSV et le convertir en format JSON
# def csv_to_json(csv_file, json_file):
#     data = []
#     # Ouvrir le fichier CSV et lire les données
#     with open(csv_file, 'r') as csvfile:
#         csvreader = csv.DictReader(csvfile)
#         # Convertir chaque ligne en un dictionnaire et l'ajouter à la liste
#         for row in csvreader:
#             data.append(row)
    
#     # Écrire les données au format JSON dans un fichier
#     with open(json_file, 'w') as jsonfile:
#         jsonfile.write(json.dumps(data, indent=4))

# # Convertir influenceur.csv en influenceur.json
# csv_to_json('influenceurs.csv', 'influenceur.json')

# # Convertir post.csv en post.json
# csv_to_json('post.csv', 'post.json')

# import csv
# import json

# # Fonction pour lire un fichier CSV et le convertir en format JSON
# def csv_to_json(csv_file):
#     data = []
#     # Ouvrir le fichier CSV et lire les données
#     with open(csv_file, 'r') as csvfile:
#         csvreader = csv.DictReader(csvfile)
#         # Convertir chaque ligne en un dictionnaire et l'ajouter à la liste
#         for row in csvreader:
#             data.append(row)
#     return data

# # Charger les données des fichiers CSV
# influenceurs = csv_to_json('influenceurs.csv')
# posts = csv_to_json('post.csv')

# # Créer un dictionnaire pour stocker les posts par username
# posts_by_username = {post['username']: post for post in posts}

# # Associer les posts aux influenceurs correspondants
# for influenceur in influenceurs:
#     username = influenceur['username']
#     if username in posts_by_username:
#         influenceur['posts'] = [posts_by_username[username]]

# # Écrire les données combinées dans un fichier JSON
# with open('combined_data.json', 'w') as jsonfile:
#     jsonfile.write(json.dumps(influenceurs, indent=4))

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

# Écrire les données combinées dans un fichier JSON
with open('combined_data.json', 'w') as jsonfile:
    jsonfile.write(json.dumps(influenceurs, indent=4))


