app.py
import streamlit as st
import requests

# 👥 Customer database
customers = [
    {"name": "Raj", "phone": "+91-9999999999", "interest": "gold", "type": "investor"},
    {"name": "Simran", "phone": "+91-8888888888", "interest": "gold", "type": "jewellery"},
    {"name": "Aman", "phone": "+91-7777777777", "interest": "gold", "type": "premium"}
]

# 🏦 + 📊 Gold prices (LBMA + Live)
def get_gold_prices():
    try:
        API_KEY = "4KVSTHP9F0JGINOUGLVR137OUGLVR"

        # LBMA price (USD/ounce)
        lbma_url = f"https://api.metals.dev/v1/metal/authority?api_key={API_KEY}&authority=lbma&currency=USD&unit=toz"
        lbma_data = requests.get(lbma_url, timeout=5).json()
        lbma_usd = lbma_data["rates"]["lbma_gold_pm"]

        # Live price (USD/ounce)
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

# ✨ Message generator
def generate_message(customer, price, trend):
    name = customer["name"]
    ctype = customer["type"]

    if ctype == "investor":
        return f"Hello {name} 💰, gold is {price} AUD. Good investment time!"
    elif ctype == "jewellery":
        return f"Hi {name} 💍, great time to buy jewellery at {price} AUD!"
    else:
        return f"Dear {name} 👑, premium collection available at {price} AUD."

# 🌐 UI
st.set_page_config(page_title="Jewellery CRM AI", layout="wide")
st.title("💎 Jewellery CRM AI Website")

# 📊 Prices
lbma_price, live_price = get_gold_prices()

st.subheader("💰 Gold Price Comparison (AUD per ounce)")
st.write(f"🏦 LBMA Price: {lbma_price} AUD/oz")
st.write(f"📊 Live Price: {live_price} AUD/oz")

difference = live_price - lbma_price
st.write(f"📈 Difference: {round(difference,2)} AUD")

# 📈 Market signal
if live_price > lbma_price:
    st.success("📈 Market is ABOVE LBMA → Strong demand")
else:
    st.warning("📉 Market is BELOW LBMA → Weak demand")

# 🤖 CRM Agent Button
if st.button("🚀 Run CRM AI Agent"):
    st.write("🤖 Running AI...\n")

    # 🧠 Price memory
    if "old_price" not in st.session_state:
        st.session_state.old_price = live_price

    old_price = st.session_state.old_price

    # 📊 Trend detection
    if live_price < old_price:
        trend = "decreased"
    elif live_price > old_price:
        trend = "increased"
    else:
        trend = "stable"

    # 📩 Send messages
    for c in customers:
        msg = generate_message(c, live_price, trend)
        st.success(f"📩 {c['name']}: {msg}")

    # 🔄 Update price memory
    st.session_state.old_price = live_price
