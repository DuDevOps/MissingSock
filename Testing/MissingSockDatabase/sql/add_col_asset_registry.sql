ALTER TABLE `asset_registry`
ADD `asset_breeding_id` int(11) NULL,
ADD FOREIGN KEY (`asset_breeding_id`) REFERENCES `asset_breeding` (`id`);

ALTER TABLE `asset_registry`
CHANGE `name` `animal_reg_no` text COLLATE 'utf8mb4_general_ci' NULL COMMENT 'Rename - name' AFTER `tag_id`;

commit ;