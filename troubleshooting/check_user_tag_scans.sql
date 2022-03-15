select * from asset_registry
where users_id = 96 ;

-- check tags linked to this user
select * from tag
where users_id = 96 ;

-- Check TAG current location
select * from tag_current
where 
    id in ( select tag_id 
        from asset_registry
        where 
            users_id = 96
        ) ;
    
-- Check BASESTATION current location
select * from base_station_current
where 
    id in ( select tag_id 
        from asset_registry
        where 
            users_id = 96
        ) ;