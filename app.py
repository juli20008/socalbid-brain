import streamlit as st
import google.generativeai as genai

# 1. 页面基本配置
st.set_page_config(page_title="SoCalBid Assistant", page_icon="🤖")

# 2. 隐藏 Streamlit 默认的菜单，让它看起来更像一个纯聊天窗口
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.title("🤖 SoCalBid 客服助手")

# 3. 获取 API Key (安全地从 Secrets 里读取)
# 如果没配置 Key，就提示用户
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("⚠️ 还没有配置 API Key。请在 Streamlit 的 Secrets 设置里添加 GOOGLE_API_KEY。")
    st.stop()

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# 4. 定义机器人的“人设” (System Instruction)
system_instruction = """
You are a helpful and professional customer service assistant for 'SoCalBid', an online liquidation auction company based in City of Industry, CA.

Your rules:
1. **Location:** We are located in City of Industry, California.
2. **Pickup Only:** We do NOT offer shipping. All items must be picked up locally.
3. **Hours:** Pickup hours are Monday to Friday, 10:00 AM to 4:00 PM.
4. **Payments:** We accept Credit Cards online. No cash is accepted at the warehouse.
5. **Returns:** All items are sold "AS-IS". No returns or exchanges.
6. **Language:** You can answer in English or Chinese (中文), depending on what language the user speaks.

If a user asks about something not listed here, kindly ask them to email contact@socalbid.com.
"""

# 5. 设置模型
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=system_instruction
)

# 6. 初始化聊天历史 (让 AI 记得住上下文)
if "messages" not in st.session_state:
    st.session_state.messages = []
    # 可以在这里加一句默认的开场白
    st.session_state.messages.append({"role": "assistant", "content": "您好！我是 SoCalBid 的智能助手。请问关于拍卖、取货或付款有什么可以帮您的？"})

# 7. 显示聊天记录
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 8. 处理用户输入
if prompt := st.chat_input("输入您的问题..."):
    # 显示用户的提问
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # AI 思考并回答
    try:
        # 把历史记录发给 AI
        history_for_ai = [
            {"role": "user" if m["role"] == "user" else "model", "parts": [m["content"]]}
            for m in st.session_state.messages if m["role"] != "system" # 过滤掉非标准角色
        ]
        
        chat = model.start_chat(history=history_for_ai[:-1]) # 排除最新的一条，防止重复
        response = chat.send_message(prompt)
        
        # 显示 AI 的回答
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
        
    except Exception as e:
        st.error(f"连接出错了，请稍后再试。错误信息: {e}")
