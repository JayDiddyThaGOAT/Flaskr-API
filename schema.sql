DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS Relationships;

CREATE TABLE Users(
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE Relationships(
    follower_id INTEGER NOT NULL,
    followed_id INTEGER NOT NULL,
    FOREIGN KEY (follower_id) REFERENCES Users (user_id),
    FOREIGN KEY (followed_id) REFERENCES Users (user_id),
    PRIMARY KEY (follower_id, followed_id)
);