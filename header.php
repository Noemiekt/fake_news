<?php
    session_start();
?>
<div class="nav-container">
    <div class="banniere">
        <a class="logo" href="index.php">
            <img src="./images/logo.png" class="image">
        </a>
        <div class="option">
            <a class="bouton" href="#">
                je
            </a>
        </div>
        <div class="option">
            <a class="bouton" href="#">
                sais 
            </a>
        </div>
        <div class="option">
            <a class="bouton" href="#">
                pas
            </a>
        </div>
        <div class="option">
            <?php
                if($_SESSION['pseudo_client']){
                    $answer1 = 'home.php';
                    $answer2 = 'Mon compte';
                }else {
                    $answer1 = 'connexion.php';
                    $answer2 = 'Me connecter';
                }
                $a = '<a class="bouton" href="'.$answer1.'">'.$answer2.'</a>';
                echo $a;
            ?>
        </div>
    </div>
</div>