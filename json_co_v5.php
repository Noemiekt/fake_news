<?php
header('Content-Type: application/json');

// Configuration initiale
$totalInfluencers = 5; // Nombre fixe d'influenceurs
$totalStudents = isset($_GET['s']) ? (int)$_GET['s'] : 20;
$totalUsers = $totalInfluencers + $totalStudents;

$influencers = [];
$students = [];
$posts = [];
$nb_students = $totalStudents;

// Création des influenceurs avec leurs caractéristiques
for ($i = 1; $i <= $totalInfluencers; $i++) {
    $influencers[] = [
        'influencer_id' => $i,
        'username' => 'influencer' . $i,
        'credibility' => rand(1, 10), // Valeurs exemple, ajustez selon vos besoins
        'activity_rate' => rand(1, 10),
        'reliability' => rand(1, 10),
        'verified' => (bool)rand(0, 1),
        'interaction' => rand(1, 10),
        'followers' => [],
    ];
}

// Création des étudiants
for ($s = 1; $s <= $totalStudents; $s++) {
    $students[] = [
        'student_id' => $s,
        'username' => 'student' . $s,
        'followers' => [],
    ];
}

// Assignation des followers (étudiants) aux influenceurs
foreach ($influencers as $influencerKey => &$influencer) {
    $followingsCount = rand(0, $totalStudents);
    $influencer['followers_count'] = $followingsCount;
    $followings = [];
    
    $studentIds = range(0, $totalStudents - 1);
    shuffle($studentIds);

    foreach ($studentIds as $id) {
        if (count($followings) >= $followingsCount) {
            break;
        }

        if (!in_array($id, $followings)) {
            $followings[] = $id;
            $studentUsername = $students[$id]['username'];
            $influencer['followers'][] = ['username' => $studentUsername];
        }
    }
}
unset($influencer);

// Gestion des connections entre students
foreach ($students as &$student) {
    $followingsCount = rand(0, $totalStudents - 1);
    $student['followers_count'] = $followingsCount;
    $followings = [];

    while (count($followings) < $followingsCount) {
        $randomUserKey = rand(0, $totalStudents - 1);

        if (!in_array($randomUserKey, $followings) && $randomUserKey != $student['student_id'] - 1) {
            $followings[] = $randomUserKey;
            $student['followers'][] = $students[$randomUserKey]['username'];
        }
    }
}
unset($student);

// Création des publications et des partages de manière aléatoire pour chaque influenceur
foreach ($influencers as $influencer) {
    $postsCount = rand(1, 2); // Nombre de posts aléatoire pour chaque influenceur

    for ($j = 0; $j < $postsCount; $j++) {
        $postId = count($posts) + 1;
        $post = [
            'post_id' => $postId,
            'influencer_id' => $influencer['influencer_id'],
            'is_fake_news' => true,
            'shares' => [],
            'likes' => [],
        ];

        // Initialiser $receivedFakeNews[$postId] comme un tableau vide
        if (!isset($receivedFakeNews[$postId])) {
            $receivedFakeNews[$postId] = [];
        }

        // Sélection aléatoire des étudiants partageurs
        $sharingStudents = array_rand($students, rand(1, count($students) / 2));
        if (!is_array($sharingStudents)) {
            $sharingStudents = [$sharingStudents];
        }

        foreach ($sharingStudents as $sharingStudentKey) {
            $student = $students[$sharingStudentKey];

            // Choix aléatoire des destinataires
            $recipientKeys = array_rand($students, rand(1, count($students) / 2));
            if (!is_array($recipientKeys)) {
                $recipientKeys = [$recipientKeys];
            }

            $share = [
                'username' => $student['username'],
                'user_id' => $student['student_id'],
                'to' => [],
            ];

            foreach ($recipientKeys as $recipientKey) {
                if (!in_array($students[$recipientKey]['username'], $receivedFakeNews[$postId])) {
                    $share['to'][] = ['username' => $students[$recipientKey]['username']];
                    // Ajouter le destinataire à la liste des étudiants ayant reçu la fausse nouvelle
                    $receivedFakeNews[$postId][] = $students[$recipientKey]['username'];
                }
            }

            if (!empty($share['to'])) {
                $post['shares'][] = $share;
            }
        }

        $post['shares_count'] = count($post['shares']);

        // Génération aléatoire des likes
        $likedByKeys = array_rand($students, rand(1, count($students)));
        if (!is_array($likedByKeys)) {
            $likedByKeys = [$likedByKeys];
        }

        foreach ($likedByKeys as $likedByKey) {
            $like = [
                'username' => $students[$likedByKey]['username'],
                'user_id' => $students[$likedByKey]['student_id'],
            ];
            $post['likes'][] = $like;
        }

        $post['likes_count'] = count($post['likes']);

        $posts[] = $post;
    }
}



// Calcul de la probabilité de persuasion et de corruption ici...
foreach ($influencers as &$influencer) {
    // Calcul simple pour la probabilité de persuasion en fonction des attributs
    $influencer['proba_persu'] = (
        $influencer['credibility'] +
        $influencer['activity_rate'] +
        $influencer['reliability'] +
        ($influencer['verified'] ? 1 : 0) + // Supposons que vérifié ajoute +1 à la proba
        $influencer['interaction']
    ) / 5; // Division par le nombre d'attributs pour faire une moyenne
}

// Pour la probabilité de corruption, nous pourrions compter le nombre total de partages
$totalShares = 0;
foreach ($posts as $post) {
    $totalShares += count($post['shares']);
    // $totalShares += max(1, count($post['shares']));
}

// Calcul de la probabilité de corruption pour chaque influenceur
foreach ($influencers as &$influencer) {
    // Supposons que chaque partage augmente la probabilité de corruption
    $influencer['proba_corrupt'] = count($influencer['followers']) / $totalShares;

//     $influencer['proba_corrupt'] = $totalShares > 0 ? count($influencer['followers']) / $totalShares : 0;
}

$data = [
    'students' => $students,
    'influencers' => $influencers,
    'posts' => $posts,
];

$jsonData = json_encode($data, JSON_PRETTY_PRINT);
echo $jsonData;

$filePath = './json_co_v5.json';
file_put_contents($filePath, $jsonData);
?>
