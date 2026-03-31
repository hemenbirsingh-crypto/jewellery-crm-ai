import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# 👥 Customers
customers = [
    {"name": "Raj", "type": "investor"},
    {"name": "Simran", "type": "jewellery"},
    {"name": "Aman", "type": "premium"}
]

# 🏦 Gold Price (LBMA + Live + AUD)
def get_gold_prices():
    try:
        API_KEY = st.secrets["API_KEY"]  # 🔐 secure

        lbma_url = f"https://api.metals.dev/v1/metal/authority?api_key={API_KEY}&authority=lbma&currency=USD&unit=toz"
        lbma_data = requests.get(lbma_url, timeout=5).json()
        lbma_usd = lbma_data["rates"]["lbma_gold_pm"]

        live_url = "https://api.gold-api.com/price/XAU"
        live_data = requests.get(live_url, timeout=5).json()
        live_usd = live_data.get("price", lbma_usd)

        fx = requests.get("https://api.exchangerate-api.com/v4/latest/USD", timeout=5).json()
        usd_to_aud = fx["rates"]["AUD"]

        lbma_aud = lbma_usd * usd_to_aud
        live_aud = live_usd * usd_to_aud

        return round(lbma_aud, 2), round(live_aud, 2)

    except:
        return 7000, 7050


# 📈 Chart
def get_chart_data(price):
    data = [price - i * 15 for i in range(15)]
    return pd.DataFrame({"Price": data[::-1]})


# 🤖 CRM Messages
def generate_message(customer, price, trend):
    name = customer["name"]
    if customer["type"] == "investor":
        return f"{name}, gold is {price} AUD. Trend: {trend}"
    elif customer["type"] == "jewellery":
        return f"{name}, great time to buy jewellery at {price} AUD!"
    else:
        return f"{name}, premium collection available 💎"


# 💬 Chatbot
def chatbot(user_input):
    text = user_input.lower()

    if "price" in text:
        return "📊 Check the dashboard above for latest gold prices."
    elif "buy" in text:
        return "📈 If price is below LBMA, it may be a good buying opportunity."
    elif "sell" in text:
        return "📉 If price is above LBMA, you may consider selling."
    else:
        return "Ask me about gold, buying, selling, or jewellery 💎"


# 🌐 UI
st.set_page_config(page_title="Jewellery CRM AI", layout="wide")

st.markdown("<h1 style='text-align:center;color:gold;'>💎 Jewellery CRM AI Dashboard</h1>", unsafe_allow_html=True)

# 💰 Prices
lbma_price, live_price = get_gold_prices()

col1, col2 = st.columns(2)
col1.metric("🏦 LBMA Price (AUD/oz)", lbma_price)
col2.metric("📊 Live Price (AUD/oz)", live_price)

# 📊 Market comparison
diff = live_price - lbma_price
if diff > 0:
    st.success(f"📈 Market ABOVE LBMA by {round(diff,2)} AUD")
else:
    st.warning(f"📉 Market BELOW LBMA by {round(diff,2)} AUD")

st.markdown("---")

# 📈 Chart
st.subheader("📈 Gold Price Trend")
df = get_chart_data(live_price)
fig = px.line(df, y="Price")
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# 🤖 CRM
st.subheader("🤖 CRM AI Agent")

if st.button("Run CRM Agent"):
    if "old_price" not in st.session_state:
        st.session_state.old_price = live_price

    old = st.session_state.old_price

    if live_price > old:
        trend = "📈 Increased"
    elif live_price < old:
        trend = "📉 Decreased"
    else:
        trend = "➖ Stable"

    for c in customers:
        st.success(generate_message(c, live_price, trend))

    st.session_state.old_price = live_price

st.markdown("---")

# 💬 Chatbot
st.subheader("💬 AI Chatbot")
user_input = st.text_input("Ask something:")

if user_input:
    st.info(chatbot(user_input))

st.markdown("---")

# 👥 Customers
st.subheader("👥 Customer Database")
st.table(customers)
