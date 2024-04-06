<?php
include 'db.php'; // Inclure le fichier de connexion

$sql = "SELECT * FROM suivi_suppressions";
$result = $conn->query($sql);

// Vérifier si le résultat contient des lignes avant de générer le tableau
if ($result->num_rows > 0) {
    // Déplacer le code HTML pour le tableau dans la section HTML pour une meilleure structure et lisibilité
    $rows = [];
    while($row = $result->fetch_assoc()) {
        $rows[] = $row; // Stocker les lignes pour une utilisation dans le HTML ci-dessous
    }
} else {
    $message = "0 résultats";
}
$conn->close(); // Il est bon de fermer la connexion ici, après avoir terminé les opérations de base de données
?>

<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Historique des Suppressions</title>
</head>
<body>
    <h1>Historique des Suppressions</h1>
    <?php if (!empty($rows)): ?>
    <table>
        <tr>
            <th>ID</th>
            <th>Nom</th>
            <th>Email</th>
            <th>Date de Suppression</th>
        </tr>
        <?php foreach ($rows as $row): ?>
        <tr>
            <td><?php echo htmlspecialchars($row["id"]); ?></td>
            <td><?php echo htmlspecialchars($row["nom"]); ?></td>
            <td><?php echo htmlspecialchars($row["email"]); ?></td>
            <td><?php echo htmlspecialchars($row["date_suppression"]); ?></td>
        </tr>
        <?php endforeach; ?>
    </table>
    <?php else: ?>
    <p><?php echo isset($message) ? $message : ''; ?></p>
    <?php endif; ?>
</body>
</html>
