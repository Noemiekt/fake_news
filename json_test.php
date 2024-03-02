<?php
header('Content-Type: application/json');

// Noms avec catégories de publication
$noms = array(
  array('Nom' => 'Toto', 'Publication' => 'Nouveaux vaccin covid'),
  array('Nom' => 'Tata', 'Publication' => 'Le vaccin a tué 2 personnes'),
  array('Nom' => 'Titi', 'Publication' => 'Les vaccins sont créés par le gouvernement'),
);

$data = array(
  'Noms' => $noms,
);
echo json_encode($data);

?>
