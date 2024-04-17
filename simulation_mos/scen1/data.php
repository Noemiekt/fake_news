<?php
header('Content-Type: application/json');
$data = [
    'number_students' => 10,
    'instructor-students_co' => 5,
    'students-students_co' => 5,
    'timesteps' => 67,
    'proba_persu' => 0.26282051282051,
    'proba_corrupt' => 0.18666666666667,
];
$jsonData = json_encode($data, JSON_PRETTY_PRINT);
echo $jsonData;
?>