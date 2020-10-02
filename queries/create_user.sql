-- :name create_user :insert
INSERT INTO Users(username, email, password)
VALUES(:username, :email, :password)