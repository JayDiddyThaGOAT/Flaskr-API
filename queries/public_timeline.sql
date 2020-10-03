-- :name public_timeline :many
SELECT author_name, created, tweet FROM Posts
ORDER BY created DESC
LIMIT 25