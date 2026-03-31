import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# 👥 Customer database
customers = [
    {"name": "Raj", "type": "investor"},
    {"name": "Simran", "type": "jewellery"},
    {"name": "Aman", "type": "premium"}
]

# 🏦 Gold price function (LBMA + Live + AUD)
def get_gold_prices():
    try:
        API_KEY = "4KVSTHP9F0JGINOUGLVR137OUGLVR"

        # LBMA price (USD per ounce)
        lbma_url = f"https://api.metals.dev/v1/metal/authority?api_key={4KVSTHP9F0JGINOUGLVR137OUGLVR}&authority=lbma&currency=USD&unit=toz"
        lbma_data = requests.get(lbma_url, timeout=5).json()
        lbma_usd = lbma_data["rates"]["lbma_gold_pm"]

        # Live price (USD per ounce)
        live_url = "https://api.gold-api.com/price/XAU"
        live_data = requests.get(live_url, timeout=5).json()
        live_usd = live_data.get("price", lbma_usd)

        # USD → AUD
        fx = requests.get("https://api.exchangerate-api.com/v4/latest/USD", timeout=5).json()
        usd_to_aud = fx["rates"]["AUD"]

        lbma_aud = lbma_usd * usd_to_aud
        live_aud = live_usd * usd_to_aud

        return round(lbma_aud, 2), round(live_aud, 2)

    except:
        return 7000, 7050


# 📈 Chart data (demo)
def get_chart_data(price):
    data = []
    for i in range(15):
        data.append(price - (i * 15))
    df = pd.DataFrame({"Price": data[::-1]})
    return df


# 🤖 CRM Message Generator
def generate_message(customer, price, trend):
    name = customer["name"]
    ctype = customer["type"]

    if ctype == "investor":
        return f"Hello {name} 💰, gold is {price} AUD. Trend: {trend}"
    elif ctype == "jewellery":
        return f"Hi {name} 💍, great time to buy jewellery at {price} AUD!"
    else:
        return f"Dear {name} 👑, premium collection available at {price} AUD."


# 💬 Simple AI Chatbot
def chatbot(user_input):
    user_input = user_input.lower()

    if "price" in user_input:
        return "📊 Check the dashboard above for latest gold prices."
    elif "buy" in user_input:
        return "📈 If price is below LBMA, it may be a good buying opportunity."
    elif "sell" in user_input:
        return "📉 If price is above LBMA, you may consider selling."
    elif "hello" in user_input:
        return "Hello! I can help with gold prices and jewellery advice 💎"
    else:
        return "Ask me about gold price, buying, selling, or jewellery 💎"


# 🌐 UI START
st.set_page_config(page_title="Jewellery CRM AI", layout="wide")

st.markdown("""
    <h1 style='text-align:center; color:gold;'>💎 Jewellery CRM AI Dashboard</h1>
    <hr>
""", unsafe_allow_html=True)

# 💰 Prices
lbma_price, live_price = get_gold_prices()

col1, col2 = st.columns(2)

col1.metric("🏦 LBMA Price (AUD/oz)", lbma_price)
col2.metric("📊 Live Market Price (AUD/oz)", live_price)

# 📈 Market comparison
difference = live_price - lbma_price

if difference > 0:
    st.success(f"📈 Market ABOVE LBMA by {round(difference,2)} AUD")
else:
    st.warning(f"📉 Market BELOW LBMA by {round(difference,2)} AUD")

st.markdown("---")

# 📈 Chart
st.subheader("📈 Gold Price Trend")
df = get_chart_data(live_price)
fig = px.line(df, y="Price", title="Gold Trend (Demo)")
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# 🤖 CRM Agent
st.subheader("🤖 CRM AI Agent")

if st.button("🚀 Run CRM Agent"):
    st.write("### 📩 Customer Messages")

    if "old_price" not in st.session_state:
        st.session_state.old_price = live_price

    old_price = st.session_state.old_price

    if live_price < old_price:
        trend = "📉 Decreased"
    elif live_price > old_price:
        trend = "📈 Increased"
    else:
        trend = "➖ Stable"

    st.info(f"Market Trend: {trend}")

    for c in customers:
        msg = generate_message(c, live_price, trend)
        st.success(f"👤 {c['name']}: {msg}")

    st.session_state.old_price = live_price

st.markdown("---")

# 💬 Chatbot
st.subheader("💬 AI Chatbot")

user_input = st.text_input("Ask something about gold or jewellery:")

if user_input:
    response = chatbot(user_input)
    st.info(response)

st.markdown("---")

# 👥 Customer table
st.subheader("👥 Customer Database")
st.table(customers)

    # 🔄 Update price memory
    st.session_state.old_price = live_price
