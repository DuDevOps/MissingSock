select base_id, tag_id, gps_lat, gps_long, rssi, sync_id, timestamp 
 from base_sync where timestamp like '{DAY_1}' ;
 
 select distinct date_format(timestamp,'%Y/%m/%d') , DATE_SUB(timestamp, INTERVAL 2 DAY) from base_sync ;