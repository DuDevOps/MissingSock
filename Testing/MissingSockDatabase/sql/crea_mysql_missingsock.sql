-- Adminer 4.7.1 MySQL dump

SET NAMES utf8;
SET time_zone = '+00:00';
SET foreign_key_checks = 0;
SET sql_mode = 'NO_AUTO_VALUE_ON_ZERO';

SET NAMES utf8mb4;

DROP TABLE IF EXISTS `assets`;
CREATE TABLE `assets` (
  `id` int(11) DEFAULT NULL,
  `asset_name` int(11) NOT NULL,
  `asset_description` int(11) NOT NULL,
  `tag_id` int(11) NOT NULL,
  `dz_tag_id` datetime NOT NULL,
  `old_tag_id` int(11) NOT NULL,
  `dz_old_tag_id` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


DROP TABLE IF EXISTS `base_station`;
CREATE TABLE `base_station` (
  `id` int(11) DEFAULT NULL,
  `base_id` text NOT NULL,
  `nicename` text NOT NULL,
  `use_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


DROP TABLE IF EXISTS `base_sync`;
CREATE TABLE `base_sync` (
  `id` int(11) DEFAULT NULL,
  `base_id` text NOT NULL,
  `tag_id` text NOT NULL,
  `GPS_lat` text NOT NULL,
  `GPS_long` text NOT NULL,
  `RSSI` int(11) NOT NULL,
  `sync_id` text NOT NULL,
  `timestamp` datetime DEFAULT NULL ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


DROP TABLE IF EXISTS `billing`;
CREATE TABLE `billing` (
  `id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  `timestamp` datetime DEFAULT NULL,
  `description` text NOT NULL,
  `debit` decimal(10,0) NOT NULL,
  `credit` decimal(10,0) NOT NULL,
  KEY `user_id` (`user_id`),
  CONSTRAINT `billing_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


DROP TABLE IF EXISTS `tag_name`;
CREATE TABLE `tag_name` (
  `id` int(11) NOT NULL,
  `tag_id` int(11) NOT NULL,
  `nicename` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  KEY `user_id` (`user_id`),
  CONSTRAINT `tag_name_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` text NOT NULL,
  `password` text NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO `users` (`id`, `username`, `password`) VALUES
(1,	'tom',	''),
(2,	'Dick',	''),
(3,	'Harry',	''),
(4,	'',	'');

-- 2021-10-28 13:34:36