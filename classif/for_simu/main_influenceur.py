import csv
import os
from collections import defaultdict

# Ouvrir le fichier CSV des prédictions finales des meilleurs influenceurs en lecture
with open('../final_prediction_total.csv', 'r', encoding='utf-8') as influencer_csv:
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