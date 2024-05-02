import json
import pandas as pd

# Chemin vers le fichier JSON
file_path = './influenceur.json'

# Charger les données JSON
with open(file_path, 'r') as file:
    data = json.load(file)

# Préparer une liste pour stocker les données calculées
influencers_metrics = []

# Itérer sur chaque influenceur dans le fichier JSON
for influencer in data:
    posts = influencer['posts']
    followers_count = int(influencer['followers_count'])
    
    # Vérifier si 'post_count_week' est présent, sinon utiliser la longueur des posts
    post_count_week = int(influencer.get('post_count_week', len(posts)))

    # Variables pour calculer la moyenne de l'engagement rate des 10 derniers posts
    engagement_rates = []

    # Compter les fausses nouvelles
    fake_news_count = sum(1 for post in posts if post['is_a_fake_news'] == "1")

    # Itérer sur chaque post de l'influenceur
    for post in posts:
        likes = int(post['likes_count'])
        shares = int(post['shares_count'])
        comments = int(post['comments_count'])
        
        # Calculer l'engagement rate pour le post actuel
        if followers_count > 0:  # Éviter la division par zéro
            engagement_rate_post = ((likes + shares + comments) / followers_count) * 100
        else:
            engagement_rate_post = 0
        
        # Ajouter le taux d'engagement de ce post à la liste
        engagement_rates.append(engagement_rate_post)

    # Calculer le taux de crédibilité
    if len(posts) > 0:
        credibility_rate = (1 - (fake_news_count / len(posts)))
    else:
        credibility_rate = 1  # Si aucun post, supposons que la crédibilité est maximale

    # Calculer l'engagement rate global pour les 10 derniers posts
    if engagement_rates:
        engagement_rate_global = sum(engagement_rates[-10:]) / min(10, len(engagement_rates))
    else:
        engagement_rate_global = 0

    # Enregistrer les métriques pour l'influenceur actuel
    influencers_metrics.append({
        "influencer_id": influencer['influencer_id'],
        "username": influencer['username'],
        "followers_count": followers_count,
        "post_count_week": post_count_week,
        "activity_rate_weekly": (post_count_week / 14), # 14 est la norme pour 2 posts par jour
        "credibility_rate": credibility_rate,
        "engagement_rate_global": engagement_rate_global
    })

# Créer un DataFrame à partir des résultats
df_influencers = pd.DataFrame(influencers_metrics)

# Trouver le plus grand nombre de followers dans le DataFrame
max_followers = df_influencers['followers_count'].max()

# Normaliser les followers à une échelle de 0 à 1000
df_influencers['followers_count_normalized_to_1000'] = (df_influencers['followers_count'] / max_followers) * 1000

# Prendre uniquement la partie entière des valeurs normalisées
df_influencers['followers_count_normalized_to_1000'] = df_influencers['followers_count_normalized_to_1000'].apply(int)

# Chemin de sortie pour le fichier CSV
output_csv_path = './metrics.csv'  # Remplacez par le chemin où vous souhaitez sauvegarder le fichier CSV

# Sauvegarder le DataFrame dans un fichier CSV
df_influencers.to_csv(output_csv_path, index=False)

# Afficher le DataFrame pour vérification
print(df_influencers)