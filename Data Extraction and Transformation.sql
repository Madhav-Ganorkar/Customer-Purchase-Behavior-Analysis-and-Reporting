Create Database Customers_Project;
use Customers_Project;

CREATE TABLE Customer_Purchase (
    TransactionID INT,
    CustomerID INT,
    CustomerName VARCHAR(100),
    ProductID INT,
    ProductName VARCHAR(100),
    ProductCategory VARCHAR(50),
    PurchaseQuantity INT,
    PurchasePrice DECIMAL(10,2),
    PurchaseDate DATE,
    Country VARCHAR(50));
    
-- Just confirm that data exists here:
SELECT * FROM Customer_Purchase LIMIT 10;


-- a. Customer Table with Surrogate Key
CREATE TABLE Customers (
    CustomerKey INT AUTO_INCREMENT PRIMARY KEY,
    CustomerID INT,
    CustomerName VARCHAR(100),
    Country VARCHAR(50));

-- b. Product Table with Surrogate Key
CREATE TABLE Products (
    ProductKey INT AUTO_INCREMENT PRIMARY KEY,
    ProductID INT,
    ProductName VARCHAR(100),
    ProductCategory VARCHAR(50));

-- c. Transactions Table referencing surrogate keys
CREATE TABLE Transactions (
    TransactionID INT PRIMARY KEY,
    CustomerKey INT,
    ProductKey INT,
    PurchaseQuantity INT,
    PurchasePrice DECIMAL(10,2),
    PurchaseDate DATE,
    FOREIGN KEY (CustomerKey) REFERENCES Customers(CustomerKey),
    FOREIGN KEY (ProductKey) REFERENCES Products(ProductKey));
    

-- Insert distinct Customer rows
INSERT INTO Customers (CustomerID, CustomerName, Country)
SELECT DISTINCT CustomerID, CustomerName, Country
FROM Customer_Purchase;

-- Insert distinct Product rows
INSERT INTO Products (ProductID, ProductName, ProductCategory)
SELECT DISTINCT ProductID, ProductName, ProductCategory
FROM Customer_Purchase;

-- Insert distinct Transaction rows
INSERT INTO Transactions (TransactionID, CustomerKey, ProductKey, PurchaseQuantity, PurchasePrice, PurchaseDate)
SELECT 
    cp.TransactionID,
    c.CustomerKey,
    p.ProductKey,
    cp.PurchaseQuantity,
    cp.PurchasePrice,
    cp.PurchaseDate
FROM Customer_Purchase cp
JOIN Customers as c 
    ON cp.CustomerID = c.CustomerID 
    AND cp.CustomerName = c.CustomerName 
    AND cp.Country = c.Country
JOIN Products as p 
    ON cp.ProductID = p.ProductID 
    AND cp.ProductName = p.ProductName 
    AND cp.ProductCategory = p.ProductCategory;


-- 1. Total Purchases (Quantity) per Customer
SELECT c.CustomerID, c.CustomerName, SUM(t.PurchaseQuantity) as Total_Purchases
FROM Customers as c
JOIN Transactions as t on c.CustomerKey = t.CustomerKey
GROUP BY c.CustomerID, c.CustomerName
ORDER BY Total_Purchases DESC;


-- 2. Total Sales (Revenue) per Product
SELECT p.ProductID, ProductName, SUM(t.PurchaseQuantity * t.PurchasePrice) as Total_Sales 
FROM Products as p
JOIN Transactions as t on p.ProductKey = t.ProductKey
GROUP BY p.ProductID, ProductName
ORDER BY Total_Sales DESC;


-- 3. Total Sales per Country
SELECT c.Country, SUM(t.PurchaseQuantity * t.PurchasePrice) as Total_Sales
FROM Customers as c
JOIN Transactions as t on c.CustomerKey = t.CustomerKey
GROUP BY c.Country
ORDER BY Total_Sales DESC;


-- 4. Top Selling Products in 2023
SELECT p.ProductID, p.ProductName, SUM(t.PurchaseQuantity) as Total_Qty_Sale
FROM Products as p 
JOIN Transactions as t on p.ProductKey = t.ProductKey
WHERE YEAR(t.PurchaseDate) = 2023
GROUP BY p.ProductID, p.ProductName
ORDER BY Total_Qty_Sale DESC;


-- 5. High-Revenue Products where Purchase Quantity > 2 and Revenue > 5,000
SELECT p.ProductID, ProductName, SUM(t.PurchaseQuantity * t.PurchasePrice) as Total_Revenue 
FROM Products as p
JOIN Transactions as t on p.ProductKey = t.ProductKey
WHERE PurchaseQuantity > 2
GROUP BY p.ProductID, ProductName
HAVING SUM(t.PurchaseQuantity * t.PurchasePrice) > 5000
ORDER BY Total_Revenue DESC;






