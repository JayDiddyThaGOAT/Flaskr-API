-- :name remove_follower :affected
DELETE FROM Relationships
WHERE follower_name=:follower_name AND followed_name=:followed_name