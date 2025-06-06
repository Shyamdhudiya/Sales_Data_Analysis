# -*- coding: utf-8 -*-
"""Sales_Data_Analysis

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1TE73qpxEH9mxuW8XsHsD9gWT6XP5-c_h

# Import necessary Libraries
"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from google.colab import files
uploaded = files.upload()

"""# Load the Data"""

df = pd.read_excel("ECOMM DATA.xlsx")

"""# Explore the Data"""

df.head()

df.columns

df.shape

df.info()

df.describe()

"""# Data Cleaning"""

# convert date columns
df['Order Date'] = pd.to_datetime(df['Order Date'], dayfirst = True)
df['Ship Date'] = pd.to_datetime(df['Ship Date'], dayfirst = True)

# Remove white spaces from column names
df.columns = df.columns.str.strip()

# Handle possible non-numeric shipping costs
df['Shipping Cost'] = df['Shipping Cost'].astype(str).str.replace(',', '').str.strip()
df['Shipping Cost'] = pd.to_numeric(df['Shipping Cost'], errors='coerce')

df.drop(columns=['Postal Code'], inplace=True)

# check missing value
print(df.isnull().sum())

"""# Key Metrics"""

total_sales = df['Sales'].sum()
total_profit = df['Profit'].sum()

print(f"Total Sales: {total_sales:,.2f}")
print(f"Total Profit: {total_profit:,.2f}")

total_orders =df['Order ID'].nunique()
avg_order_value = total_sales / total_orders

print(f"Total Orders: {total_orders}")
print(f"Average Order Value: {avg_order_value:,.2f}")

# trend Over Time
# Monthly sales

df['month'] = df['Order Date'].dt.to_period('M')
monthly_sales = df.groupby('month')['Sales'].sum()

monthly_sales.plot(kind='line', figsize=(12,6))
plt.title('Monthly Sales Trend')
plt.xlabel('Month')
plt.ylabel('Sales')
plt.show()

# Best Selling Products

top_products = df.groupby('Product Name')['Quantity'].sum().sort_values(ascending=False).head(10)

top_products.plot(kind='barh', figsize=(12,6), color='pink')
plt.title('Top Selling Products')
plt.xlabel('Sales')
plt.tight_layout()
plt.show()

# Sales by Category & Sub-Category

category_sales = df.groupby(['Category', 'Sub-Category'])['Sales'].sum().sort_values(ascending=False)
print(category_sales)

pivot_data = df.pivot_table(values='Sales', index='Category', columns='Sub-Category', aggfunc='sum')

plt.figure(figsize=(12, 6))
sns.heatmap(pivot_data, annot=True, fmt=".0f", cmap="YlGnBu")
plt.title("Sales by Category and Sub-Category")
plt.show()

# Sales by Region

region_sales = df.groupby('Region')['Sales'].sum().sort_values(ascending=False)
region_sales.plot(kind='bar', figsize=(12,6), color='green')
plt.title('Sales by Region')
plt.xlabel('Region')
plt.ylabel('Sales')
plt.show()

# profit vs. Discount Scatter plot

plt.figure(figsize=(10,6))
sns.scatterplot(data=df, x='Discount', y='Profit', hue='Category')
plt.title('Profit vs. Discount Scatter Plot')
plt.show()

# Sales by shipping mode
ship_mode_sales = df.groupby('Ship Mode')['Sales'].sum().sort_values()
ship_mode_sales.plot(kind='pie', autopct='%1.1f%%', figsize=(7,7))
plt.title('Sales Distribution by Shipping Mode')

# Sales by Segment

segment_sales = df.groupby('Segment')['Sales'].sum().sort_values()
segment_sales.plot(kind='bar', color='orange')
plt.title('Sales by Customers Segment')

# Heatmap: Sales by Region and Category

pivot = df.pivot_table(values='Sales', index='Region', columns='Category', aggfunc='sum')

plt.figure(figsize=(8,6))
sns.heatmap(pivot, annot=True, fmt=".0f", cmap="YlGnBu")
plt.title('Sales Heatmap by Region and Category')

# Repeat Customers (Customer Loyalty Insight)

repeat_customers = df['Customer ID'].value_counts()
repeat_customers.value_counts().sort_index().plot(kind='bar',figsize=(10,5), color='orchid')
plt.title('Repeat Customers')

# Profit by Sub-Category

subcategory_profit = df.groupby('Sub-Category')['Profit'].sum().sort_values()
subcategory_profit.plot(kind='barh', figsize=(10,6),  color='purple')
plt.title('Profit by Sub-Category')

# Monthy Sales & Profit (Dual Axis Plot)

df['month'] = df['Order Date'].dt.to_period('M')
monthly = df.groupby('month')[['Sales', 'Profit']].sum()

fig, ax1 = plt.subplots(figsize=(12,6))
monthly['Sales'].plot(ax=ax1, color='dodgerblue', label='Sales')
ax2 = ax1.twinx()
monthly['Profit'].plot(ax=ax2, color='orange', label='Profit')
ax1.set_title('Monthly Sales and Profit')
ax1.set_xlabel('Month')
ax1.set_ylabel('Sales')
ax2.set_ylabel('Profit')
ax1.legend(loc='upper left')
ax2.legend(loc='upper right')

plt.figure(figsize=(8,6))
sns.heatmap(df[['Sales', 'Profit', 'Discount', 'Quantity', 'Shipping Cost']].corr(), annot=True, cmap='coolwarm')
plt.title('Correlation Matrix')