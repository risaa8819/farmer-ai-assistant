import streamlit as st
import requests
import json
import datetime
import re

# ==========================================
# 1. PAGE CONFIGURATION (Week 4)
# ==========================================
st.set_page_config(page_title="Twin AI", page_icon="🤖", layout="wide")

# ==========================================
# 2. WEEK 2: RAG (Vector Store & Retrieval)
# ==========================================
class TwinVectorStore:
    def __init__(self, chunk_size=40):
        self.chunk_size = chunk_size
        self.chunks = []
        self.index = {}

    def load_and_chunk(self, text):
        text = re.sub(r'\s+', ' ', text) 
        words = text.split()
        for i in range(0, len(words), self.chunk_size):
            chunk_text = " ".join(words[i:i + self.chunk_size])
            self.chunks.append(chunk_text)
        self._build_index()

    def _build_index(self):
        self.index = {}
        for idx, chunk in enumerate(self.chunks):
            for word in set(chunk.lower().split()):
                if word not in self.index:
                    self.index[word] = []
                self.index[word].append(idx)

    def search(self, query, top_k=2):
        query_words = re.sub(r'[^\w\s]', '', query.lower()).split()
        scores = {}
        for word in query_words:
            if word in self.index:
                for chunk_id in self.index[word]:
                    scores[chunk_id] = scores.get(chunk_id, 0) + 1
        sorted_chunks = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return [self.chunks[cid] for cid, score in sorted_chunks[:top_k]]

@st.cache_resource
def get_vector_store():
    store = TwinVectorStore(chunk_size=40)
    try:
        with open("twin_manual.txt", "r") as file:
            store.load_and_chunk(file.read())
    except FileNotFoundError:
        pass
    return store

vector_db = get_vector_store()

# ==========================================
# 3. WEEK 3: TOOLS (Tool Registry)
# ==========================================
def calculator(expression: str) -> dict:
    try:
        result = eval(expression) 
        return {'result': result}
    except Exception as e:
        return {'error': str(e)}

def get_time() -> dict:
    now = datetime.datetime.now()
    return {'time': now.strftime('%H:%M:%S')}

class ToolRegistry:
    def __init__(self): self.tools = {}
    def register(self, name, func, description):
        self.tools[name] = {'function': func, 'description': description}
    def get_tool(self, name): return self.tools[name]['function']
    def get_schema(self):
        schema = []
        for name, info in self.tools.items():
            schema.append({
                "type": "function",
                "function": {
                    "name": name,
                    "description": info['description'],
                    "parameters": {"type": "object", "properties": {"arg": {"type": "string"}}, "required": ["arg"]}
                }
            })
        return schema

tool_registry = ToolRegistry()
tool_registry.register('calculator', calculator, 'Calculate math expressions. Input should be a math string like "2+2".')
tool_registry.register('get_time', get_time, 'Get current time. Input is ignored.')

# ==========================================
# 4. THE AI BRAIN (Week 1 + 2 + 3 Combined)
# ==========================================
API_KEY = st.secrets["GROQ_API_KEY"]
BASE_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL_NAME = "openai/gpt-oss-120b"

def get_twin_response(prompt):
    retrieved_chunks = vector_db.search(prompt, top_k=2)
    context_text = "\n\n".join(retrieved_chunks)
    
    system_message = f"""You are a Digital Twin assistant. 
    Answer using the provided CONTEXT. If the user asks for math or time, use the tools.
    CONTEXT: {context_text}
    """

    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    
    payload = {
        "model": MODEL_NAME,
        "messages": [{"role": "system", "content": system_message}, {"role": "user", "content": prompt}],
        "tools": tool_registry.get_schema(),
        "tool_choice": "auto" 
    }
    
    try:
        response = requests.post(BASE_URL, headers=headers, json=payload)
        response.raise_for_status() 
        message = response.json()['choices'][0]['message']
        
        if message.get("tool_calls"):
            tool_call = message["tool_calls"][0]
            function_name = tool_call["function"]["name"]
            args = json.loads(tool_call["function"]["arguments"])
            tool_func = tool_registry.get_tool(function_name)
            
            if function_name == 'calculator':
                res = tool_func(args.get("arg", ""))
                return f"[Tool: Calculator] The result is {res.get('result')}."
            elif function_name == 'get_time':
                res = tool_func()
                return f"[Tool: Clock] The time is {res['time']}."
                
        return message["content"]
    except Exception as e:
        return f"⚠️ API Error: {str(e)}"

# ==========================================
# 5. STREAMLIT FRONTEND (Week 4)
# ==========================================
if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.header("👤 User Profile")
    # THE UNIQUE KEY IS HERE
    st.text_input("Name", value="Operator", key="unique_user_name_box")
    
    st.divider()
    st.header("⚙️ Settings")
    st.slider("AI Temperature", 0.0, 1.0, 0.7)
    
    st.divider()
    if st.button("🗑️ Clear Conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

st.title("🤖 Digital Twin Interface")

tab_chat, tab_stats = st.tabs(["💬 Chat", "📊 Stats Dashboard"])

with tab_chat:
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    if prompt := st.chat_input("Ask about the machine..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = get_twin_response(prompt) 
            st.write(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

with tab_stats:
    st.subheader("System Metrics")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Queries", len(st.session_state.messages) // 2)
    col2.metric("Model", MODEL_NAME)
    col3.metric("RAG Status", "Active", delta="Manual Loaded")
    
    st.divider()
    st.write("### RAG Database Inspector")
    st.write(f"Total Chunks in Memory: **{len(vector_db.chunks)}**")
    with st.expander("View Loaded Text Chunks"):
        for i, chunk in enumerate(vector_db.chunks):
            st.info(f"Chunk {i+1}: {chunk}")