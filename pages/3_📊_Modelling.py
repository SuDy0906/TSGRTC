import streamlit as st

st.set_page_config(
    page_title="Exploratory Data Analysis - TGSRTC Analytics",
    page_icon="📊",
    layout="wide"
)



st.title("VihariNet: AI-Driven Fleet Optimization for TGSRTC")


import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import streamlit as st

st.title("📈 Passenger & Revenue Forecast – Actual vs Predicted")

# Step 0: Route selection
route_options = {
    "Warangal - Upl": {
        "passenger_file": "ActualvsPrediction_passengers_Wl-Upl.csv",
        "revenue_file": "ActualvsPrediction_revenue_Wl-Upl.csv"
    },
    "49m Route": {
        "passenger_file": "ActualvsPrediction_passengers_49M.csv",
        "revenue_file": "ActualvsPrediction_revenue_49M.csv"
    },
    # Add more routes if needed
}

selected_route = st.selectbox("Select Route", list(route_options.keys()))
route_files = route_options[selected_route]

# Load passenger data
df_passenger = pd.read_csv(route_files["passenger_file"])
start_date = datetime(2022, 4, 1)
df_passenger["date"] = df_passenger["Row"].apply(lambda x: start_date + timedelta(days=int(x)))
df_passenger["Year"] = df_passenger["date"].dt.year

# Load revenue data
df_revenue = pd.read_csv(route_files["revenue_file"])
df_revenue["date"] = df_revenue["Row"].apply(lambda x: start_date + timedelta(days=int(x)))
df_revenue["Year"] = df_revenue["date"].dt.year

# Extract available years (intersection of both)
years = sorted(set(df_passenger["Year"]).intersection(df_revenue["Year"]))
default_year = 2024 if 2024 in years else years[-1]
selected_year = st.selectbox("Select Year", years, index=years.index(default_year))

# Filter both dataframes by selected year
df_passenger_year = df_passenger[df_passenger["Year"] == selected_year].sort_values("date")
df_revenue_year = df_revenue[df_revenue["Year"] == selected_year].sort_values("date")

# Step 4a: Passenger Plot
st.subheader("🧍 Passenger Trends")
fig_passenger = go.Figure()
fig_passenger.add_trace(go.Scatter(
    x=df_passenger_year["date"],
    y=df_passenger_year["Actual Value"],
    mode="lines+markers",
    name="Actual Passengers",
    line=dict(color="#1f77b4")
))
fig_passenger.add_trace(go.Scatter(
    x=df_passenger_year["date"],
    y=df_passenger_year["Predicted Value"],
    mode="lines+markers",
    name="Predicted Passengers",
    line=dict(color="#ff7f0e")
))
fig_passenger.update_layout(
    title=f"🧍 Actual vs Predicted Passengers ({selected_year}) – {selected_route}",
    xaxis_title="Date",
    yaxis_title="Number of Passengers",
    template="plotly_dark",
    height=500,
    legend=dict(orientation="h", y=-0.2, x=0.5, xanchor="center", yanchor="top")
)
st.plotly_chart(fig_passenger, use_container_width=True)

# Step 4b: Revenue Plot
st.subheader("💰 Revenue Trends")
fig_revenue = go.Figure()
fig_revenue.add_trace(go.Scatter(
    x=df_revenue_year["date"],
    y=df_revenue_year["Actual Value"],
    mode="lines+markers",
    name="Actual Revenue",
    line=dict(color="#5883c3")
))
fig_revenue.add_trace(go.Scatter(
    x=df_revenue_year["date"],
    y=df_revenue_year["Predicted Value"],
    mode="lines+markers",
    name="Predicted Revenue",
    line=dict(color="#ef4e4e")
))
fig_revenue.update_layout(
    title=f"💰 Actual vs Predicted Revenue ({selected_year}) – {selected_route}",
    xaxis_title="Date",
    yaxis_title="Revenue (₹)",
    template="plotly_dark",
    height=500,
    legend=dict(orientation="h", y=-0.2, x=0.5, xanchor="center", yanchor="top")
)
st.plotly_chart(fig_revenue, use_container_width=True)
