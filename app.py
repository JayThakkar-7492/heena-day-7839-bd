import streamlit as st
import pandas as pd
import time
from datetime import date

# --- CONFIGURATION ---
# Updated to August 1st, 2026
TARGET_DATE = pd.Timestamp("2026-08-01 00:00:00").tz_localize('Asia/Kolkata')
TITLE = "Countdown to your birthday 🎂"
VALID_USER = "Heena"
VALID_PASS = "Heena@123"

# Set page config at the very top
st.set_page_config(page_title="Countdown", layout="centered")

def main():
    # Initialize the "gate"
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    # Create a single placeholder for the entire app content
    main_placeholder = st.empty()

    # --- LOGIN SCREEN ---
    if not st.session_state["authenticated"]:
        with main_placeholder.container():
            st.title("🔒 Private Access")
            user_input = st.text_input("User ID", key="user_login")
            pass_input = st.text_input("Password", type="password", key="pass_login")
            
            if st.button("Login"):
                if user_input == VALID_USER and pass_input == VALID_PASS:
                    st.session_state["authenticated"] = True
                    # This clears the login UI immediately
                    main_placeholder.empty()
                    st.rerun()
                else:
                    st.error("Invalid User ID or Password")

    # --- TIMER SCREEN ---
    if st.session_state["authenticated"]:
        # Custom CSS for the UI
        st.markdown("""
            <style>
            .timer-card {
                background: linear-gradient(135deg, #ff9a9e 0%, #fad0c4 99%, #fad0c4 100%);
                padding: 40px;
                border-radius: 25px;
                color: #4a4a4a;
                text-align: center;
                box-shadow: 0px 10px 30px rgba(0,0,0,0.1);
                margin-top: 20px;
            }
            .title { font-size: 28px; font-weight: bold; margin-bottom: 20px; }
            .time-display { font-size: 38px; font-weight: 800; color: #ff5e62; font-family: monospace; }
            </style>
        """, unsafe_allow_html=True)

        # Start the live update loop
        while True:
            now = pd.Timestamp.now(tz='Asia/Kolkata')
            diff = TARGET_DATE - now

            if diff.total_seconds() <= 0:
                main_placeholder.markdown(f"""
                    <div class="timer-card">
                        <div class="title">{TITLE}</div>
                        <div class="time-display">The Wait is Over! ❤️</div>
                    </div>
                """, unsafe_allow_html=True)
                break
            
            days = diff.days
            hours, remainder = divmod(diff.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)

            # Update the main placeholder with the timer card
            # NOTE: I changed the 'until' line to dynamically show the target month/day
            main_placeholder.markdown(f"""
                <div class="timer-card">
                    <div class="title">{TITLE}</div>
                    <div class="time-display">
                        {days}d {hours:02d}h {minutes:02d}m {seconds:02d}s
                    </div>
                    <div style="margin-top:10px; opacity:0.7;">
                        until {TARGET_DATE.strftime('%B %d, %Y')}
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            time.sleep(1)

if __name__ == "__main__":
    main()
