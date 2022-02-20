ALTER TABLE `asset_breeding`
CHANGE `start_date` `start_date` date NOT NULL AFTER `breeding_number`,
CHANGE `end_date` `end_date` date NULL AFTER `start_date`;

ALTER TABLE `asset_medical`
CHANGE `timestamp` `timestamp` date NOT NULL AFTER `asset_registry_id`;

ALTER TABLE `asset_produce`
CHANGE `timestamp` `timestamp` date NOT NULL DEFAULT '0000-00-00 00:00:00' AFTER `type`;

ALTER TABLE `asset_registry`
CHANGE `date_of_birth` `date_of_birth` date NULL AFTER `group_name`;

