-- select a.id, a.base_id, a.tag_id, a.timestamp, a.RSSI, a.sync_id,
--                                        b.nicename, a.gps_lat, a.gps_long
--                                     from base_sync a
--                                     left join base_station b on a.base_id = b.base_id
--                                     where a.base_id||a.timestamp in (
--                                     select distinct a.base_id||max(a.timestamp)
--                                      from base_sync a
--                                      group by a.base_id) ;
									 
select a.id, a.asset_name, a.asset_description, a.tag_id, a.old_tag_id 
from assets a 
left join tag_name b on a.tag_id = b.tag_id 
left join base_sync c on a.tag_id = c.tag_id ;