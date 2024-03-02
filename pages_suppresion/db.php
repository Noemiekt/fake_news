<?php
$servername = "localhost";
$username = "newuser";
$password = "password";
$dbname = "projet6";

// Créer la connexion
$conn = new mysqli($servername, $username, $password, $dbname);

// Vérifier la connexion
if ($conn->connect_error) {
    die("Échec de la connexion: " . $conn->connect_error);
}
?>
