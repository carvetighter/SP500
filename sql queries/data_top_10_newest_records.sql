use Finance
select top(10) * 
from sp500.data
order by date_date desc

--delete from sp500.data
--where date_date >= '2019-01-01'