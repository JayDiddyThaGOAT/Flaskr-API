DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS Relationships;
DROP TABLE IF EXISTS Posts;

CREATE TABLE Users(
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE Relationships(
    follower_name TEXT NOT NULL,
    followed_name TEXT NOT NULL,
    FOREIGN KEY (follower_name) REFERENCES Users (username),
    FOREIGN KEY (followed_name) REFERENCES Users (username),
    PRIMARY KEY (follower_name, followed_name)
);

CREATE TABLE Posts(
    post_id INTEGER PRIMARY KEY AUTOINCREMENT,
    author_name TEXT NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    tweet TEXT NOT NULL,
    FOREIGN KEY (author_name) REFERENCES Users (username)
);