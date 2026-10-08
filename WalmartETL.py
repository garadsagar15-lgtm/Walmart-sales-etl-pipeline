import mysql.connector

import csv
from datetime import datetime
import mysql.connector

CSV_FILE = r"C:\Users\SAGAR\Downloads\Walmart_Sales.csv"

# 1. Connect to MySQL server and create the database if needed
con = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234"
)
cursor = con.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS etl")
cursor.close()
con.close()

# 2. Connect to the etl database
con = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="ETL"
)
cursor = con.cursor()

print("Connected to MySQL")

# =========================================================
# CREATE THE WALMART SALES TABLE
# =========================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS Walmart_Sales (
    Store INT NOT NULL,
    `Date` DATE NOT NULL,
    Weekly_Sales DECIMAL(14, 2),
    Holiday_Flag TINYINT,
    Temperature DECIMAL(8, 2),
    Fuel_Price DECIMAL(8, 3),
    CPI DECIMAL(12, 7),
    Unemployment DECIMAL(8, 3),
    PRIMARY KEY (Store, `Date`)
)
""")

# =========================================================
# LOAD CSV DATA INTO MYSQL
# =========================================================

with open(CSV_FILE, mode="r", newline="", encoding="utf-8-sig") as file:
    reader = csv.DictReader(file)

    rows = []
    for row in reader:
        rows.append((
            int(row["Store"]),
            datetime.strptime(row["Date"], "%d-%m-%Y").date(),
            float(row["Weekly_Sales"]),
            int(row["Holiday_Flag"]),
            float(row["Temperature"]),
            float(row["Fuel_Price"]),
            float(row["CPI"]),
            float(row["Unemployment"])
        ))

cursor.executemany("""
    INSERT INTO Walmart_Sales
    (Store, `Date`, Weekly_Sales, Holiday_Flag, Temperature,
     Fuel_Price, CPI, Unemployment)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
        Weekly_Sales = VALUES(Weekly_Sales),
        Holiday_Flag = VALUES(Holiday_Flag),
        Temperature = VALUES(Temperature),
        Fuel_Price = VALUES(Fuel_Price),
        CPI = VALUES(CPI),
        Unemployment = VALUES(Unemployment)
""", rows)

con.commit()
print("Walmart sales data loaded successfully")


# =========================================================
# 1. SELECT ALL DATA
# =========================================================

cursor.execute("DROP TABLE IF EXISTS Backup_All")
cursor.execute("""
CREATE TABLE Backup_All AS
SELECT *
FROM Walmart_Sales
""")

print("1. All data extracted")


# =========================================================
# 2. WHERE - FILTER DATA
# =========================================================

cursor.execute("DROP TABLE IF EXISTS Backup_High_Sales")
cursor.execute("""
CREATE TABLE Backup_High_Sales AS
SELECT *
FROM Walmart_Sales
WHERE Weekly_Sales > 1000000
""")

print("2. Filtered data extracted")


# =========================================================
# 3. SELECT SPECIFIC COLUMNS
# =========================================================

cursor.execute("DROP TABLE IF EXISTS Backup_Selected_Columns")
cursor.execute("""
CREATE TABLE Backup_Selected_Columns AS
SELECT Store, `Date`, Weekly_Sales
FROM Walmart_Sales
""")

print("3. Selected columns extracted")


# =========================================================
# 4. DISTINCT
# =========================================================

cursor.execute("DROP TABLE IF EXISTS Backup_Stores")
cursor.execute("""
CREATE TABLE Backup_Stores AS
SELECT DISTINCT Store
FROM Walmart_Sales
""")

print("4. Distinct stores extracted")


# =========================================================
# 5. ORDER BY
# =========================================================

cursor.execute("DROP TABLE IF EXISTS Backup_Sales_Sorted")
cursor.execute("""
CREATE TABLE Backup_Sales_Sorted AS
SELECT *
FROM Walmart_Sales
ORDER BY Weekly_Sales DESC
""")

print("5. Sorted data extracted")


# =========================================================
# 6. GROUP BY + COUNT
# =========================================================

cursor.execute("DROP TABLE IF EXISTS Backup_Store_Count")
cursor.execute("""
CREATE TABLE Backup_Store_Count AS
SELECT Store, COUNT(*) AS Week_Count
FROM Walmart_Sales
GROUP BY Store
""")

print("6. Store count extracted")


# =========================================================
# 7. GROUP BY + AVG
# =========================================================

cursor.execute("DROP TABLE IF EXISTS Backup_Average_Sales")
cursor.execute("""
CREATE TABLE Backup_Average_Sales AS
SELECT Store, AVG(Weekly_Sales) AS Average_Weekly_Sales
FROM Walmart_Sales
GROUP BY Store
""")

print("7. Average sales extracted")


# =========================================================
# 8. HAVING
# =========================================================

cursor.execute("DROP TABLE IF EXISTS Backup_High_Average_Sales")
cursor.execute("""
CREATE TABLE Backup_High_Average_Sales AS
SELECT Store, AVG(Weekly_Sales) AS Average_Weekly_Sales
FROM Walmart_Sales
GROUP BY Store
HAVING AVG(Weekly_Sales) > 1000000
""")

print("8. HAVING result extracted")


# =========================================================
# 9. BETWEEN
# =========================================================

cursor.execute("DROP TABLE IF EXISTS Backup_Sales_Range")
cursor.execute("""
CREATE TABLE Backup_Sales_Range AS
SELECT *
FROM Walmart_Sales
WHERE Weekly_Sales BETWEEN 500000 AND 1500000
""")

print("9. BETWEEN result extracted")


# =========================================================
# 10. IN
# =========================================================

cursor.execute("DROP TABLE IF EXISTS Backup_Holiday_Sales")
cursor.execute("""
CREATE TABLE Backup_Holiday_Sales AS
SELECT *
FROM Walmart_Sales
WHERE Holiday_Flag IN (0, 1)
""")

print("10. IN result extracted")


# =========================================================
# 11. LIKE
# =========================================================

cursor.execute("DROP TABLE IF EXISTS Backup_Store_Search")
cursor.execute("""
CREATE TABLE Backup_Store_Search AS
SELECT *
FROM Walmart_Sales
WHERE CAST(Store AS CHAR) LIKE '1%'
""")

print("11. LIKE result extracted")


# =========================================================
# 12. CASE
# =========================================================

cursor.execute("DROP TABLE IF EXISTS Backup_Sales_Category")
cursor.execute("""
CREATE TABLE Backup_Sales_Category AS
SELECT
    Store,
    `Date`,
    Weekly_Sales,
    CASE
        WHEN Weekly_Sales >= 1500000 THEN 'High'
        WHEN Weekly_Sales >= 500000 THEN 'Medium'
        ELSE 'Low'
    END AS Sales_Category
FROM Walmart_Sales
""")

print("12. CASE result extracted")


# =========================================================
# SAVE ALL CHANGES
# =========================================================

con.commit()

print("\nETL completed successfully!")


# =========================================================
# SHOW CREATED TABLES
# =========================================================

cursor.execute("SHOW TABLES")

print("\nTables in database:")

for table in cursor.fetchall():
    print(table[0])


# =========================================================
# CLOSE CONNECTION
# =========================================================

cursor.close()
con.close()

print("\nMySQL connection closed")