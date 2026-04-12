-- Q1:Identify customers who made purchases on exactly three different days in the last month
-- Tables: purchases(customer_id,purchase_date)

-- Q2: Find the top 2 highest-selling products for each category.
-- Tables: sales(product_id,sale_amount),products(product_id,category)

-- Q3: Detect anomalies where sales for a product are 50% lower than the average for that product
-- Tables: sales(product_id, sale_amount)

-- Q4: Find employees who have never been a manager and have worked in more than one department.
-- Tables: employees(employee_id,name,manager_id,department_id)

-- Q5:Caculate the median salary in each department
-- Tables: employees(employee_id, department_id, salary)

-- Q6: identify customers who purchased products from all available categories
-- tables: purchases(customer_id,product_id), products(product_id,category)

-- Q7: calculate the cumulative sales for each store, but only include dates where the daily sales exceeded the stores'average daily sales.
-- Tables:sales(store_id,sale_amount,sale_date)

-- Q8: List employees who earn more than their department average.
-- Tables: employees (employee_id,department_id, salary)

-- Q9: identify products that have been sold but have no record in the products table and also calculate how many times each missing product has been sold.
-- tables: sales(product_id) products(product_id)

-- Q10:identify suppliers whose average delivery time is less than 2 days, but only consider deliveries with quantities greater than 100 units.
-- tables: deliveries(supplier_id, delivery_date, order_date, quantity)

-- Q11: Find customers who made no purchase in the last 6 months but made at least one purchase in the 6 months prior to that.
-- tables: customers(customer_id), Purchases(customer_id,purchase_date)

-- Q12: Find the top 3 most frequent product combination bought together.
-- tables: order_detail(order_id,product_id)

-- Q13: Calculate the moving average of sales for each product over a 7 day window
-- tables: sales(product_id,sale_amount,sale_date)

-- Q14: Rank stores by monthly sales performance.
-- Tables: sales(store_id,sale_amount,sale_date)

-- Q15: Find customers who placed more than 50% of their orders in the last month.
-- Tables: orders(customer_id,order_id,order_date)




-- Q1:Identify customers who made purchases on exactly three different days in the last month
-- Tables: purchases(customer_id,purchase_date)
select 
    customer_id
from purchases
where purchase_date between date_sub(current_date(), interval 30 day) and current_date()
group by 1
having count(distinct date(purchase_date)) = 3;
-- Q2: Find the top 2 highest-selling products for each category.
-- Tables: sales(product_id,sale_amount),products(product_id,category)

with total_sales as (
    select 
        product_id,
        sum(sale_amount) as total_sales
    from sales
    group by 1
),

total_sales_rank as (
select 
t.product_id,
p.category,
t.total_sales,
row_number() over (partition by p.category order by t.total_sales desc) as rn 
from total_sales t 
join products p 
on t.product_id = p.product_id )

select 
    product_id,category
from total_sales_rank 
where rn < 3;

-- Q3: Detect anomalies where sales for a product are 50% lower than the average for that product
-- Tables: sales(product_id, sale_amount)


with avg_sales as (
select 
    product_id,
    avg(sale_amount)as avg_sales
from sales 
group by product_id
)

select s.product_id, s.sale_amount
from sales s
join avg_sales a 
on s.product_id = a.product_id
where s.sale_amount < a.avg_sales * (1-0.5);

-- Q4: Find employees who have never been a manager and have worked in more than one department.
-- Tables: employees(employee_id,name,manager_id,department_id)


select employee_id, name 
from employees 
where employee_id in (
        select employee_id
        from employees
        group by 1
        having count(distinct department_id) > 1
)
and employee_id not in (
    select manager_id
    from employees 
    where manager_id is not null
);

-- Q5:Caculate the median salary in each department
-- Tables: employees(employee_id, department_id, salary)

with department_info as (
select 
    employee_id,
    salary,
    department_id,
    count(employee_id) over(partition by department_id) as employee_count,
    row_number() over (partition by department_id order by salary) as rn 
from employees
)

select 
    department_id,
    avg(salary) as median_salary
from department_info
where 
rn in (ceil((employee_count+1)/2),floor((employee_count+1)/2))
group by 1
;

-- Q6: identify customers who purchased products from all available categories
-- tables: purchases(customer_id,product_id), products(product_id,category)
select 
pu.customer_id,
count(distinct po.category)
from purchases pu 
join products po 
on pu.product_id = po.product_id
group by 1
having count(distinct po.category) = (
    select count(distinct category)
    from products
);

