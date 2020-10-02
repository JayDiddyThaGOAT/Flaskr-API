-- :name show_following :many
SELECT Relationships.follower_id, Relationships.followed_id, Users.username, Users.email
FROM Relationships
INNER JOIN Users ON (Relationships.followed_id = Users.user_id)
WHERE follower_id = :follower_id