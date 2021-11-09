-- insert 14% / 36% / 18% / 32%
-- 126 / 324 / 162 / 288

select min(id) , max(id) from tag ;  -- 2078	2977

insert into base_sync (base_id, tag_id, gps_lat, gps_long, rssi, sync_id, timestamp) 
select a.sync_base_id, c.sync_tag_id, b.gps_lat, b.gps_long, 14, c.sync_tag_id  ,  NOW() - INTERVAL c.id SECOND
from base_station a , base_station_current  b, tag c
 where a.id = b.id 
and a.sync_base_id = 'base_0'
and c.id between 2078 and 2300 ;

insert into base_sync (base_id, tag_id, gps_lat, gps_long, rssi, sync_id, timestamp) 
select a.sync_base_id, c.sync_tag_id, b.gps_lat, b.gps_long, 14, c.sync_tag_id  ,  NOW() - INTERVAL c.id SECOND
from base_station a , base_station_current  b, tag c
 where a.id = b.id 
and a.sync_base_id = 'base_1'
and c.id between 2301 and 2500
 ;
 
insert into base_sync (base_id, tag_id, gps_lat, gps_long, rssi, sync_id, timestamp) 
select a.sync_base_id, c.sync_tag_id, b.gps_lat, b.gps_long, 14, c.sync_tag_id  ,  NOW() - INTERVAL c.id SECOND
from base_station a , base_station_current  b, tag c
 where a.id = b.id 
and a.sync_base_id = 'base_2'
and c.id between 2501 and 2777
 ;
 
insert into base_sync (base_id, tag_id, gps_lat, gps_long, rssi, sync_id, timestamp) 
select a.sync_base_id, c.sync_tag_id, b.gps_lat, b.gps_long, 14, c.sync_tag_id  ,  NOW() - INTERVAL c.id SECOND
from base_station a , base_station_current  b, tag c
 where a.id = b.id 
and a.sync_base_id = 'base_3'
and c.id between 2763 and 2977
 ;

--insert into base_sync (base_id, tag_id, gps_lat, gps_long, rssi, sync_id) ;
