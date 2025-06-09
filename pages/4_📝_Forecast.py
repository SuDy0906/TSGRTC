import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from io import BytesIO

# Configure page
st.set_page_config(
    page_title="Forecast & Alerts - TGSRTC Analytics",
    page_icon="🔮",
    layout="wide"
)

st.title("📅 March 2025 – Predicted Passengers & Revenue")

# --- Step 0: Define route options and corresponding files ---
route_files = {
    "Warangal - Upl": {
        "passenger": "Predicted_passengers_Wl-Upl.csv",
        "revenue": "Predicted_revenue_Wl-Upl.csv"
    },
    "49M Route": {
        "passenger": "Predicted_passengers_49M.csv",
        "revenue": "Predicted_revenue_49M.csv"
    },
    # Add more routes here as needed
}

# --- Step 1: Route selector ---
selected_route = st.selectbox("Select Route", list(route_files.keys()))
selected_files = route_files[selected_route]

# --- Step 2: Load Data ---
df_passenger = pd.read_csv(selected_files["passenger"], parse_dates=["date"])
df_revenue = pd.read_csv(selected_files["revenue"], parse_dates=["date"])

# Filter to March 2025
df_passenger = df_passenger[df_passenger["date"].dt.strftime("%Y-%m") == "2025-03"]
df_revenue = df_revenue[df_revenue["date"].dt.strftime("%Y-%m") == "2025-03"]

# --- Step 3: Passenger Plot ---
st.subheader(f"🧍 Predicted Total Passengers – March 2025 ({selected_route})")
fig1 = px.line(
    df_passenger,
    x="date",
    y="total_passengers_PREDICTION",
    title="Predicted Passengers",
    markers=True
)
fig1.update_layout(template="plotly_dark", xaxis_title="Date", yaxis_title="Total Passengers")
st.plotly_chart(fig1, use_container_width=True)

# --- Download Button: Passenger ---
csv_passenger = df_passenger.to_csv(index=False).encode('utf-8')
st.download_button(
    label="📥 Download Passenger Forecast CSV",
    data=csv_passenger,
    file_name=f"March2025_Passenger_Predictions_{selected_route.replace(' ', '_')}.csv",
    mime="text/csv"
)

# --- Step 4: Revenue Plot ---
st.subheader(f"💰 Predicted Total Revenue – March 2025 ({selected_route})")
fig2 = px.line(
    df_revenue,
    x="date",
    y="total_fare_PREDICTION",
    title="Predicted Revenue",
    markers=True
)
fig2.update_layout(template="plotly_dark", xaxis_title="Date", yaxis_title="Revenue (₹)")
st.plotly_chart(fig2, use_container_width=True)

# --- Download Button: Revenue ---
csv_revenue = df_revenue.to_csv(index=False).encode('utf-8')
st.download_button(
    label="📥 Download Revenue Forecast CSV",
    data=csv_revenue,
    file_name=f"March2025_Revenue_Predictions_{selected_route.replace(' ', '_')}.csv",
    mime="text/csv"
)
