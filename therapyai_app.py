import streamlit as st
import os
import google.generativeai as genai

# 💎 Your Gemini API Key
GEMINI_API_KEY = st.secrets["gemini"]["api_key"]
genai.configure(api_key=GEMINI_API_KEY)

# 🎯 Page Configuration
st.set_page_config(page_title="TherAI Chatbot", page_icon="💖", layout="centered")

# 💅 Custom CSS
st.markdown("""
<style>
body {
    background-color: #fef6f9;
    font-family: 'Segoe UI', sans-serif;
    color: #5c5470;
}
.main {
    background: linear-gradient(135deg, #fff0f6, #f0e7ff);
    border-radius: 24px;
    padding: 40px;
    margin-top: 30px;
    box-shadow: 0 10px 25px rgba(200, 160, 255, 0.25);
}
.stTextInput>div>div>input {
    background: #fff5fb;
    color: #6a4e77;
    border-radius: 14px;
    border: 1.5px solid #d3b9ff;
    padding: 14px;
    font-size: 17px;
    transition: box-shadow 0.3s ease;
}
.stTextInput>div>div>input:focus {
    box-shadow: 0 0 0 3px #e7d6ff;
    border: 1.5px solid #bb91f0;
}
.stButton>button {
    background: linear-gradient(135deg, #e8d0ff, #ffc2e0);
    color: #4a405f;
    border-radius: 10px;
    border: none;
    font-size: 16px;
    padding: 12px 20px;
    margin-top: 10px;
    font-weight: 600;
    transition: all 0.3s ease-in-out;
}
.stButton>button:hover {
    transform: scale(1.03);
    box-shadow: 0 0 10px rgba(238, 179, 255, 0.6);
}
.bubble-user, .bubble-bot {
    padding: 16px 22px;
    border-radius: 20px;
    margin: 12px 0;
    font-size: 16px;
    line-height: 1.5;
    animation: softFadeIn 0.4s ease-out;
    max-width: 90%;
}
.bubble-user {
    background: #ffd8eb;
    color: #5c3d58;
    align-self: flex-end;
    border-left: 4px solid #ffaad4;
}
.bubble-bot {
    background: #d9cfff;
    color: #4e3f6b;
    align-self: flex-start;
    border-left: 4px solid #bca6ff;
}
.message-container {
    display: flex;
    flex-direction: column;
    gap: 10px;
}
.message-box {
    margin-top: 15px;
    padding: 24px;
    border-radius: 18px;
    border: 2px dashed #decafc;
    background-color: #f2e6f7;  /* Softer light lavender */
    box-shadow: 0 0 12px rgba(200, 150, 255, 0.2); /* Less intense shadow */
}

@keyframes softFadeIn {
    from { opacity: 0; transform: translateY(8px); }
    to { opacity: 1; transform: translateY(0); }
}
</style>
""", unsafe_allow_html=True)


# ✨ Title with Emotion Recognition Teaser
st.markdown(f"""
<style>
@keyframes glowWave {{
  0%, 100% {{ text-shadow: 0 0 5px #ff44aa55; transform: translateY(0); }}
  50% {{ text-shadow: 0 0 15px #ff44aa, 0 0 25px #ff44aa88; transform: translateY(-5px); }}
}}
.animated-title {{
  display: flex;
  justify-content: center;
  font-size: 2.5rem;
  font-weight: bold;
  margin-bottom: 10px;
  color: #ff44aa;
}}
.animated-title span {{
  animation: glowWave 1.5s ease-in-out infinite;
  display: inline-block;
  white-space: pre;
}}
{''.join(f".animated-title span:nth-child({i}) {{ animation-delay: {i * 0.08:.2f}s; }}" for i in range(1, len("💬 Chat with TherAI") + 1))}
</style>
<h1 class='animated-title'>{''.join(f"<span>{c}</span>" for c in "💬 Chat with TherAI")}</h1>
<h4 style='text-align:center; color: #aaa;'>🧠 Emotion Recognition: <i>Coming soon...</i></h4>
""", unsafe_allow_html=True)

# 🌈 Chat Initialization
if "chat" not in st.session_state:
    model = genai.GenerativeModel("gemini-1.5-flash")
    st.session_state.chat = model.start_chat(history=[{
        "role": "user",
        "parts": ["""
You are TherAI — a calm, emotionally intelligent virtual therapist who blends mental health support with gentle Gen-Z flair. You speak like a caring, relatable friend, but you're grounded in real therapy-backed knowledge. You create a safe, judgment-free space for anyone who needs to vent, reflect, or feel seen.

Guidelines:
- Prioritize emotional support, validation, and understanding.
- Always listen first, and respond with warmth and encouragement.
- Use soft Gen-Z energy: emojis, relatable phrasing, modern slang — but keep it soothing, not chaotic.
- Avoid gender assumptions. Speak inclusively.
- Gently suggest coping tools, reframing techniques, or grounding exercises when needed.
- Don’t use terms like “bestie” or overwhelm users with too many emojis.
- Act like a digital safe space: calm, kind, always there when someone needs to talk.
"""]
    }])

# 🤖 Get Response Function
def get_gemini_response(message: str):
    try:
        response = st.session_state.chat.send_message(message)
        return response.text.strip()
    except Exception as e:
        return f"Error from Gemini API: {str(e)}"

# 💾 History
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 📥 User Input
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("Type your message:", key="input")
    submitted = st.form_submit_button("💌 Send")

# ✨ Get & Save Replies
if submitted and user_input:
    st.session_state.chat_history.append(("You", user_input))
    bot_reply = get_gemini_response(user_input)
    st.session_state.chat_history.append(("TherAI", bot_reply))

# 📜 Chat UI
st.markdown("<div class='main'><div class='message-container'>", unsafe_allow_html=True)

for i in reversed(range(0, len(st.session_state.chat_history), 2)):
    user_message = st.session_state.chat_history[i][1]
    bot_message = st.session_state.chat_history[i + 1][1] if i + 1 < len(st.session_state.chat_history) else ""
    st.markdown(f"""
        <div class='message-box'>
            <div class='bubble-user'><strong>You:</strong><br>{user_message}</div>
            <div class='bubble-bot'><strong>TherAI:</strong><br>{bot_message}</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("</div></div>", unsafe_allow_html=True)
