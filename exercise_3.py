



import streamlit as st
from datetime import datetime

st.title("💬 Chat Interface Exercise")

# 1. Initialize memory (Session State)
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# 5. Clear chat button in the sidebar
with st.sidebar:
    st.header("Options")
    if st.button("Clear Chat History"):
        st.session_state.chat_history = []
        st.rerun() # Refresh to clear the screen immediately

# 2. Display message history
# We loop through the memory and draw a chat bubble for each message
for msg in st.session_state.chat_history:
    # The st.chat_message automatically aligns left/right based on the role
    with st.chat_message(msg['role']):
        # Display the text
        st.write(msg['content'])
        # 4. Add timestamps (using st.caption makes it small and gray)
        st.caption(f"Sent at: {msg['time']}")

# 1. Chat input widget (and 3. Alternate user/bot messages)
# The := is the "walrus operator". It assigns the input to 'prompt' AND checks if it's not empty
if prompt := st.chat_input("Type your message here..."):
    
    # Get current time
    current_time = datetime.now().strftime("%H:%M:%S")
    
    # Save and display USER message
    user_msg = {"role": "user", "content": prompt, "time": current_time}
    st.session_state.chat_history.append(user_msg)
    
    # Display the user message immediately
    with st.chat_message("user"):
        st.write(prompt)
        st.caption(f"Sent at: {current_time}")
        
    # Save and display BOT message (Fake response for now)
    bot_msg = {"role": "assistant", "content": f"I am a bot. You said: {prompt}", "time": current_time}
    st.session_state.chat_history.append(bot_msg)
    
    # Display the bot message immediately
    with st.chat_message("assistant"):
        st.write(f"I am a bot. You said: {prompt}")
        st.caption(f"Sent at: {current_time}")