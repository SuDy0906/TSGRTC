import streamlit as st
import plotly.graph_objects as go
from utils.passenger import load_weekday_trends_data
from components.sidebar import render_main_sidebar, render_historical_sidebar
from utils.revenue import get_monthly_fare_summary
import pandas as pd

# Page config
st.set_page_config(
    page_title="Historical Trends - TGSRTC Analytics",
    page_icon="📊",
    layout="wide"
)

render_main_sidebar()
filters = render_historical_sidebar()

# Load weather data once and preprocess
# weather_csv_path = "Wl-Upl_final.csv"
print(filters["csv_path"])
df = pd.read_csv(filters['csv_path'], parse_dates=["date"])
df["Year"] = df["date"].dt.year
df["Month"] = df["date"].dt.month_name()
df["Month_Num"] = df["date"].dt.month
df.sort_values("date", inplace=True)


# Sidebar rendering


# Get trend type choice
trend_type = filters['trend_view_option']

if trend_type == "Passenger Trends":
    # Title of the app
    st.title("VihariNet: AI-Driven Fleet Optimization for TGSRTC")
# Title and description
    import streamlit as st
    import pandas as pd
    import plotly.graph_objects as go

    st.title("📊 Historical Passenger Trends by Weekday")
    st.markdown("""
    Compare historical total passenger counts across weekdays for the years **2022–2024**.  
    The **most popular weekday** is <span style="color:#FF6B93;"><strong>highlighted with a border</strong></span>.
    """, unsafe_allow_html=True)

    

    # # Map integers to weekday names
    # day_map = {
    #     0: 'Monday', 1: 'Tuesday', 2: 'Wednesday',
    #     3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'
    # }
    # df['Weekday'] = df['Day Type'].map(day_map)
    # df['Year'] = df['date'].dt.year

    # # Filter years
    # df = df[df["Year"].isin([2022, 2023, 2024])]

    # # Weekday order
    # ordered_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    # df['Weekday'] = pd.Categorical(df['Weekday'], categories=ordered_days, ordered=True)

    # # --- Prepare Data for Bar Chart ---
    # trend_data = df.groupby(['Year', 'Weekday'])['total_passengers'].sum().reset_index()

    # # Find max weekday over all years
    # weekday_total = trend_data.groupby("Weekday")["total_passengers"].sum()
    # max_weekday = weekday_total.idxmax()

    # # --- Bar Chart ---
    # year_colors = {
    #     2022: "#4682B4",
    #     2023: "#2E8B57",
    #     2024: "#E97451"
    # }
    # bar_opacity = 0.9
    # border_width_default = 0.6
    # border_width_highlight = 2

    # fig_bar = go.Figure()
    # years = sorted(trend_data["Year"].unique())

    # for year in years:
    #     year_data = trend_data[trend_data["Year"] == year].set_index("Weekday").reindex(ordered_days).reset_index()
    #     border_widths = [
    #         border_width_highlight if wd == max_weekday else border_width_default
    #         for wd in year_data["Weekday"]
    #     ]

    #     fig_bar.add_trace(go.Bar(
    #         x=year_data["Weekday"],
    #         y=year_data["total_passengers"],
    #         name=str(year),
    #         marker=dict(
    #             color=year_colors[year],
    #             line=dict(color='white', width=border_widths)
    #         ),
    #         opacity=bar_opacity,
    #         text=year_data["total_passengers"].apply(lambda x: f"{int(x):,}"),
    #         textposition="outside",
    #         hovertemplate="<b>%{x}</b><br>Year: "+str(year)+"<br>Passengers: %{y:,}<extra></extra>"
    #     ))

    # fig_bar.update_layout(
    #     barmode='group',
    #     title=dict(
    #         text=f"📈 Passenger Distribution by Weekday (2022–2024)<br><span style='font-size:16px;'>🏆 Highest Overall: {max_weekday}</span>",
    #         x=0.5, xanchor='center', font=dict(size=20)
    #     ),
    #     xaxis=dict(title="Weekday", tickfont=dict(size=13)),
    #     yaxis=dict(title="Total Passengers", titlefont=dict(size=14), tickfont=dict(size=12), gridcolor="#444"),
    #     plot_bgcolor="#1E1E1E",
    #     paper_bgcolor="#1E1E1E",
    #     font=dict(color="white"),
    #     legend=dict(title="Year", orientation="h", y=-0.2),
    #     bargap=0.15
    # )

    # st.plotly_chart(fig_bar, use_container_width=True)

    # Filter and map weekday names
    df_filtered = df[df["Year"].isin([2022, 2023, 2024])].copy()
    df_filtered["Weekday"] = df_filtered["date"].dt.day_name()
    weekday_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    df_filtered["Weekday"] = pd.Categorical(df_filtered["Weekday"], categories=weekday_order, ordered=True)

    # Group and prepare data
    summary_df = df_filtered.groupby(["Year", "Weekday"])["total_passengers"].sum().reset_index()
    summary_df.sort_values(["Weekday", "Year"], inplace=True)

    # Identify the most popular weekday across all years
    total_by_weekday = summary_df.groupby("Weekday")["total_passengers"].sum()
    most_popular_day = total_by_weekday.idxmax()

    # Define colors and styles
    year_colors = {
        2022: "#4682B4",  # dark steel blue
        2023: "#2E8B57",  # dark forest green
        2024: "#E97451"   # dark red/burgundy
    }
    border_width_default = 0.6
    border_width_highlight = 2

    # Plot
    fig = go.Figure()
    years = sorted(summary_df["Year"].unique())

    for year in years:
        year_df = summary_df[summary_df["Year"] == year]
        line_widths = [border_width_highlight if day == most_popular_day else border_width_default for day in year_df["Weekday"]]

        fig.add_trace(go.Bar(
            x=year_df["Weekday"],
            y=year_df["total_passengers"],
            name=str(year),
            marker=dict(
                color=year_colors[year],
                line=dict(color="white", width=line_widths)
            ),
            text=[f"{val:,.0f}" for val in year_df["total_passengers"]],
            textposition="outside",
            hoverinfo="text",
            hovertext=[
                f"{day} {year}<br>Passengers: {val:,.0f}"
                for day, val in zip(year_df["Weekday"], year_df["total_passengers"])
            ]
        ))

    fig.update_layout(
        barmode="group",
        title=dict(
            text=f"📈 Passenger Distribution by Weekday (2022–2024)<br><span style='font-size:16px;'>🏆 Highest Overall: {most_popular_day}</span>",
            x=0.5,
            font=dict(size=20)
        ),
        xaxis_title="Weekday",
        yaxis_title="Total Passengers",
        template="plotly_dark",
        height=550,
        legend=dict(title="Year", orientation="h", y=-0.2)
    )

    st.plotly_chart(fig, use_container_width=True)


    # --- Pie Chart Section ---
    st.markdown("### 🥧 Weekday Share of Total Passengers (2022–2024)")
    # Prepare pie chart data from summary_df (already grouped by Year & Weekday)
    pie_data = summary_df.groupby("Weekday")["total_passengers"].sum().reset_index()
    total = pie_data["total_passengers"].sum()
    pie_data["percentage"] = round(100 * pie_data["total_passengers"] / total, 2)

    # Color map
    weekday_colors = {
        "Monday": "#A398D1",
        "Tuesday": "#5F9EA0",
        "Wednesday": "#708D81",
        "Thursday": "#C2B280",
        "Friday": "#9C6B6B",
        "Saturday": "#61788C",
        "Sunday": "#C97C5D"
    }

    # Pie chart
    fig_pie = go.Figure(
        go.Pie(
            labels=pie_data["Weekday"],
            values=pie_data["total_passengers"],
            textinfo="label+percent",
            textfont=dict(size=16),
            hole=0.4,
            marker=dict(
                colors=[weekday_colors.get(day, "#000000") for day in pie_data["Weekday"]],
                line=dict(color="black", width=1.5)
            ),
            pull=[0.05 if day == most_popular_day else 0 for day in pie_data["Weekday"]],
            hovertemplate="<b>%{label}</b><br>Passengers: %{value:,} (%{percent})<extra></extra>"
        )
    )

    fig_pie.update_layout(
        title=dict(
            text=f"📊 Passenger Share by Weekday (2022–2024)<br><span style='font-size:16px;'>🏆 Most Popular: {most_popular_day}</span>",
            x=0.5,
            font=dict(size=20)
        ),
        showlegend=False,
        template="plotly_dark",
        margin=dict(t=60, b=0, l=0, r=0)
    )

    st.plotly_chart(fig_pie, use_container_width=True)




    st.subheader("🧍 Passengers vs Buses (Daily - Monthly View)")

    # Ensure required columns exist
    df["Year"] = df["date"].dt.year
    df["Month"] = df["date"].dt.month_name()
    df["Month_Num"] = df["date"].dt.month

    # Dropdowns
    selected_year = st.selectbox("Select Year", sorted(df["Year"].unique()), index=len(df["Year"].unique()) - 1)
    months_in_year = df[df["Year"] == selected_year]["Month"].unique()
    selected_month = st.selectbox("Select Month", months_in_year)

    # Filter by month and year
    df_filtered = df[(df["Year"] == selected_year) & (df["Month"] == selected_month)]

    # Sort by date
    df_filtered.sort_values("date", inplace=True)

    # Plot
    fig_pass_bus = go.Figure()

    # Bar for total buses
    fig_pass_bus.add_trace(go.Scatter(
        x=df_filtered["date"],
        y=df_filtered["total_buses"],
        name="Total Buses",
        mode="lines+markers",
        line=dict(color="#A398D1", width=2),
        yaxis="y"
    ))

    # Line for total passengers
    fig_pass_bus.add_trace(go.Scatter(
        x=df_filtered["date"],
        y=df_filtered["total_passengers"],
        name="Total Passengers",
        mode="lines+markers",
        line=dict(color="#C2B280", width=2),
        yaxis="y2"
    ))

    # Layout
    fig_pass_bus.update_layout(
        title=f"Daily Passengers vs Buses – {selected_month} {selected_year}",
        xaxis=dict(title="Date"),
        yaxis=dict(title="Total Buses", side="left"),
        yaxis2=dict(
            title="Total Passengers",
            overlaying="y",
            side="right"
        ),
        template="plotly_dark",
        legend=dict(orientation="h"),
        height=500,
        margin=dict(t=50, b=50)
    )

    st.plotly_chart(fig_pass_bus, use_container_width=True)




