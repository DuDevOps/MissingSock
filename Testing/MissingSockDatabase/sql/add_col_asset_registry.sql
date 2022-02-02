ALTER TABLE `asset_registry`
ADD `asset_breeding_id` int(11) NULL,
ADD FOREIGN KEY (`asset_breeding_id`) REFERENCES `asset_breeding` (`id`);