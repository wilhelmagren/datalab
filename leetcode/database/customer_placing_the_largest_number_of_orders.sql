SELECT customer_number FROM Orders
GROUP BY customer_number
ORDER BY COUNT(order_number) DESC lIMIT 1;