# If Revenue Trends selected
elif trend_type == "Revenue Trends":
    st.title("VihariNet: AI-Driven Fleet Optimization for TGSRTC")

    st.title("💰 Monthly Revenue Trends")

    # Extract year and month
    df['Year'] = df['date'].dt.year
    df['Month'] = df['date'].dt.month

    # Group and sum
    monthly_fare = df.groupby(['Year', 'Month'])['total_fare'].sum().reset_index()

    # Add month names
    monthly_fare['Month_Name'] = pd.to_datetime(monthly_fare['Month'], format='%m').dt.strftime('%B')

    # Sort properly
    monthly_fare = monthly_fare.sort_values(['Year', 'Month'])

    # --- UI Filter ---
    selected_year = st.selectbox("Select Year", [2022, 2023, 2024], index=2)
    filtered_revenue = monthly_fare[monthly_fare["Year"] == selected_year]

    # --- Line Chart ---
    fig_revenue = go.Figure()

    fig_revenue.add_trace(go.Scatter(
        x=filtered_revenue["Month_Name"],
        y=filtered_revenue["total_fare"],
        mode="lines+markers",
        line=dict(color="#FFB74D", width=3),
        marker=dict(size=8),
        hovertemplate="<b>%{x}</b><br>Revenue: ₹%{y:,.0f}<extra></extra>"
    ))

    fig_revenue.update_layout(
        title=f"Monthly Revenue Trend - {selected_year}",
        xaxis_title="Month",
        yaxis_title="Total Revenue (₹)",
        plot_bgcolor="#1E1E1E",
        paper_bgcolor="#1E1E1E",
        font=dict(color="white"),
        xaxis=dict(tickmode="linear"),
        yaxis=dict(gridcolor="#444"),
        margin=dict(t=50, b=50, l=0, r=0)
    )

    st.plotly_chart(fig_revenue, use_container_width=True)


    st.subheader("💰 Revenue vs Buses (Daily - Monthly View)")

    # Ensure required columns exist
    df["Year"] = df["date"].dt.year
    df["Month"] = df["date"].dt.month_name()
    df["Month_Num"] = df["date"].dt.month

    # Dropdowns
    selected_year = st.selectbox("Select Year", sorted(df["Year"].unique()), index=len(df["Year"].unique()) - 1, key="year_revenue")
    months_in_year = df[df["Year"] == selected_year]["Month"].unique()
    selected_month = st.selectbox("Select Month", months_in_year, key="month_revenue")

    # Filter by month and year
    df_filtered = df[(df["Year"] == selected_year) & (df["Month"] == selected_month)]

    # Sort by date
    df_filtered.sort_values("date", inplace=True)

    # Plot
    fig_revenue_bus = go.Figure()
    # Line for total buses
    fig_revenue_bus.add_trace(go.Scatter(
        x=df_filtered["date"],
        y=df_filtered["total_buses"],
        name="Total Buses",
        mode="lines+markers",
        line=dict(color="#F8961E", width=2),
        yaxis="y"
    ))

    # Line for total revenue
    fig_revenue_bus.add_trace(go.Scatter(
        x=df_filtered["date"],
        y=df_filtered["total_fare"],
        name="Total Revenue (₹)",
        mode="lines+markers",
        line=dict(color="#43AA8B", width=2),
        yaxis="y2"
    ))

    # Layout
    fig_revenue_bus.update_layout(
        title=f"Daily Revenue vs Buses – {selected_month} {selected_year}",
        xaxis=dict(title="Date"),
        yaxis=dict(title="Total Buses", side="left"),
        yaxis2=dict(
            title="Total Revenue (₹)",
            overlaying="y",
            side="right"
        ),
        template="plotly_dark",
        legend=dict(orientation="h"),
        height=500,
        margin=dict(t=50, b=50)
    )

    st.plotly_chart(fig_revenue_bus, use_container_width=True)


