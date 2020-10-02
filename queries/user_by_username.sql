-- :name user_by_username :one
SELECT * FROM Users
WHERE username = :username