<?php
header('Content-Type: application/json');

// Nombre total d'utilisateurs
$totalUsers = 8;
$users = [];
$posts = [];

// Création des utilisateurs
for ($i = 1; $i <= $totalUsers; $i++) {
    $users[] = [
        'user_id' => $i,
        'username' => 'user'.$i,
        'followers' => [],
    ];
}

// Assignation aléatoire des followings
foreach ($users as &$user) {
    $followingsCount = rand(1, $totalUsers - 1);
    $followings = [];

    while (count($followings) < $followingsCount) {
        $randomUserKey = rand(0, $totalUsers - 1);

        if ($randomUserKey != $user['user_id'] - 1 && !in_array($randomUserKey, $followings)) {
            $followings[] = $randomUserKey;
            $users[$randomUserKey]['followers'][] = ['username' => $user['username']];
        }
    }

    $user['followers_count'] = count($user['followers']);
}

// Création des publications et des partages de manière aléatoire
foreach ($users as $user) {
    $postsCount = rand(1, 5); // Chaque utilisateur peut avoir entre 1 et 5 posts

    for ($j = 0; $j < $postsCount; $j++) {
        $postId = count($posts) + 1;
        $post = [
            'post_id' => $postId,
            'user_id' => $user['user_id'],
            'is_fake_news' => (bool)rand(0, 1),
            'shares' => [],
        ];

        // Génération aléatoire des partages pour chaque post
        $sharesCount = rand(0, $totalUsers - 1);
        for ($k = 0; $k < $sharesCount; $k++) {
            $sharingUserKey = rand(0, $totalUsers - 1);
            $sharedToUserCount = rand(1, $totalUsers - 1);
            $allUserKeys = range(0, $totalUsers - 1);
            $sharedToUserKeys = $sharedToUserCount > 1 ? array_rand($allUserKeys, $sharedToUserCount) : [(array_rand($allUserKeys))];

            // Création du partage
            $share = [
                'username' => $users[$sharingUserKey]['username'],
                'to' => [],
            ];

            foreach ($sharedToUserKeys as $key) {
                if ($key != $sharingUserKey) {
                    $share['to'][] = ['username' => $users[$key]['username']];
                }
            }

            // Ajout du partage au post si ce n'est pas vide
            if (!empty($share['to'])) {
                $post['shares'][] = $share;
            }
        }

        $post['shares_count'] = count($post['shares']);
        $posts[] = $post;
    }
}

// Aggrégation des données dans une structure unique
$data = [
    'users' => $users,
    'posts' => $posts,
];

// Génération du JSON
$jsonData = json_encode($data, JSON_PRETTY_PRINT);

// Affichage du JSON 
echo $jsonData;

// Chemin du fichier où vous souhaitez enregistrer le JSON
$filePath = './json_co_v2.json';

// Écriture du JSON dans le fichier
file_put_contents($filePath, $jsonData);
?>

