DELIMITER //

CREATE or REPLACE PROCEDURE ins_upd_base_stations( IN in_SYNC_BASE_ID TEXT, IN in_GPS_LONG TEXT, IN in_GPS_LAT TEXT) 
BEGIN
    DECLARE
     new_id INT ;

--  check if new base station
   IF ( (select count(*) from base_station where sync_base_id = in_SYNC_BASE_ID  ) = 0)
   then
     insert into base_station(SYNC_BASE_ID) values(in_SYNC_BASE_ID ) ;
     select id into new_id from base_station where sync_base_id = in_SYNC_BASE_ID ;
     
     insert into base_station_current(ID, GPS_LONG, GPS_LAT) values(new_id, in_GPS_LONG, in_GPS_LAT ) ;
     insert into base_station_hist(base_ID, GPS_LONG, GPS_LAT) values(new_id, in_GPS_LONG, in_GPS_LAT ) ;

   ELSE
     select id into new_id from base_station where sync_base_id = in_SYNC_BASE_ID ;

   END IF ; 
   
--  check if new coordinates
   IF ( (select count(*) from base_station_current where id = new_id and gps_lat = in_GPS_LAT and gps_long = in_GPS_LONG ) = 0) 
   THEN
      update base_station_current set gps_long = in_GPS_LONG, gps_lat = in_GPS_LAT WHERE id = new_id ;
      insert into base_station_hist(base_id, GPS_LONG, GPS_LAT ) values(new_id, in_GPS_LONG, in_GPS_LAT  ) ;
  END IF ;
  
END 

//

DELIMITER ;


DELIMITER //

CREATE or REPLACE PROCEDURE ins_upd_tag( IN in_SYNC_TAG_ID TEXT, IN in_GPS_LONG TEXT, IN in_GPS_LAT TEXT) 
BEGIN
    DECLARE
     new_id INT ;

--  check if new base station
   IF ( (select count(*) from tag where sync_tag_id = in_SYNC_TAG_ID  ) = 0)
   then
     insert into tag(SYNC_tag_ID) values(in_SYNC_tag_ID ) ;
     select id into new_id from tag where sync_tag_id = in_SYNC_TAG_ID ;
     
     insert into tag_current(ID, GPS_LONG, GPS_LAT) values(new_id, in_GPS_LONG, in_GPS_LAT ) ;
     insert into tag_hist(tag_ID, GPS_LONG, GPS_LAT) values(new_id, in_GPS_LONG, in_GPS_LAT ) ;
     
   ELSE
     select id into new_id from tag where sync_tag_id = in_SYNC_TAG_ID ;

   END IF ; 
   
--  check if new coordinates
   IF ( (select count(*) from tag_current where id = new_id and gps_lat = in_GPS_LAT and gps_long = in_GPS_LONG ) = 0) 
   THEN
      update tag_current set gps_long = in_GPS_LONG, gps_lat = in_GPS_LAT WHERE id = new_id ;
      insert into tag_hist(tag_id, GPS_LONG, GPS_LAT ) values(new_id, in_GPS_LONG, in_GPS_LAT  ) ;
  END IF ;
  
END 

//

DELIMITER ;

-- =================================

DELIMITER //

CREATE TRIGGER after_base_sync_insert
AFTER INSERT
ON base_sync FOR EACH ROW
BEGIN
    CALL ins_upd_tag(
         NEW.TAG_ID , 
         NEW.GPS_LONG , 
         NEW.GPS_LAT 
    );

    CALL ins_upd_base_stations(
         NEW.BASE_ID , 
         NEW.GPS_LONG , 
         NEW.GPS_LAT 
    );

END ;

//

DELIMITER ;



insert into base_sync (base_id, tag_id, gps_lat, gps_long, rssi, sync_id) 
values ('base_0', 'tag_0', -25.557164, 28.49824, 85, 0),
('base_0', 'tag_0', -25.557164, 28.49824, 85, 1),
('base_1', 'tag_0', -25.557527, 28.500515, 85, 2),
('base_1', 'tag_0', -25.557527, 28.500515, 85, 3),
('base_2', 'tag_0', -25.559192, 28.500756, 85, 4),
('base_2', 'tag_0', -25.559192, 28.500756, 85, 5),
('base_2', 'tag_0', -25.559192, 28.500756, 85, 6),
('base_3', 'tag_0', -25.55866, 28.498444, 85, 7) ;