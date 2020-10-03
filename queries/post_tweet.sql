-- :name post_tweet :insert
INSERT INTO Posts (author_name, tweet)
VALUES (:author_name, :tweet)