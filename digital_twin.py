import streamlit as st
import time

# --- 1. PAGE CONFIG ---
st.set_page_config(page_title="Digital Twin", page_icon="🤖", layout="wide")
st.title("🤖 Digital Twin Dashboard")

# --- PART 4: LAYOUT ---
# Create two columns. The left is twice as wide as the right.
col_left, col_right = st.columns([2, 1])

with col_left:
    st.header("💬 Main Chat Area")
    st.write("This wide column is where the chat interface will go.")
    
    # A simple chat input to test the layout
    prompt = st.chat_input("Ask your twin...")
    if prompt:
        st.chat_message("user").write(prompt)
        st.chat_message("assistant").write("I am a digital twin.")

with col_right:
    st.header("⚙️ Controls")
    
    # --- PART 5: EXPANDERS & UI/UX ---
    
    # 1. Expander (Collapsible Content)
    with st.expander("❓ Help & Info"):
        st.write("This content is hidden by default to save space.")
        
    # 2. Slider
    st.slider("Max Tokens", 100, 2000, 500)
    
    # 3. Loading State (Spinner) and Error Handling
    if st.button("Run Diagnostics"):
        try:
            # Show a spinner while the "AI" is thinking
            with st.spinner("Analyzing data..."):
                time.sleep(2) # Pretend to do heavy processing
                
            # Show success message
            st.success("Diagnostics Complete!")
            
        except Exception as e:
            # Show error message if something fails
            st.error(f"Error: {e}")