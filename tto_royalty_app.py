import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

# Function to format large numbers
def format_large_number(value):
    if value >= 1000:
        return f"${value / 1000:.2f}B"
    return f"${value:.2f}M"

# Function to calculate market penetration with a peak
def calculate_penetration_curve(years, initial_penetration):
    penetration_rates = [initial_penetration / 100]
    peak_penetration = initial_penetration / 100 + 0.25  # Allow natural peak growth
    
    for i in range(1, years):
        if i < 3:
            penetration_rates.append(penetration_rates[-1] + 0.05)  # Slow uptake
        elif i < 7:
            penetration_rates.append(penetration_rates[-1] + 0.10)  # Rapid growth
        elif i == 7 or i == 8:
            penetration_rates.append(peak_penetration)  # Peak
        else:
            penetration_rates.append(penetration_rates[-1] - 0.05)  # Decline/Stabilization
        penetration_rates[-1] = max(penetration_rates[-1], penetration_rates[0])  # Ensure it doesn't go below initial
    return penetration_rates[:years]

# Function to calculate royalty revenue
def calculate_royalty_revenue(royalty_rate, market_entry_year, royalty_term, market_size, cagr, initial_penetration):
    projected_market = market_size * 1_000_000  # Convert from $M to $
    total_royalty = 0
    results = []
    
    penetration_rates = calculate_penetration_curve(royalty_term, initial_penetration)
    
    for i, year in enumerate(range(market_entry_year, market_entry_year + royalty_term)):
        projected_market *= (1 + cagr / 100)
        penetrated_market = projected_market * penetration_rates[i]
        annual_royalty = penetrated_market * (royalty_rate / 100)
        total_royalty += annual_royalty
        results.append({
            "Year": str(year),  # Ensure years are strings to prevent commas
            "Market Size": format_large_number(projected_market / 1_000_000),
            "Penetrated Market": format_large_number(penetrated_market / 1_000_000),
            "Annual Royalty": format_large_number(annual_royalty / 1_000_000)
        })
    
    df = pd.DataFrame(results)
    return df, total_royalty

# Streamlit Web UI
st.title("📊 Royalty Analysis")

# User Inputs
royalty_rate = st.number_input("Minimum Expected Royalty Rate (%)", min_value=0.1, max_value=20.0, value=5.0, step=0.1)
market_entry_year = st.number_input("Anticipated Year of Market Entry", min_value=2024, max_value=2050, value=2026, step=1)
royalty_term = st.slider("Royalty Term Length (Years)", min_value=1, max_value=35, value=10)
market_size = st.number_input("Current Market Size ($M)", min_value=1, value=500, step=1)
cagr = st.number_input("Compound Annual Growth Rate (CAGR, %)", min_value=1, max_value=20, value=6, step=1)
initial_penetration = st.number_input("Initial Market Penetration (%)", min_value=1, max_value=100, value=10, step=1)

if st.button("Calculate Royalty Projections"):
    df, total_royalty = calculate_royalty_revenue(royalty_rate, market_entry_year, royalty_term, market_size, cagr, initial_penetration)
    
    # Display Data Table with Proper Formatting
    st.subheader("📈 Annual Royalty Revenue Breakdown")
    st.dataframe(df)
    
    # Dual Y-Axis Plot
    fig, ax1 = plt.subplots(figsize=(10, 5))
    ax2 = ax1.twinx()
    
    ax1.plot(df["Year"], df["Penetrated Market"], label="Penetrated Market", marker="^", color='green', linewidth=2)
    ax1.plot(df["Year"], df["Market Size"], label="Projected Market Size", linestyle='dashed', color='blue', alpha=0.5)
    ax2.plot(df["Year"], df["Annual Royalty"], label="Annual Royalty Revenue", marker="s", color='red', linewidth=2)
    
    ax1.set_xlabel("Year")
    ax1.set_ylabel("Market Size & Penetration ($M)", color='blue')
    ax2.set_ylabel("Annual Royalty Revenue ($M)", color='red')
    ax1.set_title("Market Growth, Penetration & Royalty Projections")
    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')
    ax1.grid()
    
    st.pyplot(fig)
    
    # Display High-Value Opportunity Notification
    st.markdown("---")
    st.markdown("<h2 style='text-align: center; color: black;'>Total Estimated Royalty Revenue".format(royalty_term), unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; color: green;'>{}</h1>".format(format_large_number(total_royalty / 1_000_000)), unsafe_allow_html=True)
    
    if total_royalty >= 30_000_000:
        st.markdown("<h3 style='text-align: center; color: darkblue;'>🎉 Congrats! This is a High-Value Opportunity (HVO)! 🎉</h3>", unsafe_allow_html=True)
    else:
        st.markdown("<h3 style='text-align: center; color: red;'>😞 Unfortunately, this opportunity is expected to generate less than $30M in royalties.</h3>", unsafe_allow_html=True)
