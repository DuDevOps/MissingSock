BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "base_sync" (
	"id"	int,
	"base_id"	text,
	"Tag_id"	text,
	"GPS_lat"	text,
	"GPS_long"	text,
	"RSSI"	integer,
	"sync_id"	varchar(30),
	"timestamp"	TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "users" (
	"id"	INTEGER,
	"username"	varchar(250) NOT NULL,
	"password"	varchar(20) NOT NULL,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "base_station" (
	"id"	int,
	"base_id"	TEXT,
	"nicename"	TEXT,
	"user_id"	integer NOT NULL,
	FOREIGN KEY("user_id") REFERENCES "user"("id"),
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "tag_name" (
	"id"	int,
	"tag_id"	TEXT,
	"nicename"	TEXT,
	"user_id"	integer,
	FOREIGN KEY("user_id") REFERENCES "user"("id"),
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "billing" (
	"id"	integer,
	"user_id"	integer NOT NULL,
	"created"	TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	"description"	text,
	"debit"	DECIMAL,
	"credit"	DECIMAL,
	FOREIGN KEY("user_id") REFERENCES "user"("id"),
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "assets" (
	"id"	INTEGER,
	"asset_name"	TEXT,
	"asset_description"	TEXT,
	"tag_id"	INTEGER,
	"old_tag_id"	INTEGER,
	PRIMARY KEY("id")
);
INSERT INTO "base_sync" ("id","base_id","Tag_id","GPS_lat","GPS_long","RSSI","sync_id","timestamp") VALUES (NULL,'BASE0132','TAG001','-25.6859','28.2726',23.9,'T002001','2021-10-26 16:09:39'),
 (NULL,'BASE0132','TAG002','-25.6859','28.2726',1.9,'T002001','2021-10-26 16:09:40'),
 (NULL,'BASE0132','TAG003','-25.6859','28.2726',20.9,'T002001','2021-10-26 16:09:41'),
 (NULL,'BASE0132','TAG001','-25.6859','28.2726',3.9,'T002001','2021-10-26 16:10:11'),
 (NULL,'BASE0132','TAG002','-25.6859','28.2726',0.9,'T002001','2021-10-26 16:10:12'),
 (NULL,'BASE0132','TAG003','-25.6859','28.2726',2.9,'T002001','2021-10-26 16:10:13'),
 (NULL,'BASE0140','TAG001','-25.7059','28.2726',3.9,'T002001','2021-10-26 16:10:43'),
 (NULL,'BASE0140','TAG002','-25.7059','28.2726',0.9,'T002001','2021-10-26 16:10:44'),
 (NULL,'BASE0140','TAG003','-25.7059','28.2726',2.9,'T002001','2021-10-26 16:10:45'),
 (NULL,'BASE0150','TAG001','-25.7159','28.3026',13.9,'T002001','2021-10-26 16:10:55'),
 (NULL,'BASE0150','TAG002','-25.7159','28.3026',10.9,'T002001','2021-10-26 16:10:56'),
 (NULL,'BASE0150','TAG003','-25.7159','28.3026',12.9,'T002001','2021-10-26 16:10:57'),
 (NULL,'BASE0160','TAG001','-25.6870','28.2726',13.9,'T002001','2021-10-25 16:11:02'),
 (NULL,'BASE0160','TAG002','-25.6875','28.2726',10.9,'T002001','2021-10-26 16:11:05'),
 (NULL,'BASE0160','TAG003','-25.7158','28.2726',12.9,'T002001','2021-10-27 16:11:08'),
 (NULL,'BASE0160','TAG004','-25.6875','28.2726',12.3,'T002002','2021-10-28 07:49:31');
INSERT INTO "users" ("id","username","password") VALUES (1,'koosbilly9@gmail.com','kooskoos');
INSERT INTO "base_station" ("id","base_id","nicename","user_id") VALUES (NULL,'BASE0132','Water Gat',1),
 (NULL,'BASE0140','Kraal',1),
 (NULL,'BASE0150','Pad Hek',1),
 (NULL,'BASE0160','Land Rover',1);
INSERT INTO "tag_name" ("id","tag_id","nicename","user_id") VALUES (NULL,'TAG001','Brown Cow',1),
 (NULL,'TAG002','Green Cow',1),
 (NULL,'TAG003','Pink Cow',1),
 (NULL,'TAG004','Brown Cow 2',1),
 (NULL,'TAG005','Green Cow 3',1),
 (NULL,'TAG006','Pink Cow 4',1),
 (NULL,'TAG007','Brown Cow 2',1),
 (NULL,'TAG008','Green Cow 3',1),
 (NULL,'TAG009','Pink Cow 4',1);
INSERT INTO "billing" ("id","user_id","created","description","debit","credit") VALUES (1,1,'2021-10-26 16:09:39',NULL,200,NULL);
INSERT INTO "assets" ("id","asset_name","asset_description","tag_id","old_tag_id") VALUES (1,'James','Pig','TAG009','TAG006'),
 (2,'Jim','Bull','TAG002',''),
 (3,'Jane','Brown Cow','TAG003',NULL),
 (4,'John','Black Cow','TAG004',NULL),
 (5,'Bill','Sheep','TAG005',NULL),
 (6,'Shawn','Sheep','TAG006',NULL);
COMMIT;
