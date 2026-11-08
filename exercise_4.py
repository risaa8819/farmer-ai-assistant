### Exercise 3 (Intermediate): Chat Interface

#Task**: Build a simple chatbot UI
#Requirements**:
#1. Chat input widget
#2. Display message history
#3. Alternate user/bot messages
#4. Add timestamps
#5. Clear chat button in sidebar

import streamlit as st

# Professional look (Page Config)
st.set_page_config(page_title="Digital Twin Dashboard", page_icon="📊", layout="wide")
st.title("📊 Digital Twin Dashboard")

# 4. Sidebar with filters
with st.sidebar:
    st.header("Filters & Settings")
    time_range = st.selectbox("Select Time Range", ["Last 24 Hours", "Last 7 Days", "Last 30 Days"])
    st.write(f"Currently viewing data for: **{time_range}**")

# 1. 3 columns with st.metric()
col1, col2, col3 = st.columns(3)

with col1:
    # delta adds the little green/red arrow
    st.metric(label="System Status", value="Online", delta="0%")
with col2:
    st.metric(label="Avg Temperature", value="75 °F", delta="+2 °F")
with col3:
    st.metric(label="Pressure", value="120 PSI", delta="-5 PSI", delta_color="inverse")

st.divider()

# 2. Tabs for different views
tab1, tab2 = st.tabs(["📈 Main View", "⚙️ System Details"])

with tab1:
    st.subheader("System Overview")
    st.write("This is where your charts (like `st.line_chart`) would go.")
    
    # 3. Expander with details
    with st.expander("❓ What do these metrics mean?"):
        st.write("""
        - **System Status:** Whether the twin is actively receiving data.
        - **Avg Temperature:** The temperature reading from the main sensor.
        - **Pressure:** Current pressure in the primary valve.
        """)

with tab2:
    st.subheader("Raw Data")
    st.write("This tab could hold a table of raw sensor logs.")