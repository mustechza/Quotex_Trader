import streamlit as st
from quotexapi_patch import Quotex  # Make sure this is in the same folder

st.set_page_config(page_title="Quotex Demo Trader", layout="centered")

st.title("📊 Quotex Demo Trading App")

# Ask user for Laravel session cookie
laravel_session = st.text_input("🔐 Enter your `laravel_session` cookie:", type="password")

# Optional asset and trade section
st.markdown("---")
st.subheader("📈 Trading Options")

asset = st.selectbox("Choose Asset", ["EURUSD", "USDJPY", "GBPUSD", "BTCUSD"])
amount = st.number_input("Enter amount to trade ($)", min_value=1.0, step=1.0, value=10.0)
direction = st.radio("Trade Direction", ["call", "put"])
duration = st.slider("Trade Duration (in seconds)", 30, 300, step=30)

if laravel_session:
    try:
        qx = Quotex(laravel_session=laravel_session)
        qx.connect()
        profile = qx.get_profile()

        st.success("✅ Successfully connected to Quotex Demo Account")
        st.write("👤 **Profile Info**:")
        st.json(profile)

        if st.button("📤 Execute Trade"):
            result = qx.buy(amount=amount, asset=asset, direction=direction, duration=duration)
            st.success("✅ Trade Executed")
            st.json(result)

    except Exception as e:
        st.error(f"❌ Failed to connect or trade: {e}")
else:
    st.warning("Please enter your `laravel_session` cookie to connect.")
