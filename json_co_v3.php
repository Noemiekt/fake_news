<?php
header('Content-Type: application/json');



// Récupération du nombre d'utilisateurs à partir du paramètre 'n' dans l'URL
$totalInstructors = isset($_GET['i']) ? (int)$_GET['i'] : 20;
$totalStudents = isset($_GET['s']) ? (int)$_GET['s'] : 20; 
$totalUsers = $totalInstructors + $totalStudents;

$instructors = [];
$students = [];
$posts = [];
$nb_students = $totalStudents;
$inst_stud_co = [];
$stud_stud_co = [];
$proba_persu = [];
$proba_corrupt = [];

// Création des Instructeurs
for ($i = 1; $i <=$totalInstructors; $i++) {
    
    $instructors[] = [
        'instructors_id' => $i,
        'username' => 'instructor'.$i,
        'followers' => [],
    ];
}

// Création des Students
for ($s = 1; $s <=$totalStudents; $s++) {
    
    $students[] = [
        'students_id' => $s,
        'username' => 'student'.$s,
        'followers' => [],
    ];
}

// Assignation aléatoire des followings de students a instructors

foreach ($instructors as $instructorKey => &$instructor) {
    $followingsCount = rand(0, $totalStudents);
    $instructor['followers_count'] = $followingsCount;
    $followings = [];

    
    $studentIds = range(0, $totalStudents-1);
    shuffle($studentIds); 

    foreach ($studentIds as $id) {
        if (count($followings) >= $followingsCount) {
            break; 
        }

        if (!in_array($id, $followings)) {
            $followings[] = $id;
            $studentUsername = $students[$id]['username'];
            $instructors[$instructorKey]['followers'][] = ['username' => $studentUsername];
        }
    }
}
unset($instructor); 


// Assignation aléatoire des followings de students a students

foreach ($students as &$student) {
    $followingsCounts = rand(floor($totalStudents/3), $totalStudents - 1);
    $student['followers_count'] = $followingsCounts ;
    $followingss = [];

    while (count($followingss) < $followingsCounts) {
        $randomUserKeys = rand(0, $totalStudents - 1);

        if ($randomUserKeys != $student['students_id'] - 1 && !in_array($randomUserKeys, $followingss)) {
            $followingss[] = $randomUserKeys;
            $students[$randomUserKeys]['followers'][] = ['username' => $student['username']];
        }
    }

}
unset($student);



// Création des publications et des partages de manière aléatoire
foreach ($instructors as $instructor) {
    foreach ($students as &$student) {
        $postsCount = rand(1, 2); // Nombre de post random

        for ($j = 0; $j < $postsCount; $j++) {
            $postId = count($posts) + 1;
            $post = [
                'post_id' => $postId,
                'instructors_id' => $instructor['instructors_id'],
                'is_fake_news' => (bool)rand(0, 1),
                'shares' => [],
                'likes' => [],
            ];

            // Génération aléatoire des partages pour chaque post

            $usersShared = [];
            $sharesCount = rand(0, $totalInstructors - 1);

            for ($k = 0; $k <= $sharesCount; $k++) {

                $sharingUserKey = rand(0, $totalStudents - 1);
                $sharedToUserCount = rand(1, $totalStudents - 1);
                $allUserKeys = range(0, $totalStudents - 1);
                $sharedToUserKeys = $sharedToUserCount > 1 ? array_rand($allUserKeys, $sharedToUserCount) : [(array_rand($allUserKeys))];

                if (in_array($sharingUserKey, $usersShared)) {
                    continue; // Si oui, passez à la prochaine itération de la boucle
                }

                $usersShared[] = $sharingUserKey;
                

                $share = [
                    'username' => $students[$sharingUserKey]['username'],
                    'user_id' => $students[$sharingUserKey]['students_id'],
                    'to' => [],
                ];
                    


                foreach ($sharedToUserKeys as $key) {
                    if ($key != $sharingUserKey) {
                        $share['to'][] = ['username' => $students[$key]['username']];
                    }
                }

                // Ajout du partage au post si ce n'est pas vide
                if (!empty($share['to'])) {
                    $post['shares'][] = $share;
                }
            }

            $post['shares_count'] = count($post['shares']);


            // Generation aleatoire des likes

            $usersLiked = [];
            $likesCount = rand(floor($totalStudents/3), $totalInstructors - 1);

            for ($k = 0; $k <= $likesCount; $k++) {
                $likingUserKey = rand(0, $totalStudents - 1);
                if (in_array($likingUserKey, $usersLiked)) {
                    continue; // Si oui, passez à la prochaine itération de la boucle
                }

                $usersLiked[] = $likingUserKey;
                $like = [
                    'username' => $students[$likingUserKey]['username'],
                    'user_id' => $students[$likingUserKey]['students_id'],
                ];

                // Ajout du like au post
                $post['likes'][] = $like;
            }

            $post['likes_count'] = count($post['likes']);



            $posts[] = $post;
        }
    }
}

// Caclul du nombre de co instructeurs etudiants

$totalfollowersI = 0;

foreach ($instructors as $instructor) {
    $totalfollowersI += $instructor['followers_count'];
}

$inst_stud_co = floor($totalfollowersI/$totalInstructors);

// Caclul du nombre de co etudiants etudiants

$totalfollowersS = 0;

foreach ($students as $student) {
    $totalfollowersS += $student['followers_count'];
}

$stud_stud_co = floor($totalfollowersS/$totalStudents);

// Calcul de la proba de persuasion
$totalLikes = 0;

foreach ($posts as $post) {
    $totalLikes += $post['likes_count'];
}

$proba_persu = $totalLikes/(count($posts)*$totalUsers);


// Calcul de la proba de corruption

$totalSharesForFakeNews = 0;
$fakeNewsCount = 0; 

foreach ($posts as $post) {
    if ($post['is_fake_news'] === true) { 
        $totalSharesForFakeNews += $post['shares_count'];
        $fakeNewsCount++;
    }
}

$proba_corrupt = $totalSharesForFakeNews / ($fakeNewsCount * $totalUsers);

// Aggrégation des données dans une structure unique
$data = [
    'students' => $students,
    'instructors' => $instructors,
    'posts' => $posts,
    'number_students' => $nb_students,
    'instructor-students_co' => $inst_stud_co,
    'students-students_co' => $stud_stud_co,
    'proba_persu' => $proba_persu,
    'proba_corrupt'=> $proba_corrupt,
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


