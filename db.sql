CREATE DATABASE CECS;
CREATE USER 'cecsuser'@'localhost' identified by 'cecspass123';
GRANT ALL PRIVILEGES ON CECS.* TO 'cecsuser'@'localhost';
FLUSH PRIVILEGES;