elif trend_type == "Weather Trends":
    st.title("VihariNet: AI-Driven Fleet Optimization for TGSRTC")
    st.title("🌦️ Weather Impact on Passenger Demand")

    # Year and Month selection
    selected_year = st.selectbox("Select Year", sorted(df["Year"].unique()), index=2)

    # Filter data for the selected year
    df_year = df[df["Year"] == selected_year].copy()

    # Group by month and calculate total rainfall and passengers
    monthly_summary = df_year.groupby("Month").agg({
        "Rainfall_mm": "sum",
        "total_passengers": "sum"
    }).reset_index()

    # # Convert month number to month name for better display
    # monthly_summary["Month"] = pd.to_datetime(monthly_summary["Month"], format='%m').dt.strftime('%B')

    # Maintain month order
    month_order = ["January", "February", "March", "April", "May", "June",
                "July", "August", "September", "October", "November", "December"]
    monthly_summary["Month"] = pd.Categorical(monthly_summary["Month"], categories=month_order, ordered=True)
    monthly_summary.sort_values("Month", inplace=True)

    # ----------------------------
    # 1. Rainfall vs Passengers (Monthly View)
    # ----------------------------
    st.subheader("🌧️ Monthly Rainfall vs Passenger Trends")

    fig_rain_monthly = go.Figure()

    fig_rain_monthly.add_trace(go.Bar(
        x=monthly_summary["Month"],
        y=monthly_summary["Rainfall_mm"],
        name="Rainfall (mm)",
        marker_color="#4FC3F7",
        opacity=0.6,
        yaxis="y"
    ))

    fig_rain_monthly.add_trace(go.Scatter(
        x=monthly_summary["Month"],
        y=monthly_summary["total_passengers"],
        name="Passengers",
        mode="lines+markers",
        line=dict(color="#76C7C0", width=2),
        yaxis="y2"
    ))

    fig_rain_monthly.update_layout(
        title=f"Rainfall vs Passengers (Monthly) - {selected_year}",
        xaxis_title="Month",
        yaxis=dict(title="Rainfall (mm)", side="left"),
        yaxis2=dict(title="Passengers", overlaying="y", side="right"),
        template="plotly_dark",
        legend=dict(orientation="h"),
        height=500,
        margin=dict(t=50, b=50)
    )

    st.plotly_chart(fig_rain_monthly, use_container_width=True)


    # ----------------------------
    # 2. Temperature vs Passengers/Buses
    # ----------------------------
    st.subheader("🌡️ Temperature vs Passenger Trends (Daily)")
    
    selected_year = st.selectbox("Select Year", sorted(df["Year"].unique()), index=2, key="weather_year")
    months_in_year = df[df["Year"] == selected_year]["Month"].unique()
    selected_month = st.selectbox("Select Month", months_in_year, key="weather_month")


    # Filter data by selected year and month
    df_filtered = df[(df["Year"] == selected_year) & (df["Month"] == selected_month)]

    # Sort by date
    df_filtered.sort_values("date", inplace=True)

    fig_temp = go.Figure()

    fig_temp.add_trace(go.Scatter(
        x=df_filtered["date"], y=df_filtered["Min_temp_celsius"],
        name="Min Temp (°C)",
        mode="lines+markers",
        line=dict(color="#90CAF9", dash="dot"),
        yaxis="y"
    ))

    fig_temp.add_trace(go.Scatter(
        x=df_filtered["date"], y=df_filtered["Max_temp_celsius"],
        name="Max Temp (°C)",
        mode="lines+markers",
        line=dict(color="#FF8A65"),
        yaxis="y"
    ))

    fig_temp.add_trace(go.Scatter(
        x=df_filtered["date"], y=df_filtered["total_passengers"],
        name="Passengers",
        mode="lines+markers",
        line=dict(color="#76C7C0", width=2),
        yaxis="y2"
    ))

    # fig_temp.add_trace(go.Scatter(
    #     x=df_filtered["date"], y=df_filtered["total_buses"],
    #     name="Total Buses",
    #     mode="lines+markers",
    #     line=dict(color="#FFD166", width=2, dash='dot'),
    #     yaxis="y2"
    # ))

    fig_temp.update_layout(
        title="Temperature vs Passengers",
        xaxis_title="Date",
        yaxis=dict(title="Temperature (°C)", side="left"),
        yaxis2=dict(title="Passengers", overlaying="y", side="right"),
        template="plotly_dark",
        legend=dict(orientation="h"),
        height=500,
        margin=dict(t=50, b=50)
    )

    st.plotly_chart(fig_temp, use_container_width=True)


