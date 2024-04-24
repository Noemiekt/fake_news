import csv
from collections import defaultdict

# Ouvrir le fichier CSV des utilisateurs en lecture
with open('../utilisateurs.csv', 'r', encoding='utf-8') as csv_file:
    reader_user = csv.DictReader(csv_file)
    
    user_data = defaultdict(lambda: {'user_id':0, 'username':"", 'followers':[], 'posts':"", 'followers_count':0, 'followed_influencers_count':0})

    # Parcourir les lignes du CSV des utilisateurs
    for row in reader_user:
        user_id = row['ID']
        username = row['username']
        followers = row['Followers_list'].split(',')
        post = row['post_list']
        followers_count = len(followers)

        user_data[user_id]['user_id'] = user_id
        user_data[user_id]['username'] = username
        user_data[user_id]['followers'] = followers
        user_data[user_id]['posts'] = post

# Ouvrir le fichier CSV des posts en lecture
with open('posts.csv', 'r', encoding='utf-8') as csv_file:
    reader = csv.DictReader(csv_file)
    
    # Créer un dictionnaire pour stocker les informations agrégées
    aggregated_data = defaultdict(lambda: {'followers_total': 0, 'post': '', 'post_count': 0, 'media_exist': 0})
    
    # Ensemble pour stocker les noms d'utilisateur déjà rencontrés
    usernames_encountered = set()

    # Parcourir les lignes du CSV des posts
    for row in reader:
        username = row['Channel Name']
        aggregated_data[username]['post_count'] += 1
        post = row['ID']
        aggregated_data[username]['post'] += f'{post},'
        
        # Vérifier si le nom d'utilisateur a déjà été rencontré
        if username not in usernames_encountered:
            followers_list = row['Followers_list'].split(',')
            followers_count = len(followers_list)
            post_content = row['Post content']
            media_exist = int(row['Media_exists'])
            
            # Mettre à jour les valeurs agrégées pour le nom d'utilisateur
            aggregated_data[username]['followers_total'] += followers_count
            aggregated_data[username]['post_content'] = post_content
            aggregated_data[username]['media_exist'] += media_exist
            
            # Ajouter le nom d'utilisateur à l'ensemble des noms déjà rencontrés
            usernames_encountered.add(username)

# Écrire les données agrégées dans un nouveau fichier CSV pour les influenceurs
with open('influenceurs.csv', 'w', newline='', encoding='utf-8') as new_csv_file:
    fieldnames = ['influencer_id', 'username', 'followers', 'posts', 'posts_count', 'is_verified']
    writer = csv.DictWriter(new_csv_file, fieldnames=fieldnames)
    writer.writeheader()
    
    # Écrire les données agrégées dans le nouveau fichier CSV pour les influenceurs
    for id, (username, data) in enumerate(aggregated_data.items(), 1):
        writer.writerow({
            'influencer_id': id,  
            'username': username,
            'followers': data['followers_total'],
            'posts': data['post'],
            'posts_count': data['post_count'],
            'is_verified': data['media_exist']
        })

# Écrire les données des utilisateurs dans un nouveau fichier CSV
with open('users.csv', 'w', newline='', encoding='utf-8') as new_csv_file:
    fieldnames = ['user_id', 'username', 'followers', 'posts', 'followers_count', 'followed_influencers_count']
    writer = csv.DictWriter(new_csv_file, fieldnames=fieldnames)
    writer.writeheader()
    
    # Écrire les données agrégées dans le nouveau fichier CSV pour les utilisateurs
    for user_id, data in user_data.items():
        writer.writerow({
            'user_id': data['user_id'],  
            'username': data['username'],
            'followers': data['followers'],
            'posts': data['posts'],
            'followers_count': data['followers_count'],
            'followed_influencers_count': data['followed_influencers_count']
        })
