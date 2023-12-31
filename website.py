import pandas as pd
import streamlit as st
import psycopg2

from sqlalchemy import create_engine
conn = psycopg2.connect(host="localhost", port = 5432, database="superstore", user="postgres", password="9030")
cur = conn.cursor()

engine = create_engine("postgresql://postgres:9030@localhost:5432/superstore")
st.write("DMQL Project 2023")

st.write("\n Query1: SELECT * FROM product_details;")

df = pd.read_sql("SELECT * FROM product_details;", conn)
st.write(df)


st.write("\n Query2: Insertion")
df1 = pd.read_sql("""
    INSERT INTO Product_Details (Product_ID, Product_Name, Category, Sub_Category, unit_price, Sales, Row_ID)
    VALUES ('TEC-CO-5800', 'Lenovo IdeaPad 5', 'Technology', 'Computers', 1000, 500000, 324);
    SELECT * FROM Product_Details WHERE Product_ID = 'TEC-CO-5800';
""", conn)
st.write(df1)



st.write("\n Query: Deletion")
df2 = pd.read_sql("""
   DELETE FROM Product_Details
WHERE Product_ID = 'TEC-CO-5800';

select * from Product_Details where Product_ID = 'TEC-CO-5800';

""", conn)
st.write(df2)



st.write("\n Query: Insertion")
df3 = pd.read_sql("""
   INSERT INTO Customer_Details (customer_name,customer_id,country,state,region,city,phone_number,email_id)
VALUES ('Rakshitha',	'CV-0000000',	'United States',	'NewYork',	'Central US'	,'Buffalo',	'500-101-9012',	'rakshitha@example.com');

select * from Customer_Details where Customer_ID = 'CV-0000000';


""", conn)
st.write(df3)





st.write("\n Query: Deleting Operation")
df4 = pd.read_sql("""
   DELETE FROM Customer_Details where Customer_ID = 'CV-0000000';

select * from Customer_Details where Customer_ID = 'CV-0000000';



""", conn)
st.write(df4)




st.write("\n Query: Update Operation")
df5 = pd.read_sql("""
select order_date from order_details where order_id = 'IN-2015-VG2180558-42273';

UPDATE order_details
SET order_date = '2015-09-24'
WHERE order_id = 'IN-2015-VG2180558-42273';


select * from order_Details where order_id = 'IN-2015-VG2180558-42273';


""", conn)
st.write(df5)




st.write("\n Query: Update ")
df6 = pd.read_sql("""
UPDATE order_details
SET order_date = '2012-12-27'
WHERE order_id = 'SA-2012-MM7260110-41269';

select * from order_details where order_id = 'SA-2012-MM7260110-41269';
""", conn)
st.write(df6)



st.write("\n Query: Functions and trigers ::  Update the unit price of a product in the Product_Details table:")
df7 = pd.read_sql("""
CREATE OR REPLACE FUNCTION update_sales()
RETURNS TRIGGER AS
$$
BEGIN
    UPDATE Product_Details
    SET Sales = NEW.unit_price * (
        SELECT SUM(od.quantity) 
        FROM Order_Details od 
        WHERE od.product_id = NEW.product_id
    )
    WHERE Product_ID = NEW.Product_ID;
    RETURN NEW;
END;
$$
LANGUAGE plpgsql;


UPDATE Product_Details SET unit_price = 625.00 WHERE Product_ID = 'TEC-PH-5356';

select * from Product_Details where Product_ID = 'TEC-PH-5356';

""", conn)
st.write(df7)



st.write("\n Query: Joins:: Select the product details and the corresponding customer details for a specific order. ")
df8 = pd.read_sql("""
SELECT p.Product_Name, p.Category, c.customer_name, c.Country, c.state
FROM Product_Details p
INNER JOIN Order_Details o ON p.Product_ID = o.Product_ID
INNER JOIN Customer_Details c ON o.Customer_ID = c.Customer_ID
WHERE o.Order_ID = 'IN-2012-AB1010558-41270';
""", conn)
st.write(df8)



st.write("\n Query: Joins:: This query retrieves the total sales and last shipment date for each customer in the USA who has ordered more than 5 different products. ")
df9 = pd.read_sql("""
SELECT c.customer_name, c.Country, c.state, 
       SUM(b.Sales) AS Total_Sales, 
       MAX(s.Ship_Date) AS Last_Shipment_Date
FROM Customer_Details c
INNER JOIN Order_Details o ON c.Customer_ID = o.Customer_ID
INNER JOIN Billing_Details b ON o.Order_ID = b.Order_ID
INNER JOIN Shipping_Details s ON o.Order_ID = s.Order_ID
WHERE c.Country = 'United States'
GROUP BY c.customer_name, c.Country, c.state
HAVING COUNT(DISTINCT o.Product_ID) > 5
ORDER BY Total_Sales DESC;
""", conn)
st.write(df9)



