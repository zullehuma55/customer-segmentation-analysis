/* 1. Segment Distribution*/

SELECT Segment,
       COUNT(*) AS Customer_Count
FROM customer_segments
GROUP BY Segment
ORDER BY Customer_Count DESC;

/* 2. Average Income by Segment */

SELECT Segment,
       ROUND(AVG(`Annual Income (k$)`),2) AS Avg_Income
FROM customer_segments
GROUP BY Segment
ORDER BY Avg_Income DESC;

/* 3. Average Spending Score by Segment */

SELECT Segment,
       ROUND(AVG(`Spending Score (1-100)`),2) AS Avg_Spending
FROM customer_segments
GROUP BY Segment
ORDER BY Avg_Spending DESC;

/* 4. Gender-wise Segment Analysis */
SELECT Gender,
       Segment,
       COUNT(*) AS Customers
FROM customer_segments
GROUP BY Gender, Segment
ORDER BY Gender, Customers DESC;

/* 5. Age Group Analysis */
SELECT `Age Group`,
       Segment,
       COUNT(*) AS Customers
FROM customer_segments
GROUP BY `Age Group`, Segment;

/* 6. Top Revenue-Contributing Segments */
SELECT Segment,
       SUM(`Annual Income (k$)`) AS Total_Income
FROM customer_segments
GROUP BY Segment
ORDER BY Total_Income DESC;

/* 7. High Income but Low Spending Customers */
SELECT CustomerID,
       Gender,
       Age,
       `Annual Income (k$)`,
       `Spending Score (1-100)`
FROM customer_segments
WHERE `Annual Income (k$)` > 70
AND `Spending Score (1-100)` < 40;
