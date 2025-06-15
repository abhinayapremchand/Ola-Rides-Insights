import streamlit as st
import pandas as pd
import mysql.connector
import os
import matplotlib.pyplot as plt

# setting up the page
st.set_page_config(page_title="Ola Ride Insights", layout="wide")
st.title("Ola Ride Insights Dashboard")

# MySQL connection
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="ola_db"
    )

# Query function
def run_query(query, params=()):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    rows = cursor.fetchall()
    cols = [i[0] for i in cursor.description]
    cursor.close()
    conn.close()
    return pd.DataFrame(rows, columns=cols)

# Sidebar filters
st.sidebar.header("Filter Data")
vehicle = st.sidebar.selectbox("Select Vehicle Type", ["All", "Auto", "Mini", "Prime Sedan", "Prime SUV"])
payment = st.sidebar.selectbox("Select Payment Method", ["All", "Cash", "UPI", "Card", "Wallet"])

# WHERE clause logic
conditions = []
params = []

if vehicle != "All":
    conditions.append("vehicle_type = %s")
    params.append(vehicle)

if payment != "All":
    conditions.append("payment_method = %s")
    params.append(payment)

where_clause = " AND ".join(conditions)
if where_clause:
    where_clause = "WHERE " + where_clause

# Active filter summary
if vehicle != "All" or payment != "All":
    st.write("**Filtered by:**",
             f"{vehicle}" if vehicle != "All" else "All Vehicles",
             " / ",
             f"{payment}" if payment != "All" else "All Payment Methods")

# Metrics section
col1, col2 = st.columns(2)

with col1:
    df1 = run_query(f"""
        SELECT COUNT(*) AS total_successful_rides
        FROM ola_rides_cleaned
        {where_clause + " AND" if where_clause else "WHERE"} booking_status = 'Success';
    """, params)
    st.metric("Total Successful Rides", int(df1.iloc[0, 0]))

with col2:
    df2 = run_query(f"""
        SELECT SUM(booking_value) AS total_revenue
        FROM ola_rides_cleaned
        {where_clause + " AND" if where_clause else "WHERE"} booking_status = 'Success';
    """, params)
    st.metric("Total Revenue (₹)", f"{df2.iloc[0, 0]:,.2f}")

# Bar chart: Avg rating by vehicle type
st.subheader("Average Customer Rating by Vehicle Type")

df3 = run_query(f"""
    SELECT vehicle_type, ROUND(AVG(customer_rating), 2) AS avg_rating
    FROM ola_rides_cleaned
    {where_clause}
    GROUP BY vehicle_type;
""", params)

fig, ax = plt.subplots()  # default size (balanced)
ax.bar(df3["vehicle_type"], df3["avg_rating"], color="steelblue")
ax.set_xlabel("Vehicle Type")
ax.set_ylabel("Avg Rating")
ax.set_title("Customer Ratings by Vehicle Type")
st.pyplot(fig)

# Top customers table
st.subheader("Top 5 Customers by Ride Count")

df4 = run_query(f"""
    SELECT customer_id, COUNT(*) AS ride_count
    FROM ola_rides_cleaned
    {where_clause}
    GROUP BY customer_id
    ORDER BY ride_count DESC
    LIMIT 5;
""", params)

st.dataframe(df4, use_container_width=True)

# Power BI Dashboard
st.subheader("Power BI Dashboard")
st.write("Below are the visual insights generated using Power BI based on the same ride data.")

# Screenshot titles
titles = [
    "Executive Summary",
    "Trend Analysis",
    "Vehicle Analysis",
    "Cancellations Overview",
    "Ratings Overview"
]

if os.path.exists("powerbi"):
    images = sorted([
        img for img in os.listdir("powerbi")
        if img.lower().endswith((".png", ".jpg", ".jpeg"))
    ])

    if images:
        for i, (img, title) in enumerate(zip(images, titles), start=1):
            st.markdown(f"### - Chart {i}: {title}")
            st.image(f"powerbi/{img}")  # default width
    else:
        st.info("No screenshots found in powerbi/")
else:
    st.warning("The 'powerbi' folder does not exist.")
