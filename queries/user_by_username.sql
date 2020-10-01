-- :name user_by_username :one
SELECT * FROM users
WHERE username = :username