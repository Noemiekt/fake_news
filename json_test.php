<?php
header('Content-Type: application/json');

// Utilisateurs
$users = array(
  array('user_id' => 1, 'username' => 'user1', 'followers_count' => 100),
  array('user_id' => 2, 'username' => 'user2', 'followers_count' => 150),
  array('user_id' => 3, 'username' => 'user3', 'followers_count' => 200),
  array('user_id' => 4, 'username' => 'user4', 'followers_count' => 250),
  array('user_id' => 5, 'username' => 'user5', 'followers_count' => 300),
  array('user_id' => 6, 'username' => 'user6', 'followers_count' => 350),
  array('user_id' => 7, 'username' => 'user7', 'followers_count' => 400),
  array('user_id' => 8, 'username' => 'user8', 'followers_count' => 450),
  array('user_id' => 9, 'username' => 'user9', 'followers_count' => 500),
  array('user_id' => 10, 'username' => 'user10', 'followers_count' => 550),
);

// Publications
$posts = array(
  array('post_id' => 1, 'user_id' => 1, 'content' => 'Fake health news #1', 'is_fake_news' => true, 'likes' => 10, 'comments' => 5, 'shares' => 3),
  array('post_id' => 2, 'user_id' => 2, 'content' => 'Real health news #1', 'is_fake_news' => false, 'likes' => 15, 'comments' => 8, 'shares' => 4),
  array('post_id' => 3, 'user_id' => 3, 'content' => 'Fake health news #2', 'is_fake_news' => true, 'likes' => 20, 'comments' => 10, 'shares' => 5),
  array('post_id' => 4, 'user_id' => 4, 'content' => 'Real health news #2', 'is_fake_news' => false, 'likes' => 25, 'comments' => 12, 'shares' => 6),
  array('post_id' => 5, 'user_id' => 5, 'content' => 'Interesting fact about health', 'is_fake_news' => false, 'likes' => 30, 'comments' => 14, 'shares' => 7),
  array('post_id' => 6, 'user_id' => 6, 'content' => 'Misleading health fact #1', 'is_fake_news' => true, 'likes' => 35, 'comments' => 16, 'shares' => 8),
  array('post_id' => 7, 'user_id' => 7, 'content' => 'Important health update', 'is_fake_news' => false, 'likes' => 40, 'comments' => 18, 'shares' => 9),
  array('post_id' => 8, 'user_id' => 8, 'content' => 'Misleading health fact #2', 'is_fake_news' => true, 'likes' => 45, 'comments' => 20, 'shares' => 10),
  array('post_id' => 9, 'user_id' => 9, 'content' => 'Health myth debunked', 'is_fake_news' => false, 'likes' => 50, 'comments' => 22, 'shares' => 11),
  array('post_id' => 10, 'user_id' => 10, 'content' => 'Viral health scare #1', 'is_fake_news' => true, 'likes' => 55, 'comments' => 24, 'shares' => 12),
);

// Relations de suivi
$follows = array(
  array('follower_user_id' => 1, 'following_user_id' => 2),
  array('follower_user_id' => 1, 'following_user_id' => 3),
  array('follower_user_id' => 2, 'following_user_id' => 3),
  array('follower_user_id' => 2, 'following_user_id' => 4),
  array('follower_user_id' => 3, 'following_user_id' => 4),
  array('follower_user_id' => 3, 'following_user_id' => 5),
  array('follower_user_id' => 4, 'following_user_id' => 5),
  array('follower_user_id' => 4, 'following_user_id' => 6),
  array('follower_user_id' => 5, 'following_user_id' => 6),
  array('follower_user_id' => 5, 'following_user_id' => 7),
  array('follower_user_id' => 6, 'following_user_id' => 7),
  array('follower_user_id' => 6, 'following_user_id' => 8),
  array('follower_user_id' => 7, 'following_user_id' => 8),
  array('follower_user_id' => 7, 'following_user_id' => 9),
  array('follower_user_id' => 8, 'following_user_id' => 9),
  array('follower_user_id' => 8, 'following_user_id' => 10),
  array('follower_user_id' => 9, 'following_user_id' => 10),
  array('follower_user_id' => 9, 'following_user_id' => 1),
  array('follower_user_id' => 10, 'following_user_id' => 1),
  array('follower_user_id' => 10, 'following_user_id' => 2),
);

// Aggrégation des données dans une structure unique
$data = array(
  'users' => $users,
  'posts' => $posts,
  'follows' => $follows,
);

echo json_encode($data, JSON_PRETTY_PRINT);
?>
