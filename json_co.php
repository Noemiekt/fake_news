<?php
header('Content-Type: application/json');

// Utilisateurs
$users = array(
    array('user_id' => 1, 
          'username' => 'toto', 
          'followers' => $followers = array(
              array('username' => 'titi'),
              array('username' => 'tutu'),
              array('username' => 'titi'),
              array('username' => 'lala'),
              array('username' => 'tete')
          ),
  
          'followers_count' => $followers_count = count($followers),
      ),
          
    array('user_id' => 2, 
          'username' => 'titi', 
          'followers' => $followers = array(
              array('username' => 'lala')
          ),
  
          'followers_count' => $followers_count = count($followers),
      ),
    array('user_id' => 3, 
          'username' => 'tata', 
          'followers' => $followers = array(
              array('username' => 'tete'),
              array('username' => 'tutu'),
          ),
  
          'followers_count' => $followers_count = count($followers),
      ),
    array('user_id' => 4, 
          'username' => 'tutu', 
          'followers' => $followers = array(
              array('username' => 'toto'),
              array('username' => 'tata'),
              array('username' => 'lala'),
              array('username' => 'tete')
          ),
  
          'followers_count' => $followers_count = count($followers),
      ),
    array('user_id' => 5, 
          'username' => 'tete', 
          'followers' => $followers = array(
              array('username' => 'tyty'),
              array('username' => 'tata'),
          ),
  
          'followers_count' => $followers_count = count($followers),
      ),
    array('user_id' => 6, 
          'username' => 'tyty', 
          'followers' => $followers = array(
              array('username' => 'tete')
          ),
  
          'followers_count' => $followers_count = count($followers),
      ),
    array('user_id' => 7, 
          'username' => 'lala', 
          'followers' => $followers = array(
              array('username' => 'tutu'),
          ),
  
          'followers_count' => $followers_count = count($followers),
      ),
  );

// Publications
$posts = array(
    array('post_id' => 1, 
          'user_id' => 1, 
          'is_fake_news' => true,
          'shares' => $shares = array(
            array('username' =>'tata',
                   'to' => $to = array(
                     array('username' => 'tete'),
                     array('username' => 'tutu'),
                   ),
                ),
            array('username' =>'tete',
                   'to' => $to = array(
                     array('username' => 'tyty'),
                   ),
                ),
            array('username' =>'tutu',
                  'to' => $to = array(
                    array('username' => 'lala'),
                   ),
                ),
            array('username' =>'lala',
                  'to' => $to = array(
                    array('username' => 'titi'),
                  ),
                ),    
          ),
          'shares_count' => $shares_count = count($shares),
        ),
    array('post_id' => 2, 
          'user_id' => 2, 
          'is_fake_news' => false,
          'shares' => $shares = array(
            array('username' =>'lala',
                   'to' => $to = array(
                     array('username' => 'tutu'),
                   ),
                ),
            array('username' =>'tutu',
                   'to' => $to = array(
                     array('username' => 'tete'),
                     array('username' => 'toto'),
                   ),
                ),    
          ),
          'shares_count' => $shares_count = count($shares),
        ),
    array('post_id' => 3, 
          'user_id' => 3, 
          'is_fake_news' => true,
          'shares' => $shares = array(
            array('username' =>'lala',
                    'to' => $to = array(
                        array('username' => 'titi'),
                    ),
                ), 
            array('username' =>'titi',
                    'to' => $to = array(
                        array('username' => 'toto'),
                    ),
                ), 
            array('username' =>'toto',
                    'to' => $to = array(
                        array('username' => 'tutu'),
                    ),
                ), 
            array('username' =>'tutu',
                    'to' => $to = array(
                    array('username' => 'tete'),
                    ),
                ),
            array('username' =>'tete',
                    'to' => $to = array(
                        array('username' => 'tyty'),
                    ),
                ),
            ),
            'shares_count' => $shares_count = count($shares),
        ),
    array('post_id' => 4, 
          'user_id' => 6, 
          'is_fake_news' => false,
          'shares' => $shares = array(
            array('username' =>'tete',
                   'to' => $to = array(
                     array('username' => 'tata'),
                   ),
                ),
            array('username' =>'tata',
                   'to' => $to = array(
                     array('username' => 'toto'),
                   ),
                ),
            ),
            'shares_count' => $shares_count = count($shares),
        ),
    array('post_id' => 5, 
          'user_id' => 7, 
          'is_fake_news' => true,
          'shares' => $shares = array(
            array('username' =>'titi',
                    'to' => $to = array(
                        array('username' => 'toto'),
                    ),
                ),
            array('username' =>'toto',
                    'to' => $to = array(
                        array('username' => 'tutu'),
                    ),
                ),
            array('username' =>'tutu',
                    'to' => $to = array(
                    array('username' => 'tata'),
                    ),
                ),
            array('username' =>'tata',
                    'to' => $to = array(
                    array('username' => 'tete'),
                    ),
                ),
            ),
            'shares_count' => $shares_count = count($shares),
        ),
);

// Aggrégation des données dans une structure unique
$data = array(
  'users' => $users,
  'posts' => $posts,
);

echo json_encode($data, JSON_PRETTY_PRINT);
?>