elif trend_type == "Holiday Impact":
    st.title("VihariNet: AI-Driven Fleet Optimization for TGSRTC")
    st.subheader("🎉 Holiday Impact on Trends (Daily - Monthly View)")

    # Extract date info
    df["Year"] = df["date"].dt.year
    df["Month"] = df["date"].dt.month_name()
    df["Month_Num"] = df["date"].dt.month

    # Dropdown filters
    selected_year = st.selectbox("Select Year", sorted(df["Year"].unique()), index=len(df["Year"].unique()) - 1, key="year_holiday")
    months_in_year = df[df["Year"] == selected_year]["Month"].unique()
    selected_month = st.selectbox("Select Month", months_in_year, key="month_holiday")

    # Filter data
    df_filtered = df[(df["Year"] == selected_year) & (df["Month"] == selected_month)].copy()
    df_filtered.sort_values("date", inplace=True)

    # Holiday map
    holiday_colors = {
        0: "#A9A9A9",   # Normal
        1: "#FFD700",   # Optional
        2: "#FF6347",   # Holiday
        3: "#9370DB"    # Long Weekend
    }
    holiday_labels = {
        0: "Normal",
        1: "Optional Holiday",
        2: "Holiday",
        3: "Long Weekend"
    }
    df_filtered["holiday_label"] = df_filtered["Holiday"].map(holiday_labels)

    # ---------- 🔷 Add Manual Legend ----------
    st.markdown("##### 🗓️ Holiday Legend")
    

    # Transparent hover markers
    hover_annotations = []
    for _, row in df_filtered.iterrows():
        if row["Holiday"] in [1, 2, 3]:
            hover_annotations.append(go.Scatter(
                x=[row["date"] + pd.Timedelta(hours=12)],
                y=[df_filtered["total_buses"].max()],
                mode="markers",
                marker=dict(size=12, color='rgba(0,0,0,0)'),
                hoverinfo="text",
                text=[holiday_labels[row["Holiday"]]],
                showlegend=False
            ))

    # ---------- Graph 1: Revenue vs Buses ----------
    st.markdown("#### 💰 Revenue vs Buses (Holiday Highlighted)")

    fig_rev_bus = go.Figure()

    fig_rev_bus.add_trace(go.Scatter(
        x=df_filtered["date"],
        y=df_filtered["total_buses"],
        mode='lines+markers',
        name="Total Buses",
        line=dict(width=2, color="#FFA726"),
        yaxis="y"
    ))

    fig_rev_bus.add_trace(go.Scatter(
        x=df_filtered["date"],
        y=df_filtered["total_fare"],
        mode='lines+markers',
        name="Total Revenue (₹)",
        line=dict(width=2, color="#66BB6A"),
        yaxis="y2"
    ))

    # Add shaded holiday regions
    for _, row in df_filtered.iterrows():
        if row["Holiday"] in [1, 2, 3]:
            fig_rev_bus.add_shape(
                type="rect",
                x0=row["date"],
                x1=row["date"] + pd.Timedelta(days=1),
                y0=0, y1=1,
                yref="paper",
                fillcolor=holiday_colors[row["Holiday"]],
                opacity=0.2,
                layer="below",
                line_width=0
            )
    for ann in hover_annotations:
        fig_rev_bus.add_trace(ann)

    fig_rev_bus.update_layout(
        xaxis_title="Date",
        yaxis=dict(title="Total Buses", side="left"),
        yaxis2=dict(title="Revenue (₹)", overlaying="y", side="right"),
        template="plotly_dark",
        legend=dict(orientation="h"),
        title=f"Revenue vs Buses – {selected_month} {selected_year}",
        height=500
    )
    st.plotly_chart(fig_rev_bus, use_container_width=True)
    st.markdown("""
    <div style='display: flex; gap: 20px; flex-wrap: wrap; margin-bottom: 20px;'>
        <div style='display: flex; align-items: center; gap: 6px;'>
            <div style='width: 15px; height: 15px; background-color: #1e1e1e; border: 1px solid white;'></div>
            <span style='font-size: 14px;'>Normal Day</span>
        </div>
        <div style='display: flex; align-items: center; gap: 6px;'>
            <div style='width: 15px; height: 15px; background-color: #4b4318; border: 1px solid white;'></div>
            <span style='font-size: 14px;'>Optional Holiday</span>
        </div>
        <div style='display: flex; align-items: center; gap: 6px;'>
            <div style='width: 15px; height: 15px; background-color: #4b2c26; border: 1px solid white;'></div>
            <span style='font-size: 14px;'>Holiday</span>
        </div>
        <div style='display: flex; align-items: center; gap: 6px;'>
            <div style='width: 15px; height: 15px; background-color: #352e44; border: 1px solid white;'></div>
            <span style='font-size: 14px;'>Long Weekend</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ---------- Graph 2: Passengers vs Buses ----------
    st.markdown("#### 🧍 Passengers vs Buses (Holiday Highlighted)")

    fig_pass_bus = go.Figure()

    fig_pass_bus.add_trace(go.Scatter(
        x=df_filtered["date"],
        y=df_filtered["total_buses"],
        mode='lines+markers',
        name="Total Buses",
        line=dict(width=2, color="#FFA726"),
        yaxis="y"
    ))

    fig_pass_bus.add_trace(go.Scatter(
        x=df_filtered["date"],
        y=df_filtered["total_passengers"],
        mode='lines+markers',
        name="Total Passengers",
        line=dict(width=2, color="#42A5F5"),
        yaxis="y2"
    ))

    for _, row in df_filtered.iterrows():
        if row["Holiday"] in [1, 2, 3]:
            fig_pass_bus.add_shape(
                type="rect",
                x0=row["date"],
                x1=row["date"] + pd.Timedelta(days=1),
                y0=0, y1=1,
                yref="paper",
                fillcolor=holiday_colors[row["Holiday"]],
                opacity=0.2,
                layer="below",
                line_width=0
            )
    for ann in hover_annotations:
        fig_pass_bus.add_trace(ann)

    fig_pass_bus.update_layout(
        xaxis_title="Date",
        yaxis=dict(title="Total Buses", side="left"),
        yaxis2=dict(title="Total Passengers", overlaying="y", side="right"),
        template="plotly_dark",
        legend=dict(orientation="h"),
        title=f"Passengers vs Buses – {selected_month} {selected_year}",
        height=500
    )
    st.plotly_chart(fig_pass_bus, use_container_width=True)
    st.markdown("""
    <div style='display: flex; gap: 20px; flex-wrap: wrap; margin-bottom: 20px;'>
        <div style='display: flex; align-items: center; gap: 6px;'>
            <div style='width: 15px; height: 15px; background-color: #1e1e1e; border: 1px solid white;'></div>
            <span style='font-size: 14px;'>Normal Day</span>
        </div>
        <div style='display: flex; align-items: center; gap: 6px;'>
            <div style='width: 15px; height: 15px; background-color: #4b4318; border: 1px solid white;'></div>
            <span style='font-size: 14px;'>Optional Holiday</span>
        </div>
        <div style='display: flex; align-items: center; gap: 6px;'>
            <div style='width: 15px; height: 15px; background-color: #4b2c26; border: 1px solid white;'></div>
            <span style='font-size: 14px;'>Holiday</span>
        </div>
        <div style='display: flex; align-items: center; gap: 6px;'>
            <div style='width: 15px; height: 15px; background-color: #352e44; border: 1px solid white;'></div>
            <span style='font-size: 14px;'>Long Weekend</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
