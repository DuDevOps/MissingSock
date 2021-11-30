select a.* , b.nicename 
from base_sync a
left join base_station b on a.base_id = b.base_id
where a.base_id||a.created in (
select distinct a.base_id||max(a.created)
 from base_sync a
 group by a.base_id)  ;