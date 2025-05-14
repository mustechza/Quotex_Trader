import streamlit as st
from quotexapi.stable_api import Quotex
import time

# App title
st.set_page_config(page_title="Quotex Trading App", layout="wide")
st.title("💹 Quotex Demo Trader")

# Sidebar for login
st.sidebar.header("🔐 Quotex Login")
laravel_session = st.sidebar.text_input("Enter your laravel_session cookie", type="password")

# Sidebar for trade settings
st.sidebar.header("⚙️ Trade Settings")
asset = st.sidebar.selectbox("Asset", ["EURUSD", "GBPUSD", "USDJPY", "BTCUSD"])
amount = st.sidebar.number_input("Amount ($)", value=1.0, step=0.1)
direction = st.sidebar.selectbox("Direction", ["call", "put"])
duration = st.sidebar.slider("Duration (minutes)", 1, 5, 1)

if st.sidebar.button("🚀 Start Trade"):
    if not laravel_session:
        st.error("❗ Please enter a valid laravel_session cookie.")
    else:
        try:
            # Login using the laravel_session cookie
            qx = Quotex()
            qx.set_session_cookie(laravel_session)
            account_info = qx.get_balance()
            st.success(f"✅ Logged in as Demo Account | Balance: ${account_info['balance']}")

            # Open trade
            st.info(f"Placing {direction.upper()} trade on {asset} for ${amount} over {duration} minute(s)...")
            success, result = qx.buy(amount=amount, asset=asset, direction=direction, duration=duration)

            if success:
                st.success(f"✅ Trade placed successfully! ID: {result['id']}")
            else:
                st.error("❌ Failed to place trade. Check parameters and try again.")
        except Exception as e:
            st.error(f"❌ Failed to connect or trade: {str(e)}")

# Footer
st.markdown("---")
st.markdown("Built with ❤️ using Streamlit and [QuotexAPI](https://github.com/ericpedra/QuotexAPI)")
