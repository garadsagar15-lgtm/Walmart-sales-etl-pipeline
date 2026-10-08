# Walmart Sales ETL Pipeline

A Python and MySQL ETL project that imports Walmart weekly sales data from a CSV file, prepares it for database storage, and creates 12 analysis tables with SQL. The pipeline demonstrates practical ETL steps alongside common SQL operations such as filtering, sorting, grouping, aggregation, and conditional categorization.

## Workflow

![Walmart Sales ETL workflow]("C:\Users\SAGAR\Downloads\Walmart.jpg")

The workflow diagram is saved as `Walmart_Sales_ETL_Workflow.svg` in this repository. If you store it in another folder, update the image path above.

## Project Overview

- **Source:** `Walmart_Sales.csv`
- **Language:** Python
- **Database:** MySQL (`etl`)
- **Connector:** `mysql-connector-python`
- **Main table:** `Walmart_Sales`
- **Analysis outputs:** 12 `Backup_*` tables

The CSV contains store and week level data: store number, date, weekly sales, holiday flag, temperature, fuel price, CPI, and unemployment.

## ETL Steps

1. Connect to the MySQL server and create the `etl` database if needed.
2. Read the CSV with Python's `csv` module.
3. Parse dates and convert CSV fields to numeric types.
4. Create the `Walmart_Sales` table and load the rows.
5. Create 12 analysis tables using SQL queries.
6. Commit changes, display database tables, and close the connection.

The analysis tables demonstrate:

1. Select all rows — `Backup_All`
2. Filter high weekly sales — `Backup_High_Sales`
3. Select specific columns — `Backup_Selected_Columns`
4. Select distinct stores — `Backup_Stores`
5. Sort by weekly sales — `Backup_Sales_Sorted`
6. Count weeks by store — `Backup_Store_Count`
7. Average weekly sales by store — `Backup_Average_Sales`
8. Filter store averages with `HAVING` — `Backup_High_Average_Sales`
9. Filter sales with `BETWEEN` — `Backup_Sales_Range`
10. Filter holiday flag values with `IN` — `Backup_Holiday_Sales`
11. Search store numbers with `LIKE` — `Backup_Store_Search`
12. Categorize sales with `CASE` — `Backup_Sales_Category`

## Requirements

- Python 3
- MySQL Server
- `mysql-connector-python`

Install the Python dependency:

```bash
pip install mysql-connector-python
```

## Configuration

Update the CSV path and MySQL connection settings in the Python script before running it:

```python
CSV_FILE = r"C:\path\to\Walmart_Sales.csv"

con = mysql.connector.connect(
    host="localhost",
    user="root",
    password="YOUR_MYSQL_PASSWORD",
    database="etl"
)
```

Use your own MySQL password. Avoid committing real credentials to a public repository; an environment variable is a safer option.

## Run the Pipeline

Save the ETL script in the repository (for example, as `walmart_sales_etl.py`), make sure MySQL Server is running, then run:

```bash
python walmart_sales_etl.py
```

The script expects dates in the CSV to use `DD-MM-YYYY` format. It uses `(Store, Date)` as the primary key and updates matching records when the pipeline is run again.

## Screenshots

Add your screenshots at these paths, or change the paths below to match your repository:

### Python ETL code

![Python ETL code screenshot](screenshots/python_code.png)

### MySQL Workbench results

![MySQL Workbench screenshot](screenshots/mysql_workbench.png)

Expected screenshot files:

```text
screenshots/python_code.png
screenshots/mysql_workbench.png
```

