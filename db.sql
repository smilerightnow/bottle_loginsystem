CREATE DATABASE bottle;
USE bottle;

CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `username` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL,
  `is_activated` BOOLEAN DEFAULT 1,
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP
);
/* data:IPs and User-agents will be hashed.*/
CREATE TABLE `sessions` (
  `id` varchar(100) NOT NULL PRIMARY KEY,
  `email` varchar(100) UNIQUE NOT NULL,
  `data` varchar(100) NOT NULL,
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE `apps` (
  `id` int NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `user` int NOT NULL,
  `title` varchar(100) NOT NULL,
  `letype` varchar(100) NOT NULL,
  `data` varchar(10000) NOT NULL,
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP
);
