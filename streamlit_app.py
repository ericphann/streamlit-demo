import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math

st.title("Data App Assignment, on June 20th")

st.write("### Input Data and Examples")
df = pd.read_csv("Superstore_Sales_utf8.csv", parse_dates=True)
st.dataframe(df)

# This bar chart will not have solid bars--but lines--because the detail data is being graphed independently
st.bar_chart(df, x="Category", y="Sales")

# Now let's do the same graph where we do the aggregation first in Pandas... (this results in a chart with solid bars)
st.dataframe(df.groupby("Category").sum())
# Using as_index=False here preserves the Category as a column.  If we exclude that, Category would become the datafram index and we would need to use x=None to tell bar_chart to use the index
st.bar_chart(df.groupby("Category", as_index=False).sum(), x="Category", y="Sales", color="#04f")

# Aggregating by time
# Here we ensure Order_Date is in datetime format, then set is as an index to our dataframe
df["Order_Date"] = pd.to_datetime(df["Order_Date"])
df.set_index('Order_Date', inplace=True)
# Here the Grouper is using our newly set index to group by Month ('M')
sales_by_month = df.filter(items=['Sales']).groupby(pd.Grouper(freq='ME')).sum()

st.dataframe(sales_by_month)

# Here the grouped months are the index and automatically used for the x axis
st.line_chart(sales_by_month, y="Sales")

st.write("## Your additions")
st.write("### (1) add a drop down for Category (https://docs.streamlit.io/library/api-reference/widgets/st.selectbox)")
category = st.selectbox('Select Category', df['Category'].unique())
st.write("You selected: ", category)

st.write("### (2) add a multi-select for Sub_Category *in the selected Category (1)* (https://docs.streamlit.io/library/api-reference/widgets/st.multiselect)")
subcategory = st.multiselect('Select at least one Subcategory', df[df['Category'] == category]['Sub_Category'].unique())
st.write("You selected: ", subcategory)

st.write("### (3) show a line chart of sales for the selected items in (2)")
if category and subcategory:
    monthly_sales_by_category = df[df['Sub_Category'].isin(subcategory)].groupby(pd.Grouper(freq='ME')).sum(["Sales"])
    st.line_chart(monthly_sales_by_category, y='Sales')

st.write("### (4) show three metrics (https://docs.streamlit.io/library/api-reference/data/st.metric) for the selected items in (2): total sales, total profit, and overall profit margin (%)")
if category and subcategory:
    total_profit = monthly_sales_by_category['Profit'].sum()
    total_sales = monthly_sales_by_category['Sales'].sum()
    profit_margin = total_profit/total_sales
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Sales :sunglasses:", f"${total_sales:,.2f}")
    col2.metric("Total Profit :moneybag:", f"${total_profit:,.2f}")
    col3.metric("Profit Margin :money_mouth_face:", f"{profit_margin*100:.2f}%")

st.write("### (5) use the delta option in the overall profit margin metric to show the difference between the overall average profit margin (all products across all categories)")
if category and subcategory:
    average_profit_margin = df['Profit'].sum()/df['Sales'].sum()
    delta = profit_margin - average_profit_margin
    st.metric("Overall Profit Margin", f"{profit_margin*100:.2f}%", delta=f"{delta*100:.2f}%")
