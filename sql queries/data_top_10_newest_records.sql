use Finance
select top(10) * from sp500.data
order by date_date desc

use Finance
delete from sp500.data
--where date_date >= '2019-01-01'
--where date_date >= '2017-01-01'
where date_date >= '1970-01-01'