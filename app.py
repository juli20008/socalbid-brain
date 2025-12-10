import streamlit as st
import google.generativeai as genai

# 1. Page Configuration
st.set_page_config(page_title="SoCalBid Assistant", page_icon="🤖")

# 2. Hide Streamlit Menu (Clean UI)
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.title("🤖 SoCalBid Assistant")

# 3. Secure API Key Retrieval
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("⚠️ API Key not found. Please configure GOOGLE_API_KEY in Streamlit Secrets.")
    st.stop()

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# 4. System Instructions (The Bot's Persona)
# I updated Rule #6 to enforce English.
system_instruction = """
You are a helpful and professional customer service assistant for 'SoCalBid', an online liquidation auction company based in City of Industry, CA.

Your rules:
1. **Location:** We are located in City of Industry, California.
2. **Pickup Only:** We do NOT offer shipping. All items must be picked up locally.
3. **Hours:** Pickup hours are Monday to Friday, 10:00 AM to 4:00 PM.
4. **Payments:** We accept Credit Cards online. No cash is accepted at the warehouse.
5. **Returns:** All items are sold "AS-IS". No returns or exchanges.
6. **Language:** ALWAYS answer in English unless the user specifically asks in another language.

If a user asks about something not listed here, kindly ask them to email contact@socalbid.com.
"""

# 5. Initialize Model
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=system_instruction
)

# 6. Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []
    # This is the Default English Greeting
    st.session_state.messages.append({"role": "assistant", "content": "Hello! I am your SoCalBid assistant. How can I help you with auctions, pickups, or payments today?"})

# 7. Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 8. Handle User Input
if prompt := st.chat_input("Type your question here..."):
    # Display user message
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # AI Response
    try:
        # Construct history for AI
        history_for_ai = [
            {"role": "user" if m["role"] == "user" else "model", "parts": [m["content"]]}
            for m in st.session_state.messages if m["role"] != "system"
        ]
        
        chat = model.start_chat(history=history_for_ai[:-1])
        response = chat.send_message(prompt)
        
        # Display AI message
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
        
    except Exception as e:
        st.error(f"Connection error: {e}")
