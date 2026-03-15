SELECT
    country,
    SUM(sales) AS total_sales
FROM raw.customer_data
GROUP BY country
ORDER BY total_sales DESC;
