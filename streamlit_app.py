import streamlit as st
from quotexapi.stable_api import Quotex
import time

# App title and layout
st.set_page_config(page_title="Quotex Demo Trader", layout="wide")
st.title("💹 Quotex Demo Trader")

# Sidebar: Authentication
st.sidebar.header("🔐 Quotex Login")
laravel_session = st.sidebar.text_input("Enter your laravel_session cookie", type="password")

# Sidebar: Trade Settings
st.sidebar.header("⚙️ Trade Settings")
asset = st.sidebar.selectbox("Asset", ["EURUSD", "GBPUSD", "USDJPY", "BTCUSD"])
amount = st.sidebar.number_input("Amount ($)", value=1.0, step=0.1)
direction = st.sidebar.selectbox("Direction", ["call", "put"])
duration = st.sidebar.slider("Duration (minutes)", 1, 5, 1)

# Trade button
if st.sidebar.button("🚀 Start Trade"):
    if not laravel_session:
        st.error("❗ Please enter a valid laravel_session cookie.")
    else:
        try:
            # Login using cookie
            qx = Quotex(session_cookies={"laravel_session": laravel_session})

            if not qx.check_connect():
                raise Exception("Login failed or invalid laravel_session cookie.")

            balance_info = qx.get_balance()
            st.success(f"✅ Logged in to Demo Account | Balance: ${balance_info['balance']}")

            # Open trade
            st.info(f"Placing {direction.upper()} trade on {asset} for ${amount} over {duration} minute(s)...")
            success, trade_data = qx.buy(amount=amount, asset=asset, direction=direction, duration=duration)

            if success:
                st.success(f"✅ Trade placed successfully! Trade ID: {trade_data['id']}")
            else:
                st.error("❌ Failed to place trade. Check trade settings or try again.")
        except Exception as e:
            st.error(f"❌ Failed to connect or trade: {str(e)}")

# Footer
st.markdown("---")
st.markdown("Built with ❤️ using Streamlit and [QuotexAPI by ericpedra](https://github.com/ericpedra/QuotexAPI)")
