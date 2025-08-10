# Imorting all necessary libraries
import pandas as pd
from sqlalchemy import create_engine


# MySQL credentials
username = "root"               # MySQL username
password = "8898"               # MySQL password 
host = "localhost"              # Her my MySQL sever running on localhost
port = 3306                     # MySQL default port
database = "Customers_Project"  # Database name


# Create database connection
engine = create_engine(f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}")


# Test connection - show all tables
try:
    df = pd.read_sql("SHOW TABLES;", con=engine)
    print("✅ Connection successful. Tables in DB:")
    print(df)
except Exception as e:
    print("❌ Connection failed:")
    print(e)



# Loading Pandas DataFrame from SQL Tables
customers = pd.read_sql_table("customers", engine)
products = pd.read_sql_table("products", engine)
transactions = pd.read_sql_table("transactions", engine)

print(customers.head())
print(products.head())
print(transactions.head())


# Merge Transactions with Customers
merged_df = pd.merge(transactions, customers, on ='CustomerKey', how='left')

# Transactions + Products join (ProductKey ke through)
merged_df = pd.merge(merged_df, products, on="ProductKey", how="left")

#  Cheking Output 
print(merged_df.head())

# Checking for duplicate
dup = merged_df.duplicated().sum()
print("Total no of Duplicates:", dup)


# 1.1 Total Purchases (sum of quantity column)
total_purchases = merged_df['PurchaseQuantity'].sum()
print("Total Purchases:", total_purchases)

# 1.2 Total Revenue (Quantity * Price, then sum)
merged_df['Revenue'] = merged_df['PurchaseQuantity'] * merged_df['PurchasePrice']
total_revenue = merged_df['Revenue'].sum()
print("Total Revenue:", total_revenue)

# 1.3 Average Purchase Value (Total Revenue / Total Purchases)
average_purchase_value = total_revenue / total_purchases
print("Average Purchase Value:", average_purchase_value)



# 2. Identify Top Customers and Their Purchasing Behavior
# Group data by customer and calculate Total revenue & Total purchases 
customer_stats = (
    merged_df.groupby('CustomerKey')
    .agg(
        TotalRevenue=('Revenue', 'sum'),
        TotalPurchases=('PurchaseQuantity', 'sum')
    )
    .sort_values(by='TotalRevenue', ascending=False)
)

print("Top 5 Customers by Revenue:")
print(customer_stats.head(5))

# Avg Purchase Value for checking spending pattern
customer_stats['AvgPurchaseValue'] = (
    customer_stats['TotalRevenue'] / customer_stats['TotalPurchases']
)
customer_stats = customer_stats.sort_values(by='AvgPurchaseValue', ascending=False)

print("Customer with Avg Purchase Value):")
print(customer_stats.head())



# 3. Analyze purchase trends over time (Monthly, Quarterly, Yearly)
# Make sure PurchaseDate is datetime
print(merged_df['PurchaseDate'].dtype)

# Extract Year, Month, Quarter
merged_df['Year'] = merged_df['PurchaseDate'].dt.year
merged_df['Month'] = merged_df['PurchaseDate'].dt.month
merged_df['Quarter'] = merged_df['PurchaseDate'].dt.to_period('Q')

# Yearly Trends
yearly_trends = (
    merged_df.groupby('Year')
    .agg(TotalQuantity=('PurchaseQuantity', 'sum'), TotalRevenue=('Revenue', 'sum')).reset_index()
)

# Quarterly Trends
quarterly_trends = (
    merged_df.groupby('Quarter')
    .agg(TotalQuantity=('PurchaseQuantity', 'sum'), TotalRevenue=('Revenue', 'sum')).reset_index()
)

# Monthly Trends
monthly_trends = (
    merged_df.groupby(['Year', 'Month'])
    .agg(TotalQuantity=('PurchaseQuantity', 'sum'), TotalRevenue=('Revenue', 'sum')).reset_index()
)

print("Yearly Trends:\n", yearly_trends)
print("\nQuarterly Trends:\n", quarterly_trends)
print("\nMonthly Trends:\n", monthly_trends)



# 4. Identify the top-performing product categories
# Group by ProductCategory and calculate total revenue & quantity
top_categories = merged_df.groupby('ProductCategory').agg(
    TotalRevenue=('Revenue', 'sum'),
    TotalPurchases=('PurchaseQuantity', 'sum')
).sort_values(by='TotalRevenue', ascending=False).reset_index()

print("\nTop Performing Product Categories:\n", top_categories)



# 5. Generate a summary report with key insights.
'''
Customer Purchase Behavior Summary Report
Total Purchases: 3,042
Total Revenue: Rs.1,481,506.85
Average Purchase Value: Rs.487.02

Top 5 Customers by Revenue:
Customers 794, 316, 455, 485, 86 — each with around Rs.4,950 to Rs.5,000 revenue and 5 purchases each.
Customers with Highest Average Purchase Value:
Customers 266, 794, 316, 137, 363 — with average purchase values close to Rs.1,000.

Yearly Sales Trends:

2023: 1,647 units sold, revenue 790,514.96

2024: 1,395 units sold, revenue 690,991.89

Quarterly Sales Trends:

Highest revenue in Q3 and Q4 2023 (~380,000 and 402,000 respectively)

Moderate sales continuing in early 2024

Monthly Sales Trends (Sample):

June 2023: Rs.8,258.62 from 27 purchases

July 2023: Rs.140,528.32 from 269 purchases

August 2023: Rs.95,945.72 from 233 purchases

Top Performing Product Categories:

Home Appliances: Rs.745,538.64 revenue from 1,563 purchases

Electronics: Rs.735,968.21 revenue from 1,479 purchases

Insights:

The majority of revenue comes from Home Appliances and Electronics.

Top customers are consistent in purchases and contribute significantly to revenue.

Q3 and Q4 are peak sales quarters, possibly due to seasonal factors.

Focus marketing efforts on these product categories and peak quarters for maximum impact

'''
