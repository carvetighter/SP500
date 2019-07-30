use Finance
select top(10) *
from sp500.analysis
order by date_analysis desc

--use Finance
--delete from sp500.analysis
--where date_analysis >= '2019-07-27'