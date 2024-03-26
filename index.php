<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>mon site</title>
    <link rel="stylesheet" href="./style_header.css">
    <link rel="stylesheet" href="./style.css">
</head>
<?php include './header.php'; ?>
<body>
    <div class="page">
        <div class="haut">
            Autorisation de partage de données
        </div>
        <div class="autorisation">
            <div class="texte">En cliquant sur le bouton vous acceptez l'exploitation de vos données sur Instagram dans le cadre de nos recherches.</div>
            <div class="bouton_autorisation" onclick="accept()">
                <button>Accepter</button>
            </div>
        </div>
    </div>
    <script>
        function accept() {
            var xhttp = new XMLHttpRequest();
            xhttp.onreadystatechange = function() {
                if (this.readyState == 4 && this.status == 200) {
                    window.location.href = "index.php";
                }
            };
            xhttp.open("GET", "./accept.php", true);
            xhttp.send();
        }
    </script>
</body>
</html>