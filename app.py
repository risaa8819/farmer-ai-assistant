
## 🏆 Challenge Project
#Build a Production-Ready Digital Twin Interface**

#Create a complete web application that:
#1. Has a professional, polished UI
#2. Integrates your Week 1-3 digital twin
#3. Includes all UI/UX best practices
#4. Works beautifully on mobile
#5. Has error handling and loading states
#6. Shows usage statistics
#7. Allows user customization

#**Bonus Features**:
#- Dark/light mode toggle
#- Export chat history
#- Voice input (using browser APIs)
#- Multilingual support
#- Accessibility features

#           I'M CHOOSING TO BUILD A DIGITAL TWIN FOR AGRICULTURE
# 🌾 Agricultural advice chatbot (local language)

#*Success Criteria**:
#- ✅ Works on mobile (test on actual phone)
#- ✅ Loads in < 3 seconds
#- ✅ Handles errors gracefully
#- ✅ Professional appearance
#- ✅ Ready to share with real users

#IMPORT NECESSARY LIBRARIES

import streamlit as st
import requests
import json
import datetime 
import re 

# ==========================================
# PHASE 1: SETUP & PAGE CONFIG
# ==========================================
# layout="wide" makes it look professional and mobile-friendly
st.set_page_config(page_title="Production Twin", page_icon="🤖", layout="wide")

#==========================================
# PHASE 2: STATE & CUSTOMIZATION
# ==========================================
# Initialize memory so it doesn't reset on every click
if "messages" not in st.session_state:
    st.session_state.messages = []
if "user_name" not in st.session_state:
    st.session_state.user_name = "Operator"

# ==========================================
# SIDEBAR: USER CUSTOMIZATION & EXPORT
# ==========================================
with st.sidebar:
    st.header("👤 User Profile")
    st.session_state.user_name = st.text_input("Your Name", value=st.session_state.user_name)
    
    st.divider()
    st.header("⚙️ Settings")
    # Requirement 7: User Customization
    language = st.selectbox("AI Language", ["English", "Swahili"])
    ai_temperature = st.slider("AI Temperature (Creativity)", 0.0, 1.0, 0.7)
    
    st.divider()
    # BONUS: Export Chat History
    if st.button("📥 Export Chat History", use_container_width=True):
        if st.session_state.messages:
            chat_text = "\n".join([f"{m['role'].capitalize()}: {m['content']}" for m in st.session_state.messages])
            st.download_button(
                label="Download as .txt",
                data=chat_text,
                file_name="twin_chat_history.txt",
                mime="text/plain"
            )
    
    # Clear Chat
    if st.button("🗑️ Clear Conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# ==========================================
# PHASE 3: THE AI BACKEND (Week 1, 2, 3)
# ==========================================
API_KEY = st.secrets["GROQ_API_KEY"]
BASE_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL_NAME = "openai/gpt-oss-120b"

def get_twin_response(prompt, temp, lang):
    # Week 2: Simple RAG
    context = ""
    try:
        with open("agri_manual.txt", "r") as file:
            context = file.read()
    except FileNotFoundError:
        pass

    # Week 1 & Week 3: System Prompt & Tool Definition
    system_message = f"""You are a Digital Twin assistant. 
    Answer in {lang}. Use the CONTEXT to answer. 
    CONTEXT: {context}
    """
    
    # Week 3: Tools (Simplified for this standalone app)
    tools = [{
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "Calculate math",
            "parameters": {"type": "object", "properties": {"arg": {"type": "string"}}, "required": ["arg"]}
        }
    }]

    payload = {
        "model": MODEL_NAME,
        "messages": [{"role": "system", "content": system_message}, {"role": "user", "content": prompt}],
        "tools": tools,
        "temperature": temp
    }

    # Phase 4: Error Handling (Wrapped in try/except)
    try:
        response = requests.post(BASE_URL, headers={"Authorization": f"Bearer {API_KEY}"}, json=payload)
        response.raise_for_status()
        message = response.json()['choices'][0]['message']
        
        # Handle tool use
        if message.get("tool_calls"):
            args = json.loads(message["tool_calls"][0]["function"]["arguments"])
            calc_res = eval(args.get("arg", ""))
            return f"The result is {calc_res}."
            
        return message["content"]
    except Exception as e:
        return f"⚠️ System Error: {str(e)}"

# ==========================================
# MAIN PAGE: TABS (Requirement 1 & 6)
# ==========================================
st.markdown("<h1 style='color: #388E3C;'>🌾 AgriTwin AI Assistant</h1>", unsafe_allow_html=True)

tab_chat, tab_stats = st.tabs(["💬 Chat Interface", "📊 System Dashboard"])

# --- TAB 1: THE CHAT ---
with tab_chat:
    # Display chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # Chat Input
    if prompt := st.chat_input("Ask your Digital Twin..."):
        # Save user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        # Call AI with Loading State (Phase 4)
        with st.chat_message("assistant"):
            with st.spinner("Processing your request..."):
                response = get_twin_response(prompt, ai_temperature, language)
            st.write(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

# --- TAB 2: THE DASHBOARD ---
with tab_stats:
    st.header("Usage Statistics")
    
    # Calculate metrics based on the memory
    total_messages = len(st.session_state.messages)
    total_queries = total_messages // 2
    
    # Display Metrics in Columns (Professional UI)
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Queries", total_queries)
    col2.metric("Active User", st.session_state.user_name)
    col3.metric("Language", language)
    
    st.divider()
    
    # BONUS: Accessibility & Advanced Features (Placeholders)
    st.subheader("Appearance & Accessibility")
    st.info("Streamlit automatically supports Dark/Light mode based on your browser settings. Use the menu in the top right to change it.")
    
    # Simple text analysis of chat
    if total_messages > 0:
        st.subheader("Chat Volume")
        st.write(f"Your chat history is taking up roughly **{total_messages * 50}** bytes of memory.")
    else:
        st.info("Start chatting to generate statistics!")
