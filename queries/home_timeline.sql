-- :name home_timeline :many
SELECT author_name, created, tweet FROM
(
    SELECT Relationships.follower_name, Relationships.followed_name, Posts.author_name, Posts.created, Posts.tweet FROM Posts
    INNER JOIN Relationships ON (Relationships.followed_name = Posts.author_name)
    WHERE Relationships.follower_name = :follower_name
    ORDER BY created DESC
    LIMIT 25
)