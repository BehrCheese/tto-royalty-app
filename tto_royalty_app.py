import random
import requests
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# Function to fetch real-time market CAGR & size
# (Replace with real API keys if available)
def fetch_market_data(product_name):
    try:
        # Placeholder API (Replace with real one)
        url = f"https://api.example.com/market_data?query={product_name}"
        response = requests.get(url).json()
        return {
            "cagr": response.get("cagr", random.uniform(5, 12)),
            "discount_rate": response.get("discount_rate", random.uniform(8, 15)),
            "market_size": response.get("market_size", random.randint(1000, 5000)),
        }
    except:
        return {"cagr": random.uniform(5, 12), "discount_rate": random.uniform(8, 15), "market_size": random.randint(1000, 5000)}

# Function to fetch competitor data
def fetch_competitor_data(product_name):
    try:
        url = f"https://api.example.com/competitors?query={product_name}"
        headers = {"Authorization": "Bearer YOUR_API_KEY"}
        response = requests.get(url, headers=headers).json()
        return response.get("competitors", ["Competitor A", "Competitor B", "Competitor C"])
    except:
        return ["Competitor A", "Competitor B", "Competitor C"]

# Function to calculate royalty valuation
def calculate_royalty_valuation(product_name, royalty_rate, royalty_term):
    market_data = fetch_market_data(product_name)
    cagr = market_data["cagr"]
    discount_rate = market_data["discount_rate"]
    market_size = market_data["market_size"] * 1_000_000
    projected_market = market_size
    total_royalty = 0
    discounted_royalty = 0
    results = []
    
    for year in range(1, royalty_term + 1):
        projected_market *= (1 + cagr / 100)
        annual_royalty = projected_market * (royalty_rate / 100)
        total_royalty += annual_royalty
        discounted_royalty += annual_royalty / ((1 + discount_rate / 100) ** year)
        results.append({"Year": year, "Market Size ($M)": projected_market / 1_000_000, "Annual Royalty ($M)": annual_royalty / 1_000_000})
    
    df = pd.DataFrame(results)
    return df, total_royalty, discounted_royalty, market_data

# Streamlit Web UI
st.title("📊 AI-Powered Royalty Valuation & Market Analysis Tool")
product_name = st.text_input("Enter Product Name", "Biotech Drug XYZ")
royalty_rate = st.slider("Enter Royalty Rate (%)", min_value=1.0, max_value=20.0, value=5.0)
royalty_term = st.slider("Enter Royalty Term (Years)", min_value=1, max_value=20, value=10)

if st.button("Calculate Royalty Valuation"):
    df, total_royalty, discounted_royalty, market_data = calculate_royalty_valuation(product_name, royalty_rate, royalty_term)
    
    st.subheader("🔍 Market & Financial Overview")
    st.write(f"**Estimated Market Size:** ${market_data['market_size']}M")
    st.write(f"**Expected CAGR:** {market_data['cagr']}%")
    st.write(f"**Industry Discount Rate:** {market_data['discount_rate']}%")
    
    st.subheader("🏆 Competitive Landscape")
    competitors = fetch_competitor_data(product_name)
    st.write(f"**Top Competing Products in Development:** {', '.join(competitors)}")
    
    st.subheader("📈 Annual Market Growth & Royalty Revenue")
    st.dataframe(df)
    
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(df["Year"], df["Market Size ($M)"], label="Projected Market Size ($M)", marker="o")
    ax.plot(df["Year"], df["Annual Royalty ($M)"], label="Annual Royalty Revenue ($M)", marker="s")
    ax.set_xlabel("Year")
    ax.set_ylabel("Value ($M)")
    ax.set_title(f"Market Growth & Royalty Projections for {product_name}")
    ax.legend()
    ax.grid()
    
    st.pyplot(fig)
    
    st.subheader("💰 Financial Estimates")
    st.write(f"**Total Estimated Royalty Revenue Over {royalty_term} Years:** ${round(total_royalty / 1_000_000, 2)}M")
    st.write(f"**NPV of Royalty Cash Flows:** ${round(discounted_royalty / 1_000_000, 2)}M")
    
    st.markdown("---")
    st.info("🚀 Future Enhancement: Add risk-adjusted forecasting & dynamic competitor tracking!")
