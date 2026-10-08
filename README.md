# Walmart Sales ETL Pipeline with Python and MySQL

A beginner-friendly ETL workflow that uses Python and MySQL to extract Walmart weekly sales data from a CSV file, prepare and load it into a database, and create 12 tables for analysis.

## Overview

The pipeline uses Python's built-in `csv` module and `mysql-connector-python` to read `Walmart_Sales.csv`, parse the dates and numeric fields, and load the rows into the MySQL `Walmart_Sales` table. It then runs SQL queries to create 12 derived tables demonstrating common filtering, selection, sorting, grouping, aggregation, and categorization operations.

### ETL workflow

1. **Extract** Walmart sales records from `Walmart_Sales.csv`.
2. **Transform** the CSV values by parsing dates and converting fields to numeric types.
3. **Load** the data into the MySQL `Walmart_Sales` table.
4. **Analyze** the loaded data with SQL and save each result in a separate table.

## Tables created

| Table | Example operation |
|---|---|
| `Backup_All` | Copy all Walmart sales rows |
| `Backup_High_Sales` | Filter weeks with sales above 1,000,000 |
| `Backup_Selected_Columns` | Keep Store, Date, and Weekly_Sales |
| `Backup_Stores` | Select distinct store numbers |
| `Backup_Sales_Sorted` | Sort rows by weekly sales descending |
| `Backup_Store_Count` | Count weekly records by store |
| `Backup_Average_Sales` | Calculate average weekly sales by store |
| `Backup_High_Average_Sales` | Keep stores with average weekly sales above 1,000,000 |
| `Backup_Sales_Range` | Filter sales between 500,000 and 1,500,000 |
| `Backup_Holiday_Sales` | Select rows with Holiday_Flag 0 or 1 |
| `Backup_Store_Search` | Find store numbers beginning with 1 using `LIKE` |
| `Backup_Sales_Category` | Assign High, Medium, or Low sales categories with `CASE` |

> The sales thresholds and category boundaries are example values and can be adjusted for your analysis.

## Screenshots

### ETL workflow

![Walmart Sales ETL workflow](Walmart_Sales_ETL_Workflow.svg)

### Python ETL code

![Python ETL code screenshot](assets/python-code.png)

### MySQL Workbench results

![MySQL Workbench showing the Walmart sales tables](assets/mysql-workbench.png)

Add the Python code and Workbench screenshots to the repository at `assets/python-code.png` and `assets/mysql-workbench.png`, or update the image links above to match your filenames. The workflow diagram is included as `Walmart_Sales_ETL_Workflow.svg`.

## Requirements

- Python 3
- MySQL Server
- MySQL Workbench (optional, for browsing tables and query results)
- Python package: `mysql-connector-python`

Install the connector:

```bash
python -m pip install mysql-connector-python
```

## Configure the database connection

Update the CSV path and MySQL connection settings in the Python script. Do not commit your real database password to Git. For example, read connection details from environment variables:

```python
import os
import mysql.connector

connection = mysql.connector.connect(
    host=os.getenv("MYSQL_HOST", "localhost"),
    user=os.getenv("MYSQL_USER", "root"),
    password=os.getenv("MYSQL_PASSWORD"),
    database=os.getenv("MYSQL_DATABASE", "etl"),
)
```

Set `MYSQL_USER` and `MYSQL_PASSWORD` in your local environment before running the script. Make sure the MySQL account can create and write tables. Also update the script's CSV path to the location of `Walmart_Sales.csv` on your computer.

## Run

1. Start MySQL Server.
2. Place `Walmart_Sales.csv` at the configured path.
3. Install the Python dependency.
4. Set the database connection environment variables and CSV path.
5. Run the ETL script from the repository root (replace the filename if needed):

   ```bash
   python walmart_sales_etl.py
   ```

6. Refresh the schema in MySQL Workbench and inspect the `Walmart_Sales` and `Backup_*` tables.

The CSV dates are expected in `DD-MM-YYYY` format. The main table uses `(Store, Date)` as its primary key; matching rows are updated when the script runs again. The script drops and recreates each `Backup_*` table to refresh its results.

## License

No license has been selected for this project. Before publishing it or granting others permission to reuse it, choose and add a license that reflects your intended permissions.

