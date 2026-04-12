-- Q1:Identify customers who made purchases on exactly three different days in the last month
-- Tables: purchases(customer_id,purchase_date)
select 
customer_id
from purchases 
where purchase_date >= date_sub(current_date, interval 1 month)
group by 1
having count(distinct purchase_date) = 3;

-- Q2: Find the top 2 highest-selling products for each category.
-- Tables: sales(product_id,sale_amount),products(product_id,category)
with sale_amount as (
select
s.product_id,
p.category,
sum(sale_amount) as sale_amount
from sales s 
join products p 
on s.product_id = p.product_id
group by 1,2)

select product_id, category from (
select 
product_id,
category,
row_number()over (partition by category order by sale_amount desc) as rn 
from sale_amount) t
where rn < 3;

-- Q3: Detect anomalies where sales for a product are 50% lower than the average for that product
-- Tables: sales(product_id, sale_amount)
with avg_sale as (
select 
product_id,
avg(sale_amount) as avg_sale
from sales
group by 1)

select 
product_id
from sales s
join avg_sale a 
on s.product_id = a.product_id
where s.sale_amount < 0.5 * a.avg_sale;

-- Q4: Find employees who have never been a manager and have worked in more than one department.
-- Tables: employees(employee_id,name,manager_id,department_id)
select 
e1.employee_id,
e1.name 
from employees e1
where 
exists
(
select 1
from employees e2
where e1.employee_id = e2.employee_id
group by 1
having count(distinct e2.department_id) > 1
)
and not exists (
select 1
from employees e3
where e1.employee_id = e3.manager_id) ;

-- Q5:Caculate the median salary in each department
-- Tables: employees(employee_id, department_id, salary)

with dept_info as (
select
employee_id,
department_id,
salary,
count(*) over (partition by department_id) as dept_count,
row_number() over (partition by department_id order by salary) as rn
from employees)

select
department_id,
avg(salary) as dept_median
from dept_info 
where rn in (floor((dept_count+1)/2), ceiling((dept_count+1)/2))
group by 1;


-- Q6: identify customers who purchased products from all available categories
-- tables: purchases(customer_id,product_id), products(product_id,category)
select 
customer_id
from purchases p1
join products p2
on p1.product_id = p2.product_id
group by 1
having count(distinct p2.category) = (

select count(distinct category) 
from products );


-- Q7: calculate the cumulative sales for each store, but only include dates where the daily sales exceeded the stores'average daily sales.
-- Tables:sales(store_id,sale_amount,sale_date)
with daily_sale as (
    select 
        store_id,
        sale_date,
        sum(sale_amount) as daily_sale
    from sales
    group by 1,2
),

avg_sale as (
    select
        store_id,
        avg(daily_sale) as avg_sale
    from daily_sale
    group by 1
),

dates as (
    select 
        d.store_id,
        d.sale_date
    from daily_sale d
    join avg_sale a
    on d.store_id = a.store_id
    where d.daily_sale > a.avg_sale
)

select 
store_id,
sale_date,
sum(daily_sale) over (partition by store_id order by sale_date) as cumulative_sales
from daily_sale
where exists (select 1 from dates where daily_sale.sale_date = dates.sale_date and daily_sale.store_id = dates.store_id);

-- Q8: List employees who earn more than their department average.
-- Tables: employees (employee_id,department_id, salary)
select 
e1.employee_id
from employees e1
where e1.salary > 

(select 
avg(e2.salary) as dept_avg
from employees e2
where e1.department_id = e2.department_id
group by e2.department_id);

-- Q9: identify products that have been sold but have no record in the products table and also calculate how many times each missing product has been sold.
-- tables: sales(product_id) products(product_id)
select 
product_id,
count(*)
from sales 
where product_id not in (select product_id from products where product_id is not null)
group by 1;

select 
product_id,
count(*)
from sales s
where not exists (select 1 from products p where p.product_id = s.product_id)
group by 1;

-- Q10:identify suppliers whose average delivery time is less than 2 days, but only consider deliveries with quantities greater than 100 units.
-- tables: deliveries(supplier_id, delivery_date, order_date, quantity)
select
supplier_id,
avg(datediff(delivery_date,order_date)) as avg_delivery_time
from deliveries
where quantity > 100
group by 1
having avg(datediff(delivery_date,order_date))< 2

-- Q11: Find customers who made no purchase in the last 6 months but made at least one purchase in the 6 months prior to that.
-- tables: customers(customer_id), Purchases(customer_id,purchase_date)

select 
    customer_id
from customers c
where not exists(
    select 1
    from purchases p 
    where c.customer_id = p.customer_id
    and p.purchase_date >= date_sub(current_date(), interval 6 month)
)
and exists (
    select 1
    from purchases p 
    where c.customer_id = p.customer_id
    and p.purchase_date >= date_sub(current_date(), interval 12 month) 
    and p.purchase_date < date_sub(current_date(), interval 6 month) 
)

-- Q12: Find the top 3 most frequent product combination bought together.
-- tables: order_detail(order_id,product_id)
with combination_count as (
select 
o1.product_id as product1,
o2.product_id as product2,
count(*) as combination_count
from order_detail o1 
join order_detail o2 
on o1.order_id = o2.order_id
and o1.product_id > o2.product_id
group by 1,2)

select product1,product2,combination_count
from combination_count
order by combination_count desc limit 3;

-- Q13: Calculate the moving average of sales for each product over a 7 day window
-- tables: sales(product_id,sale_amount,sale_date)
select
product_id,
avg(sale_amount) over (partition by product_id order by sale_date rows between 7 preceding and current row)
from sales; 

-- Q14: Rank stores by monthly sales performance.
-- Tables: sales(store_id,sale_amount,sale_date)
with monthly_sale as (
select 
store_id,
date_format(sale_date,'%Y%m') as sale_month,
sum(sale_amount) as monthly_sale
from sales
group by 1,2)

select 
store_id,
rank() over (partition by sale_month order by monthly_sale desc) as store_rank
from monthly_sale
order by store_rank, store_id;


-- Q15: Find customers who placed more than 50% of their orders in the last month.
-- Tables: orders(customer_id,order_id,order_date)


select 
o1.customer_id 
from orders o1
where o1.order_date >= date_sub(current_date(),interval 1 month)
group by 1
having count(o1.order_id) > 

(select
    0.5*count(o2.order_id) as order_count
from orders o2
where o1.customer_id = o2.customer_id
group by o2.customer_id
);

-- Bonus Challenge Question: Find consecutive login days for each user and identify streaks of at least 3 days.
-- logins(user_id, login_date)

with
group_nbr as (
select 
user_id,
login_date,
row_number()over(partition by user_id order by login_date) as rn,
login_date - (row_number()over(partition by user_id order by login_date)) as group_nbr
from logins)

select 
user_id,
min(login_date) as start_date,
max(login_date) as end_date,
count(*)
from group_nbr
group by user_id,group_nbr
having count(*) >= 3




