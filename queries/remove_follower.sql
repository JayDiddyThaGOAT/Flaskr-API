-- :name remove_follower :affected
DELETE FROM Relationships
WHERE follower_id=:follower_id AND followed_id=:followed_id