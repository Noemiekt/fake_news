<?php
header('Content-Type: application/json');
ini_set('memory_limit', '1024M');  // Augmente la limite de mémoire à 256MB


$totalInfluencers = isset($_GET['i']) ? (int)$_GET['i'] : 3;
$totalUsers = isset($_GET['u']) ? (int)$_GET['u'] : 200; 


define('MAX_POSTS', 20);  // Définir une constante pour le nombre maximal de posts.

function generateRandomPosts($influencerId, $followersCount) {
    $posts = [];
    $totalPosts = rand(10, MAX_POSTS);  // Utilisation de la constante MAX_POSTS

    for ($i = 1; $i <= $totalPosts; $i++) {
        // Assurez-vous que le nombre de partages et de likes ne dépasse pas le nombre de followers
        $sharesCount = rand(1, $followersCount);
        $likesCount = rand(1, $followersCount);

        // Sélectionner aléatoirement les utilisateurs pour les partages et les likes
        $allUserIds = range(1, $followersCount);
        shuffle($allUserIds);

        $sharedUserIds = array_slice($allUserIds, 0, $sharesCount);
        $likedUserIds = array_slice($allUserIds, 0, $likesCount);

        $posts[] = [
            'post_id' => $i,
            'influencer_id' => $influencerId,
            'shares' => array_map(function($userId) { return ['username' => "user$userId"]; }, $sharedUserIds),
            'likes' => array_map(function($userId) { return ['username' => "user$userId"]; }, $likedUserIds),
            'shares_count' => $sharesCount,
            'likes_count' => $likesCount,
        ];
    }

    return $posts;
}

// Définissez les IDs des influenceurs vérifiés
$verifiedInfluencers = [1, 3, 5]; // Supposons que les influenceurs avec ces IDs sont vérifiés


$influencers = [];
for ($i = 1; $i <= $totalInfluencers; $i++) {
    $followersCount = rand(1, $totalUsers);
    $posts = generateRandomPosts($i, $followersCount);

    // Vérifie si l'influenceur actuel est vérifié
    $isVerified = in_array($i, $verifiedInfluencers) ? 1 : 0;

    $credibilityRate = $followersCount ? array_sum(array_column($posts, 'likes_count')) / $followersCount : 0;
    $activityRate = count($posts) / MAX_POSTS;  // Utiliser la constante MAX_POSTS ici

    // Générer un tableau de tous les ID d'utilisateurs possibles
    $allUserIds = range(1, $totalUsers);
    shuffle($allUserIds); // Mélanger le tableau pour obtenir un ordre aléatoire
    $selectedUserIds = array_slice($allUserIds, 0, $followersCount); // Sélectionner les followers

    // Créer la liste des followers
    $followers = array_map(function($userId) {
        return ['username' => "user$userId"];
    }, $selectedUserIds);

    // Pour chaque influenceur
    $totalInteractions = array_sum(array_map(function($post) {
        return $post['likes_count'] + $post['shares_count'];
    }, $posts));

    $maxPossibleInteractions = $followersCount * count($posts) * 2;  // Chaque follower peut liker et partager chaque post

    $credibilityRate = $maxPossibleInteractions ? $totalInteractions / $maxPossibleInteractions : 0;

    // Définissez les poids pour chaque facteur
    $w1 = 0.4; // Poids pour le taux de crédibilité
    $w2 = 0.3; // Poids pour le taux d'activité
    $w3 = 0.2; // Poids pour le nombre de followers
    $w4 = 0.1; // Poids pour le statut vérifié

    $followersNormalized = $followersCount / $totalUsers; // Normalisez le nombre de followers
    

    $probabilityTrueNews = $w1 * $credibilityRate + $w2 * $activityRate + $w3 * $followersNormalized + $w4 * $isVerified;  

    $influencers[] = [
        'influencer_id' => $i,
        'username' => "influencer$i",
        'followers' => $followers,
        'followers_count' => $followersCount,
        'posts' => $posts,
        'posts_count' => count($posts),
        'is_verified' => $isVerified,
        'credibility_rate' => $credibilityRate,
        'activity_rate' => $activityRate,
        'probability_true_news' => $probabilityTrueNews,
    ];
}

