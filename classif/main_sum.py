import csv

def sum_account_classification(file1_path, file2_path, output_file):
    # Dictionnaire pour stocker les données de final_predictions_fake_bot.csv
    fake_bot_data = {}
    # Dictionnaire pour stocker les données de final_predictions_top_insta.csv
    top_insta_data = {}

    # Lire les données de final_predictions_fake_bot.csv
    with open(file1_path, 'r', newline='') as csvfile1:
        reader1 = csv.DictReader(csvfile1)
        for row in reader1:
            influencer_id = row['influencer_id']
            account_type = int(row['Account type'])
            fake_bot_data.setdefault(influencer_id, []).append(account_type)

    # Lire les données de final_predictions_top_insta.csv
    with open(file2_path, 'r', newline='') as csvfile2:
        reader2 = csv.DictReader(csvfile2)
        for row in reader2:
            influencer_id = row['influencer_id']
            top_insta_data[influencer_id] = row


    # Calculer la somme de Account type et Classification pour chaque utilisateur
    result = {}
    for influencer_id, account_types in fake_bot_data.items():
        if influencer_id in top_insta_data:
            classifications = int(top_insta_data[influencer_id]['Classification'])
            total = sum(account_types) + classifications
            result[influencer_id] = total

    # Écrire les résultats dans un nouveau fichier CSV
    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = ['influencer_id','post_content', 'username', 'followers_count', 'likes_count', 'shares_count', 'comments_count', 'view_count', 'engagement_rate', 'posts_count', 'is_verified', 'Followings','sentiment','followings','total']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for influencer_id, total in result.items():
            writer.writerow({
                'influencer_id': influencer_id,
                'username': top_insta_data[influencer_id]['username'],
                'post_content': top_insta_data[influencer_id]['post_content'],
                'followers_count': top_insta_data[influencer_id]['followers_count'],
                'likes_count': top_insta_data[influencer_id]['likes_count'],
                'shares_count': top_insta_data[influencer_id]['shares_count'],
                'comments_count': top_insta_data[influencer_id]['comments_count'],
                'view_count': top_insta_data[influencer_id]['view_count'],
                'engagement_rate': top_insta_data[influencer_id]['engagement_rate'],
                'posts_count': top_insta_data[influencer_id]['posts_count'],
                'is_verified': top_insta_data[influencer_id]['is_verified'],
                'followings': top_insta_data[influencer_id]['followings'],
                'sentiment': top_insta_data[influencer_id]['sentiment'],
                'total': total
            })


# Appeler la fonction avec les chemins des fichiers CSV et le nom du fichier de sortie
sum_account_classification('final_predictions_fake_bot.csv', 'final_predictions_top_insta.csv', 'final_prediction_total.csv')
