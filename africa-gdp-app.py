# File: africa_gdp_app.py
import streamlit as st
import pandas as pd
from pyspark.sql import SparkSession

# Initialize Spark Session
spark = SparkSession.builder.getOrCreate()

# Load Delta Table into a Pandas DataFrame
@st.cache_resource
def load_data():
    return spark.sql("SELECT * FROM africa_gdp").toPandas()

# Main App
def main():
    st.title("Africa GDP Interactive Dashboard")
    
    # Load Data
    df = load_data()
    
    # Filters
    st.sidebar.header("Filters")
    year = st.sidebar.selectbox("Year", sorted(df["year"].unique()), index=0)
    country = st.sidebar.multiselect("Country", df["country"].unique())

    # Apply Filters
    filtered_df = df[(df["year"] == year)]
    if country:
        filtered_df = filtered_df[filtered_df["country"].isin(country)]

    # Display Data
    st.subheader("Filtered Data")
    st.dataframe(filtered_df)

    # Visualization
    st.subheader("GDP Trends")
    if not filtered_df.empty:
        chart_data = filtered_df.groupby("year").sum("gdp").reset_index()
        st.line_chart(data=chart_data, x="year", y="gdp")

# Run App
if __name__ == "__main__":
    main()