$users = [];
for ($i = 1; $i <= $totalUsers; $i++) {
    $followersCount = rand(1, $totalUsers/100);  // Nombre aléatoire de followers

    $userInfluencers = [];  // Influenceurs que cet utilisateur suit

    $followedInfluencers = [];

    $postLiked = [];  // Posts que cet utilisateur a aimés
    $postShared = [];  // Posts que cet utilisateur a partagés

    // Parcourir chaque influenceur pour voir si l'utilisateur actuel est un follower
    // et pour recueillir les posts aimés et partagés
    foreach ($influencers as $influencer) {
        foreach ($influencer['followers'] as $follower) {
            if ($follower['username'] === "user$i") {
                $followedInfluencers[] = $influencer['username'];
                break;
            }
        }

        // Parcourir les posts de l'influenceur
        foreach ($influencer['posts'] as $post) {
            // Vérifier si l'utilisateur a aimé le post
            foreach ($post['likes'] as $like) {
                if ($like['username'] === "user$i") {
                    $postLiked[] = $post['post_id'];
                    break;
                }
            }

            // Vérifier si l'utilisateur a partagé le post
            foreach ($post['shares'] as $share) {
                if ($share['username'] === "user$i") {
                    $postShared[] = $post['post_id'];
                    break;
                }
            }
        }
    }

    $liked_post_count = count($postLiked);
    $shared_post_count = count($postShared);

    


    // Générer un tableau de tous les ID d'utilisateurs possibles
    $allUserIds = range(1, $totalUsers);
    shuffle($allUserIds); // Mélanger le tableau pour obtenir un ordre aléatoire
    $selectedUserIds = array_slice($allUserIds, 0, $followersCount); // Sélectionner les followers

    // Créer la liste des followers
    $followers = array_map(function($userId) {
        return ['username' => "user$userId"];
    }, $selectedUserIds);

    // Calculez d'abord le nombre total de posts publiés par tous les influenceurs
    $totalPosts = array_sum(array_map(function($influencer) {
        return count($influencer['posts']);
    }, $influencers));

    // Pour chaque utilisateur
    $userInteractions = $shared_post_count + $liked_post_count;
    $maxPossibleInteractions = $totalPosts * 2;  // Chaque post peut être liké et partagé une fois

    $activityRate = $userInteractions / $maxPossibleInteractions;

    // Calculez la moyenne des probability_true_news des influenceurs suivis
    $averageProbabilityTrueNews = 0;
    if (count($followedInfluencers) > 0) {
        $totalProbability = 0;
        foreach ($followedInfluencers as $influencerUsername) {
            // Trouvez l'influenceur dans la liste $influencers par son nom d'utilisateur
            foreach ($influencers as $influencer) {
                if ($influencer['username'] === $influencerUsername) {
                    $totalProbability += $influencer['probability_true_news'];
                    break; // Arrêtez la recherche une fois l'influenceur trouvé
                }
            }
        }

        $averageProbabilityTrueNews = $totalProbability / count($followedInfluencers);
    }

    // Définir un seuil pour déterminer si l'utilisateur suit des comptes fiables
    $threshold = 0.5;  // Par exemple, si la moyenne est supérieure à 0.5, l'utilisateur suit des comptes fiables
    $followsReliableAccounts = $averageProbabilityTrueNews > $threshold ? 1 : 0;

    


    $users[] = [
        'user_id' => $i,
        'username' => "user$i",
        'followers' => $followers,
        'followers_count' => $followersCount,
        'followed_influencers_count' => count($followedInfluencers),  // Nombre d'influenceurs que l'utilisateur suit
        'userInfluencers' => $followedInfluencers,
        'activity_rate' => $activityRate,
        'follows_reliable_accounts' => $followsReliableAccounts,
    ];
}

$data = [
    'influencers' => $influencers,
    'users' => $users,
    'totalUsers' => $totalUsers,
    'totalInfluencers' => $totalInfluencers,
];

$jsonData = json_encode($data, JSON_PRETTY_PRINT);
echo $jsonData;

$filePath = './json_co_v6.json';
file_put_contents($filePath, $jsonData);
?>