-- Q7: calculate the cumulative sales for each store, but only include dates where the daily sales exceeded the stores'average daily sales.
-- Tables:sales(store_id,sale_amount,sale_date)
with daily_sales as (
    select 
        store_id,
        sale_date,
        sum(sale_amount) as daily_sales
    from sales
    group by 1,2

),
avg_sales as (
    select 
        store_id,
        avg(daily_sales) as avg_sales
    from daily_sales
    group by 1
),
dates_exceeded as (
    select
        d.store_id,
        d.sale_date,
        d.daily_sales
    from daily_sales d
    join avg_sales a 
    on d.store_id = a.store_id
    where d.daily_sales > a.avg_sales
)

select 
    store_id,
    sale_date,
    sum(daily_sales) over (partition by store_id order by sale_date) as cumulative_sales
from dates_exceeded
order by 1,2,3;

-- Q8: List employees who earn more than their department average.
-- Tables: employees (employee_id,department_id, salary)
with dept_avg as (
    select
    department_id,
    avg(salary) as dept_avg
    from employees
    group by department_id
)

select 
    e.employee_id
from employees e 
join dept_avg d 
on e.department_id = d.department_id
where e.salary > d.dept_avg;

-- Q9: identify products that have been sold but have no record in the products table and also calculate how many times each missing product has been sold.
-- tables: sales(product_id) products(product_id)
select 
product_id,
count(*)
from sales s
left join products p 
on s.product_id = p.product_id
where p.product_id is null
group by 1;

-- Q10:identify suppliers whose average delivery time is less than 2 days, but only consider deliveries with quantities greater than 100 units.
-- tables: deliveries(supplier_id, delivery_date, order_date, quantity)
select
supplier_id
from deliveries
where quantity > 100
group by 1
having avg(datediff(delivery_date,order_date)) < 2;

-- Q11: Find customers who made no purchase in the last 6 months but made at least one purchase in the 6 months prior to that.
-- tables: customers(customer_id), Purchases(customer_id,purchase_date)
select 
    customer_id
from customers
where customer_id not in(
     select customer_id 
     from purchases 
     where purchase_date between date_sub(current_date(), interval 6 month) and current_date() 
     )
     and customer_id in ( 
        select customer_id 
        from purchases
        where purchase_date between date_sub(current_date(), interval 12 month) and date_sub(current_date(), interval 6 month)        
     );
select 
    customer_id
from customers c
where not exists (
     select 1
     from purchases p
     where c.customer_id = p.customer_id
     and p.purchase_date >= date_sub(current_date(), interval 6 month)
     )
     and exists( 
        select 1
        from purchases p
        where c.customer_id = p.customer_id
        and p.purchase_date < date_sub(current_date(), interval 6 month) 
        and p.purchase_date >= date_sub(current_date(), interval 12 month)     
     );

-- Q12: Find the top 3 most frequent product combination bought together.
-- tables: order_detail(order_id,product_id)

select 
o1.product_id,
o2.product_id,
count(o1.order_id) as frequent_count

from order_detail o1
join order_detail o2
on o1.order_id = o2.order_id
where o1.product_id < o2.product_id
group by 1,2
order by frequent_count desc
limit 3;

-- Q13: Calculate the moving average of sales for each product over a 7 day window
-- tables: sales(product_id,sale_amount,sale_date)
select 
product_id,
avg(sale_amount) over (partition by product_id order by sale_date rows between 6 preceding and current row) as moving_avg
from sales;

-- Q14: Rank stores by monthly sales performance.
-- Tables: sales(store_id,sale_amount,sale_date)

with monthly_sale as (
select
store_id,
date_format(sale_date, '%Y%m') as sale_month,
sum(sale_amount) as monthly_sale
from sales
group by 1,2)

select 
store_id,
sale_month,
monthly_sale,
rank()over (partition by sale_month order by monthly_sale desc) as rank
from monthly_sale ;

-- Q15: Find customers who placed more than 50% of their orders in the last month.
-- Tables: orders(customer_id,order_id,order_date)
with last_month_order as (
select
customer_id,
count(order_id) as last_month_order_count
from orders
where order_date >= date_sub(current_date(), interval 1 month)
group by 1
)

select 
o.customer_id
from orders o 
join last_month_order l 
on o.customer_id = l.customer_id
group by 1
having l.last_month_order_count > 0.5 * count(order_id);
