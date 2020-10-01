-- :name create_user :insert
INSERT INTO users(username, email, password)
VALUES(:username, :email, :password)