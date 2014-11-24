DROP TABLE if EXISTS entries;
CREATE TABLE entries (
       id INT NOT NULL AUTO_INCREMENT,
       title TEXT NOT NULL,
       text TEXT NOT NULL,
       PRIMARY KEY(id)
);

DROP TABLE if EXISTS users;
CREATE TABLE users (
       id INT NOT NULL AUTO_INCREMENT,
       username TEXT NOT NULL,
       passhash TEXT NOT NULL,
       PRIMARY KEY(id)
);

DROP TABLE if EXISTS sessions;
CREATE TABLE sessions (
       id INT NOT NULL AUTO_INCREMENT,
       createtime TEXT NOT NULL,
       username TEXT NOT NULL,
       token TEXT NOT NULL,
       PRIMARY KEY(id)
);
