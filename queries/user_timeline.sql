-- :name user_timeline :many
SELECT author_name, created, tweet FROM Posts
WHERE author_name=:username
ORDER BY created DESC
LIMIT 25