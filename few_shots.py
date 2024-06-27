few_shots = [
    {'Question': "to calculate the total sales amount for one product (considering quantity, list price, and discount)",
     'SQLQuery': """SELECT  oi.product_id, product_name, quantity as unit_sold, oi.list_price, discount, 
         oi.list_price * (1 - discount) AS discounted_price, SUM(SUM((oi.list_price * (1 -discount))*quantity)) 
         OVER (PARTITION BY oi.product_id)  AS total_sales_per_product FROM  order_items as oi JOIN products as p 
         ON oi.product_id = p.product_id GROUP BY 1 ORDER BY 1,2,3 ASC limit 1""",
     'SQLResult': "Result of the SQL query",
     'Answer': "2 Ritchey Timberwolf Frameset - 2016 2 749.99 0.10 674.9910 78898.9480"},

    {'Question': "find the top 5 customers who have spent the most money",
     'SQLQuery': """SELECT c.customer_id, first_name ||" "|| last_name as customer_name, SUM(SUM((oi.list_price * (1 - discount))*quantity)) 
     OVER (PARTITION BY c.customer_id) AS total_spending FROM customers c INNER JOIN orders o ON o.customer_id = c.customer_id 
     INNER JOIN order_items oi ON oi.order_id = o.order_id GROUP BY 1 ORDER BY 3 DESC LIMIT 5;""",
     'SQLResult': "Result of the SQL query",
     'Answer': """94 0 34807.9392 ,
                10 0 33634.2604 ,
                75 0 32803.0062 ,
                6 0 32675.0725 ,
                16 0 31925.8857"""},

    {'Question': " Which 2 products should be kept available because they are popular",
     'SQLQuery': """SELECT oi.product_id, product_name, oi.list_price FROM order_items as oi 
         JOIN products as p ON oi.product_id = p.product_id GROUP BY 1 ORDER BY 3 DESC LIMIT 2""",
     'SQLResult': "Result of the SQL query",
     'Answer': """155 Trek Domane SLR 9 Disc - 2018 11999.99 ,
                    149 Trek Domane SLR 8 Disc - 2018 7499.99"""},

    {'Question': " Write a query to aggregate the total sales, average order value, and maximum order value for customers in each city and state.",
     'SQLQuery': """SELECT c.city, c.state, COUNT(c.customer_id) AS customer_count, SUM(quantity * oi.list_price * (1 - oi.discount)) AS total_sales, 
        AVG(quantity * oi.list_price * (1 - oi.discount)) AS average_order_value, MAX(quantity * oi.list_price * (1 - oi.discount)) AS max_order_value 
        FROM customers c JOIN orders o ON c.customer_id = o.customer_id INNER JOIN order_items oi ON o.order_id = oi.order_id GROUP BY 1 
        ORDER BY total_sales DESC LIMIT 2""",
     'SQLResult': "Result of the SQL query",
     'Answer': """Mount Vernon NY 60 105563.3335 1759.38889167 9499.9810 ,
                    Ballston Spa NY 52 98619.7500 1896.53365385 11159.981"""},

    {'Question': " Write a query to find the total quantity of each product available in all stores. first two lines",
     'SQLQuery': """SELECT s.product_id, p.product_name, SUM(s.quantity) as total_q_in_all_stores FROM stocks as s INNER JOIN products as p ON 
        p.product_id = s.product_id GROUP BY s.product_id;LIMIT 2""",
     'SQLResult': "Result of the SQL query",
     'Answer': """Trek 820 - 2016 55 ,
                Ritchey Timberwolf Frameset - 2016 45"""}


]