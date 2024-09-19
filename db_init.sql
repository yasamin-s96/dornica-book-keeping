CREATE DATABASE IF NOT EXISTS book_keeping;

USE book_keeping;

CREATE TABLE IF NOT EXISTS roles
(
    id   BIGINT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    slug ENUM ('USER', 'MANAGER', 'ADMIN') NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT unique_name_slug UNIQUE (name, slug)
);


INSERT INTO roles (`name`, `slug`, `created_at`) VALUES ('user', 'user', NOW());
INSERT INTO roles (`name`, `slug`, `created_at`) VALUES ('manager', 'manager', NOW());
INSERT INTO roles (`name`, `slug`, `created_at`) VALUES ('admin', 'admin', NOW());

