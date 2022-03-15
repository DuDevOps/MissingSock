
select  * 
    from asset_breeding 
where users_id in (84, 85, 86, 87, 88, 89, 90, 92,
             93, 95, 97, 98, 99) ;

select  * 
    from asset_medical
where users_id in (84, 85, 86, 87, 88, 89, 90, 92,
             93, 95, 97, 98, 99) ;

select  * 
    from asset_produce
where users_id in (84, 85, 86, 87, 88, 89, 90, 92,
             93, 95, 97, 98, 99) ;

select  * 
    from asset_registry 
where users_id in (84, 85, 86, 87, 88, 89, 90, 92,
             93, 95, 97, 98, 99) ;

select  * 
    from base_station
where user_id in (84, 85, 86, 87, 88, 89, 90, 92,
             93, 95, 97, 98, 99) ;

select  * 
    from base_station_current
where user_id in (84, 85, 86, 87, 88, 89, 90, 92,
             93, 95, 97, 98, 99) ;

select  * from base_station_hist ;

select count(*) , min(timestamp) , max(timestamp) 
from base_sync
where 
timestamp < NOW() - INTERVAL 60 DAY ;

select  * from billing ;

select  * 
    from tag
where users_id in (84, 85, 86, 87, 89, 90, 92,
             93, 95, 97, 98, 99) ;

select  * from tag_current
select  * from tag_hist;

select  * 
    from users
where id in (84, 85, 86, 87, 89, 90, 92,
             93, 95, 97, 98, 99) ;