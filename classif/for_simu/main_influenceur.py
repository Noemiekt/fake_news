import csv
import os
from collections import defaultdict

# Ouvrir le fichier CSV des prédictions finales des meilleurs influenceurs en lecture
with open('../final_predictions_top_insta.csv', 'r', encoding='utf-8') as influencer_csv:
    reader_influencer = csv.DictReader(influencer_csv)

    # Créer un dictionnaire pour stocker les données des influenceurs
    influencer_data = defaultdict(lambda: {'username':"", 'followers_count':0, 'post_count':0, 'is_verified':0})
    
    # Parcourir les lignes du CSV des prédictions finales des meilleurs influenceurs
    for row in reader_influencer:
        influencer_username = row['username']
        influencer_followers_count = int(row['followers_count'])
        influencer_post_count = int(row['posts_count'])
        influencer_is_verified = int(row['is_verified'])
        
        influencer_data[influencer_username]['username'] = influencer_username
        influencer_data[influencer_username]['followers_count'] = influencer_followers_count
        influencer_data[influencer_username]['post_count'] = influencer_post_count
        influencer_data[influencer_username]['is_verified'] = influencer_is_verified
        
        # Récupérer les followers depuis le fichier dans influenceur_follower
        followers_filename = f'influenceurs_followers/{influencer_username}.csv'
        if os.path.exists(followers_filename):
            with open(followers_filename, 'r', encoding='utf-8') as followers_csv:
                follower_reader = csv.reader(followers_csv)
                next(follower_reader) 
                followers_list = [follower[1] for follower in follower_reader]
                
                influencer_data[influencer_username]['followers'] = followers_list
                
                

#  Écrire les données des influenceurs dans un nouveau fichier CSV
with open('influenceurs.csv', 'w', newline='', encoding='utf-8') as new_csv_file:
    fieldnames = ['influencer_id', 'username', 'followers_count', 'post_count', 'is_verified', 'followers']
    writer = csv.DictWriter(new_csv_file, fieldnames=fieldnames)
    writer.writeheader()
    
    # Écrire les données des influenceurs dans le nouveau fichier CSV
    for id, (_, data) in enumerate(influencer_data.items(), 1):
        writer.writerow({
            'influencer_id': id,  
            'username': data['username'],
            'followers_count': data['followers_count'],
            'post_count': data['post_count'],
            'is_verified': data['is_verified'],
            'followers': ','.join(data.get('followers', [])).split(','),
        })
# # Ouvrir le fichier CSV des utilisateurs en lecture
# with open('../utilisateurs.csv', 'r', encoding='utf-8') as csv_file:
#     reader_user = csv.DictReader(csv_file)
    
#     user_data = defaultdict(lambda: {'user_id':0, 'username':"", 'followers':[], 'posts':"", 'followers_count':0, 'followed_influencers_count':0})

#     # Parcourir les lignes du CSV des utilisateurs
#     for row in reader_user:
#         user_id = row['ID']
#         username = row['username']
#         followers = row['Followers_list'].split(',')
#         post = row['post_list']
#         followers_count = len(followers)

#         user_data[user_id]['user_id'] = user_id
#         user_data[user_id]['username'] = username
#         user_data[user_id]['followers'] = followers
#         user_data[user_id]['posts'] = post

# # Ouvrir le fichier CSV des posts en lecture
# with open('posts.csv', 'r', encoding='utf-8') as csv_file:
#     reader = csv.DictReader(csv_file)
    
#     # Créer un dictionnaire pour stocker les informations agrégées
#     aggregated_data = defaultdict(lambda: {'followers_total': 0, 'post': '', 'post_count': 0, 'media_exist': 0})
    
#     # Ensemble pour stocker les noms d'utilisateur déjà rencontrés
#     usernames_encountered = set()

#     # Parcourir les lignes du CSV des posts
#     for row in reader:
#         username = row['Channel Name']
#         aggregated_data[username]['post_count'] += 1
#         post = row['ID']
#         aggregated_data[username]['post'] += f'{post},'
        
#         # Vérifier si le nom d'utilisateur a déjà été rencontré
#         if username not in usernames_encountered:
#             followers_list = row['Followers_list'].split(',')
#             followers_count = len(followers_list)
#             post_content = row['Post content']
#             media_exist = int(row['Media_exists'])
            
#             # Mettre à jour les valeurs agrégées pour le nom d'utilisateur
#             aggregated_data[username]['followers_total'] += followers_count
#             aggregated_data[username]['post_content'] = post_content
#             aggregated_data[username]['media_exist'] += media_exist
            
#             # Ajouter le nom d'utilisateur à l'ensemble des noms déjà rencontrés
#             usernames_encountered.add(username)

# # Écrire les données agrégées dans un nouveau fichier CSV pour les influenceurs
# with open('influenceurs.csv', 'w', newline='', encoding='utf-8') as new_csv_file:
#     fieldnames = ['influencer_id', 'username', 'followers', 'followers_count', 'posts', 'posts_count', 'is_verified', 'is_a_fake_news']
#     writer = csv.DictWriter(new_csv_file, fieldnames=fieldnames)
#     writer.writeheader()
    
#     # Écrire les données agrégées dans le nouveau fichier CSV pour les influenceurs
#     for id, (username, data) in enumerate(aggregated_data.items(), 1):
#         writer.writerow({
#             'influencer_id': id,  
#             'username': username,
#             'followers': data['followers_total'],
#             'posts': data['post'],
#             'posts_count': data['post_count'],
#             'is_verified': data['media_exist']
#         })

# # Écrire les données des utilisateurs dans un nouveau fichier CSV
# with open('users.csv', 'w', newline='', encoding='utf-8') as new_csv_file:
#     fieldnames = ['user_id', 'username', 'followers', 'posts', 'followers_count', 'followed_influencers_count']
#     writer = csv.DictWriter(new_csv_file, fieldnames=fieldnames)
#     writer.writeheader()
    
#     # Écrire les données agrégées dans le nouveau fichier CSV pour les utilisateurs
#     for user_id, data in user_data.items():
#         writer.writerow({
#             'user_id': data['user_id'],  
#             'username': data['username'],
#             'followers': data['followers'],
#             'posts': data['posts'],
#             'followers_count': data['followers_count'],
#             'followed_influencers_count': data['followed_influencers_count']
#         })
