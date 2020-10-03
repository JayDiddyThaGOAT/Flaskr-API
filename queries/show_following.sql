-- :name show_following :many
SELECT username, email FROM
(
    SELECT Relationships.follower_name, Relationships.followed_name, Users.username, Users.email
    FROM Relationships
    INNER JOIN Users ON (Relationships.followed_name = Users.username)
    WHERE Relationships.follower_name = :follower_name
)