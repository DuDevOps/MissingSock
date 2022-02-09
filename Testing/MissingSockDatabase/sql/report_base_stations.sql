
-- Tags currently at each base station
select b.id , count(*)
from tag_current a, base_station b
where a.base_station_id = b.id 
group by b.id ;