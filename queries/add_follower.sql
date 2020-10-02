-- :name add_follower :insert
INSERT INTO Relationships(follower_id, followed_id)
VALUES(:follower_id, :followed_id)