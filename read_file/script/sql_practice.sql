select 
user_id,
sum(case when type = 'buy' then amount * 0.015 when type = 'sell' then amount * 0.01 else 0 end)  as total_fee
from 
transactions
group by 1;