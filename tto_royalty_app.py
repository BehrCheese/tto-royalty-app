import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# Function to format large numbers
def format_large_number(value):
    if value >= 1000:
        return f"${value / 1000:.2f}B"
    return f"${value:.2f}M"

# Function to calculate royalty revenue
def calculate_royalty_revenue(royalty_rate, market_entry_year, royalty_term, market_size, cagr, market_penetration):
    projected_market = market_size * 1_000_000  # Convert from $M to $
    total_royalty = 0
    results = []
    
    for year in range(market_entry_year, market_entry_year + royalty_term):
        projected_market *= (1 + cagr / 100)
        penetrated_market = projected_market * (market_penetration / 100)
        annual_royalty = penetrated_market * (royalty_rate / 100)
        total_royalty += annual_royalty
        results.append({"Year": year, "Penetrated Market": penetrated_market / 1_000_000, "Annual Royalty": annual_royalty / 1_000_000, "Market Size": projected_market / 1_000_000})
    
    df = pd.DataFrame(results)
    return df, total_royalty

# Streamlit Web UI
st.title("📊 Royalty Analysis")

# User Inputs
royalty_rate = st.number_input("Minimum Expected Royalty Rate (%)", min_value=0.1, max_value=20.0, value=5.0, step=0.1)
market_entry_year = st.number_input("Anticipated Year of Market Entry", min_value=2024, max_value=2050, value=2026, step=1)
royalty_term = st.slider("Royalty Term Length (Years)", min_value=1, max_value=20, value=10)
market_size = st.number_input("Current Market Size ($M)", min_value=1, value=500, step=1)
cagr = st.number_input("Compound Annual Growth Rate (CAGR, %)", min_value=0.1, max_value=20.0, value=6.0)
market_penetration = st.number_input("Expected Market Penetration (%)", min_value=1.0, max_value=100.0, value=10.0, step=0.1)

df, total_royalty = calculate_royalty_revenue(royalty_rate, market_entry_year, royalty_term, market_size, cagr, market_penetration)

# Display Data Table
st.subheader("📈 Annual Royalty Revenue Breakdown")
st.dataframe(df)

# Dual Y-Axis Plot
fig, ax1 = plt.subplots(figsize=(10, 5))
ax2 = ax1.twinx()

ax1.plot(df["Year"], df["Market Size"], label="Projected Market Size", linestyle='dashed', color='blue', alpha=0.5)
ax1.plot(df["Year"], df["Penetrated Market"], label="Penetrated Market", marker="^", color='green', linewidth=2)
ax2.plot(df["Year"], df["Annual Royalty"], label="Annual Royalty Revenue", marker="s", color='red', linewidth=2)

ax1.set_xlabel("Year")
ax1.set_ylabel("Market Size & Penetration ($M)", color='blue')
ax2.set_ylabel("Annual Royalty Revenue ($M)", color='red')
ax1.set_title("Market Growth, Penetration & Royalty Projections")
ax1.legend(loc='upper left')
ax2.legend(loc='upper right')
ax1.grid()

st.pyplot(fig)

# Display Financial Estimates
st.subheader("💰 Financial Estimates")
st.write(f"**Total Estimated Royalty Revenue Over {royalty_term} Years:** {format_large_number(total_royalty / 1_000_000)}")

# High-Value Opportunity (HVO) Indicator
st.subheader("📊 High-Value Opportunity Indicator")
if total_royalty >= 30_000_000:
    st.success("🎉 Congrats! This is a High-Value Opportunity (HVO) expected to generate over $30M in royalties!")
else:
    st.warning("😞 Unfortunately, this opportunity is expected to generate less than $30M in royalties.")
