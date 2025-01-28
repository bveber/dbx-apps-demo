# File: africa_gdp_app.py
import os
import streamlit as st
import pandas as pd
from databricks import sql
from databricks.sdk.core import Config

# Ensure environment variable is set correctly
assert os.getenv('DATABRICKS_WAREHOUSE_ID'), "DATABRICKS_WAREHOUSE_ID must be set in app.yaml."

assert False

def sqlQuery(query: str) -> pd.DataFrame:
    cfg = Config() # Pull environment variables for auth
    with sql.connect(
        server_hostname=cfg.host,
        http_path=f"/sql/1.0/warehouses/{os.getenv('DATABRICKS_WAREHOUSE_ID')}",
        credentials_provider=lambda: cfg.authenticate
    ) as connection:
        with connection.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall_arrow().to_pandas()

st.set_page_config(layout="wide")

@st.cache_data(ttl=30)  # only re-query if it's been 30 seconds
def load_data():
    # This example query depends on the nyctaxi data set in Unity Catalog, see https://docs.databricks.com/en/discover/databricks-datasets.html for details
    return sqlQuery("select * from `phdata-dev-uc`.bveber.africa_gdp limit 5000")


# Main App
def main():
    st.title("Africa GDP Interactive Dashboard")

    # Load Data
    df = load_data()

    # Rename columns for better display
    df.columns = [col.strip() for col in df.columns]

    # Convert Year to string for x-axis
    df["Year"] = df["Year"].astype(str)

    # Convert GDP values to Billions
    for col in df.columns[1:]:
        df[col] = df[col] / 1e9

    # Filters
    st.sidebar.header("Filters")
    year = st.sidebar.selectbox("Select Year", sorted(df["Year"].unique()), index=0)
    countries = st.sidebar.multiselect(
        "Select Countries",
        options=df.columns[1:],  # Exclude 'Year'
        default=["Algeria", "Nigeria", "South Africa"],  # Pre-select some countries
    )

    # Filter Data
    filtered_df = df[df["Year"] == year]

    # Display Data
    st.subheader("Filtered Data (Billions)")
    if countries:
        st.dataframe(filtered_df[["Year"] + countries], hide_index=True)

    # Visualization
    st.subheader("GDP Trends")
    if countries:
        chart_data = df[["Year"] + countries].set_index("Year")
        st.line_chart(chart_data[countries])

# Run App
if __name__ == "__main__":
    main()
