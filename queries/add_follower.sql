-- :name add_follower :insert
INSERT INTO Relationships(follower_name, followed_name)
VALUES(:follower_name, :followed_name)