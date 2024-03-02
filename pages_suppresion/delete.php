<?php

ini_set('display_errors', 1);
error_reporting(E_ALL);

include 'db.php'; // Inclure le fichier de connexion

if (isset($_POST['confirm_delete'])) { // Vérifier si le formulaire a été soumis
    $id = $_POST['id']; // Utiliser les données du formulaire POST pour plus de sécurité

    // Préparer la requête SQL pour éviter les injections SQL
    $stmt = $conn->prepare("INSERT INTO demandes_suppression (user_id, confirmation_code, status, created_at, updated_at) SELECT user_id, confirmation_code, 'pending', NOW(), NOW() FROM demandes_suppression WHERE id = ?");
    $stmt->bind_param("i", $id); // "i" indique que l'ID est un entier

    // Exécuter la requête d'insertion
    if ($stmt->execute()) {
        // Préparer la requête de suppression
        $deleteStmt = $conn->prepare("DELETE FROM demandes_suppression WHERE id = ?");
        $deleteStmt->bind_param("i", $id); // Utiliser $deleteStmt au lieu de $stmt

        // Exécuter la requête de suppression
        if ($deleteStmt->execute()) {
            echo "Enregistrement supprimé avec succès";
        } else {
            echo "Erreur lors de la suppression: " . $conn->error;
        }

    } else {
        echo "Erreur lors de l'insertion dans suivi_suppressions: " . $conn->error;
    }

    $stmt->close(); // Fermer le statement
    $conn->close(); // Fermer la connexion à la base de données
    $deleteStmt->close();

}
?>

<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Confirmation de Suppression</title>
</head>
<body>
    <h1>Êtes-vous sûr de vouloir supprimer cet utilisateur ?</h1>
    <!-- Bouton de confirmation -->
    <form action="" method="post">
        <input type="hidden" name="id" value="<?php echo isset($_GET['id']) ? htmlspecialchars($_GET['id']) : ''; ?>">
        <button type="submit" name="confirm_delete">Confirmer la suppression</button>
    </form>
    <a href="list.html">Annuler</a>
</body>
</html>
