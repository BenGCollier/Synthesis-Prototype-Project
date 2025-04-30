SELECT COUNT(*) 
FROM Customers 
WHERE City LIKE '%s';

SELECT ROUND(AVG(Price), 2) 
FROM Products;

SELECT *
FROM Suppliers
ORDER BY City DESC;

SELECT Address
FROM Suppliers
ORDER BY City DESC
LIMIT 1 OFFSET 9;

SELECT CustomerID
FROM Customers
ORDER BY Country, CustomerName
LIMIT 1 OFFSET 4;

SELECT COUNT(DISTINCT City) 
FROM Suppliers;

SELECT * FROM Customers Limit 20;

SELECT COUNT(DISTINCT ProductID) 
FROM OrderDetails;

SELECT COUNT(*)
FROM Orders
WHERE EmployeeID = 5;

SELECT COUNT(*)
FROM Customers
WHERE City = 'Paris';

SELECT COUNT(*)
FROM OrderDetails
WHERE ProductID = 11 AND Quantity > 5;

SELECT COUNT(*)
FROM Customers
WHERE Country IN ('Germany', 'Mexico');

SELECT COUNT(*)
FROM Customers
WHERE (City = 'Berlin' AND Country = 'Germany')
   OR (City = 'London' AND Country = 'UK');
   
SELECT COUNT(*)
FROM OrderDetails
WHERE Quantity BETWEEN 30 AND 40;

SELECT COUNT(*)
FROM Customers
WHERE ContactName LIKE 'M%';

SELECT ROUND(AVG(Quantity), 1) AS AverageQuantity
FROM OrderDetails;

SELECT MAX(Quantity) AS MaxQuantity
FROM OrderDetails;

SELECT ROUND(MIN(Price), 2) AS MinPrice
FROM Products;

SELECT SUM(Quantity) AS TotalQuantity
FROM OrderDetails;

SELECT CustomerID, CustomerName, Country
FROM Customers
ORDER BY Country
LIMIT 1 OFFSET 4;

SELECT *
FROM Suppliers
ORDER BY Country, SupplierName
LIMIT 1 OFFSET 8;

SELECT Country, COUNT(SupplierID) AS SupplierCount
FROM Suppliers
GROUP BY Country
ORDER BY Country;

SELECT Country, COUNT(SupplierID) AS CountOfSuppliers
FROM Suppliers
GROUP BY Country
HAVING COUNT(SupplierID) >= 3
ORDER BY Country;
