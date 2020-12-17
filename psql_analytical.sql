-- create analytical (dwh) db
CREATE DATABASE olap;

-- connect to db
\c olap

ALTER ROLE postgres WITH PASSWORD 'P4ssw0rd!';
