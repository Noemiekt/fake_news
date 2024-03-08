<?php
// Assurez-vous que les données sont reçues en POST
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Récupérer les données envoyées depuis JavaScript
    $userIdentifier = $_POST['username_or_email'];
    $password = $_POST['password'];

    try {
        $pdo_options[PDO::ATTR_ERRMODE] = PDO::ERRMODE_EXCEPTION;
        $db = new PDO('mysql:host=localhost;dbname=espaceClients', 'lolo', 'CC!ZlcgqG3WD!Yt2', $pdo_options);

        // Utilisation de requêtes préparées pour éviter les injections SQL
        $sql = "SELECT passwordClient FROM clients WHERE emailClient = :identifier OR pseudoClient = :identifier";
        $stmt = $db->prepare($sql);
        $stmt->bindParam(':identifier', $userIdentifier);
        $stmt->execute();
        $row = $stmt->fetch(PDO::FETCH_ASSOC);

        $sql2 = "SELECT pseudoClient FROM clients WHERE emailClient = :identifier OR pseudoClient = :identifier";
        $stmt2 = $db->prepare($sql2);
        $stmt2->bindParam(':identifier', $userIdentifier);
        $stmt2->execute();
        $row2 = $stmt2->fetch(PDO::FETCH_ASSOC);

        if ($row) {
            $hashedPassword = $row['passwordClient'];
            $pseudo_client = $row2['pseudoClient'];

            // Vérifier la correspondance du mot de passe
            if (password_verify($password, $hashedPassword)) {
                // Mot de passe correct, l'utilisateur est authentifié avec succès
                // Faites les actions nécessaires ici (par exemple, enregistrez les informations de l'utilisateur dans une session, etc.)
                session_start();
                //$duration = 86400;
                //session_set_cookie_params($duration);
                $_SESSION['pseudo_client'] = $pseudo_client;
                $response = array('success' => true);
                echo json_encode($response);
            } else {
                // Mot de passe incorrect, renvoyer un message d'erreur
                $response = array('success' => false, 'message' => 'Mot de passe incorrect !');
                echo json_encode($response);
            }
        } else {
            // L'utilisateur n'a pas été trouvé dans la base de données, renvoyer un message d'erreur
            $response = array('success' => false, 'message' => 'Utilisateur non trouvé !');
            echo json_encode($response);
        }
    } catch (Exception $ex) {
        // En cas d'erreur, répondre avec un message d'erreur
        $response = array('success' => false, 'message' => 'Une erreur s\'est produite lors de l\'authentification.');
        echo json_encode($response);
    }
} else {
    // Répondre avec un message d'erreur si les données ne sont pas envoyées en POST
    $response = array('success' => false, 'message' => 'Requête invalide.');
    echo json_encode($response);
}
?>
