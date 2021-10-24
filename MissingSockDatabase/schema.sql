-- create database
create database missingsock ;

-- switch to database
use missingsock ;

-- check which databse you are connected on
select database() ;

-- Add users mis_read , mis_write , mis_create

CREATE USER 'mis_create'@'missingsock' IDENTIFIED BY 'mis-mis-create';
CREATE USER 'mis_write'@'missingsock' IDENTIFIED BY 'mis-mis-wite';
CREATE USER 'mis_read'@'missingsock' IDENTIFIED BY 'mis-read';

-- switch to mis_create user to create tables / grant insert,update,select ,delete to mis-write / grant select to mis-read
-- before creating 
select  user() ;

-- Initialize the database.
-- Drop any existing data and create empty tables.


CREATE TABLE user (
  id int PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE billing (
  id int PRIMARY KEY AUTOINCREMENT,
  FOREIGN KEY (user_id) REFERENCES user (id),
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  debit DECIMAL ,
  credit DECIMAL
);

CREATE TABLE base_sync (
  id int PRIMARY KEY AUTOINCREMENT,
  FOREIGN KEY (base_id) REFERENCES base_station (id) ,
  FOREIGN KEY (Tag_id) REFERENCES tag_name (id),
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  GPS_LOCAL point ,
  Tag_relative_strength DECIMAL,
  sync_id varchar(30)
);

CREATE TABLE base_station (
  id int PRIMARY KEY AUTOINCREMENT,
  base_id TEXT ,
  nicename TEXT ,
  FOREIGN KEY (user_id) REFERENCES user (id)
);

CREATE TABLE tag_name (
  id int PRIMARY KEY AUTOINCREMENT,
  tag_id TEXT ,
  nicename TEXT ,
  FOREIGN KEY (user_id) REFERENCES user (id)
);