st.write("\n Query: Create a view that shows the total sales for each product by year: ")
df10 = pd.read_sql("""
CREATE VIEW product_sales_by_year AS
SELECT pd.product_id, pd.product_name, DATE_TRUNC('year', od.order_date) AS year, SUM(bd.sales) AS total_sales
FROM product_details pd
INNER JOIN order_details od ON pd.product_id = od.product_id
INNER JOIN billing_details bd ON od.order_id = bd.order_id
GROUP BY pd.product_id, pd.product_name, DATE_TRUNC('year', od.order_date);

SELECT * FROM product_sales_by_year;
""", conn)
st.write(df10)



st.write("\n Query:  Create a trigger that automatically inserts a new record into the Shipping_Details table whenever a new order is inserted into the Order_Details table")
df11 = pd.read_sql("""
CREATE OR REPLACE FUNCTION insert_shipping_details()
RETURNS TRIGGER AS $$
BEGIN
  -- Try to update the existing record with the new values
  UPDATE Shipping_Details
  SET Order_Date = NEW.Order_Date,
      Order_Priority = NEW.Order_Priority,
      Ship_Mode = NEW.Ship_Mode,
      Country = (SELECT Country FROM Customer_Details WHERE Customer_ID = NEW.Customer_ID),
      State = (SELECT State FROM Customer_Details WHERE Customer_ID = NEW.Customer_ID),
      Region = (SELECT Region FROM Customer_Details WHERE Customer_ID = NEW.Customer_ID),
      City = (SELECT City FROM Customer_Details WHERE Customer_ID = NEW.Customer_ID)
  WHERE Order_ID = NEW.Order_ID;
  
  
  -- If no record was updated, insert a new one
  IF NOT FOUND THEN
    INSERT INTO Shipping_Details (Order_ID, Order_Date, Order_Priority, Ship_Mode, Country, State, Region, City)
    SELECT NEW.Order_ID, NEW.Order_Date, NEW.Order_Priority, NEW.Ship_Mode, c.Country, c.State, c.Region, c.City
    FROM Customer_Details c
    WHERE c.Customer_ID = NEW.Customer_ID;
  END IF;
  
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;
select * from order_details;

INSERT INTO Order_Details (Order_ID, Order_Date,customer_id,ship_mode,product_id,quantity,category,order_priority)
VALUES ('SA-2012-MM7260110-41269',	'2015-12-31',	'Fe-3512840',	'Second Class',	'TEC-PH-3807',	4	,'Technology',	'Critical');

select * from shipping_details where order_id='SA-2012-MM7260110-41269';

""", conn)
st.write(df11)






st.write("\n Query: Procedure to calculate the total revenue generated by a customer in a particular year")
df12 = pd.read_sql("""
CREATE OR REPLACE PROCEDURE calculate_customer_revenue(
    IN customer_name varchar(255),
    IN year int,
    OUT revenue double precision
)
AS $$
BEGIN
    SELECT SUM(bd.Sales) INTO revenue
    FROM Order_Details od
    JOIN Billing_Details bd ON od.Order_ID = bd.Order_ID
    JOIN Customer_Details cd ON od.Customer_ID = cd.Customer_ID
    WHERE cd.Customer_Name = calculate_customer_revenue.customer_name
    AND extract(year from od.Order_Date) = year;
END;
$$ LANGUAGE plpgsql;


DO $$
DECLARE
    v_revenue double precision;
BEGIN
    CALL calculate_customer_revenue('Stacy Cruz', 2014, v_revenue);
    RAISE NOTICE 'Revenue for Stacy Cruz in 2014: %', v_revenue;
END $$;


""", conn)
st.write(df12)





st.write("\n Query: Find the top 5 customers who have the highest number of orders, along with the average order amount:")
df13 = pd.read_sql("""
SELECT 
  cd.customer_name, COUNT(DISTINCT od.order_id) AS num_orders, AVG(bd.quantity * pd.unit_price) AS avg_order_amount
FROM 
  billing_details bd 
  JOIN order_details od ON bd.order_id = od.order_id 
  JOIN customer_details cd ON od.customer_id = cd.customer_id 
  JOIN product_details pd ON od.product_id = pd.product_id 
GROUP BY 
  cd.customer_name 
ORDER BY 
  num_orders DESC 
LIMIT 
  5;

""", conn)
st.write(df13)




st.write("\n Query: Retrieve the top 5 customers who have spent the most amount of money on purchases:")
df14 = pd.read_sql("""
SELECT customer_details.customer_name, SUM(billing_details.sales) AS total_sales
FROM customer_details
INNER JOIN order_details ON customer_details.customer_id = order_details.customer_id
INNER JOIN billing_details ON order_details.order_id = billing_details.order_id
GROUP BY customer_details.customer_name
HAVING SUM(billing_details.sales) > 0
ORDER BY total_sales DESC
LIMIT 5;

""", conn)
st.write(df14)
























