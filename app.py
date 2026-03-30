import streamlit as st
import json
import base64

# =================================================
# PAGE CONFIG
# =================================================
st.set_page_config(
    page_title="GITAM Genie",
    page_icon="🧞‍♂️",
    layout="wide"
)

# =================================================
# BACKGROUND IMAGE FUNCTION
# =================================================
def set_bg(image_file):
    with open(image_file, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded}");
            background-size: cover;
            background-position: center;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# =================================================
# SESSION STATE
# =================================================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "messages" not in st.session_state:
    st.session_state.messages = []

if "user_type" not in st.session_state:
    st.session_state.user_type = "User"

# =================================================
# LOGIN PAGE (FULL SCREEN FIXED)
# =================================================
if not st.session_state.logged_in:
    set_bg("splash_screen.png")

    st.markdown("""
    <style>

    header[data-testid="stHeader"] {
        display: none;
    }

    .block-container {
        padding-top: 0rem !important;
    }

    .login-wrapper {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;

        display: flex;
        justify-content: center;
        align-items: center;

        z-index: 9999;
        overflow: hidden;
    }

    body {
        overflow: hidden;
    }

    .login-box {
        background: rgba(0, 0, 0, 0.55);
        backdrop-filter: blur(12px);
        padding: 40px;
        border-radius: 22px;
        width: 420px;
        box-shadow: 0 12px 40px rgba(0,0,0,0.45);
        text-align: center;
    }

    .login-box h2 {
        color: white;
    }

    .login-box p {
        color: #e0fffa;
        margin-bottom: 18px;
    }

    .login-box input {
        background: rgba(255,255,255,0.3) !important;
        color: black !important;
        border-radius: 12px !important;
        border: none;
        height: 44px !important;
    }

    .login-box input::placeholder {
        color: black !important;
    }

    label {
        display: none !important;
    }

    .stButton > button {
        background: linear-gradient(135deg, #0f6f61, #20c997);
        color: white !important;
        border-radius: 25px;
        width: 100%;
        padding: 10px;
        margin-top: 10px;
        font-weight: bold;
    }

    </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='login-wrapper'><div class='login-box'>", unsafe_allow_html=True)

    st.markdown("## 🔐 GITAM Genie Login")
    st.markdown("✨ Enter the lamp to awaken the Genie ✨")

    email = st.text_input("", placeholder="📧 Email")
    password = st.text_input("", placeholder="🔑 Password", type="password")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Enter the Lamp 🧞‍♂️"):
            if email and password:
                st.session_state.logged_in = True
                st.session_state.user_type = "User"
                st.rerun()
            else:
                st.error("Enter email & password")

    with col2:
        if st.button("Continue as Guest ✨"):
            st.session_state.logged_in = True
            st.session_state.user_type = "Guest"
            st.rerun()

    st.markdown("</div></div>", unsafe_allow_html=True)
    st.stop()

# =================================================
# LOAD KNOWLEDGE
# =================================================
try:
    with open("knowledge.json", "r", encoding="utf-8") as f:
        knowledge = json.load(f)
except:
    st.error("knowledge.json missing")
    st.stop()

# =================================================
# FAST RESPONSE ENGINE
# =================================================
FAST_KB = []
for item in knowledge.values():
    for kw in item["keywords"]:
        FAST_KB.append((kw.lower(), item))

def get_response(user_input):
    q = user_input.lower()
    for kw, item in FAST_KB:
        if kw in q:
            return f"{item['response']}\n\n🔗 Source: {item['source']}"
    return "🧞‍♂️ I couldn’t find that. Try Library, Transport, Courses, or Hostel."

# =================================================
# MAIN UI STYLE
# =================================================
st.markdown("""
<style>

.stApp {
    background: radial-gradient(circle at top, #c8f3ec, #eafaf7);
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #063f38, #0f6f61);
}
section[data-testid="stSidebar"] * {
    color: white !important;
}

footer {visibility: hidden;}

</style>
""", unsafe_allow_html=True)

# =================================================
# SIDEBAR
# =================================================
with st.sidebar:
    st.markdown("## 🧞‍♂️ GITAM Genie")
    st.markdown("*Your campus assistant* ✨")

    if st.session_state.user_type == "Guest":
        st.info("Guest Mode")

    st.markdown("---")
    st.write("🚌 Bus Timings")
    st.write("Gajuwaka – 7:35 AM")
    st.write("NAD – 7:55 AM")
    st.write("RTC – 8:00 AM")

    if st.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.session_state.messages = []
        st.rerun()

# =================================================
# MAIN TITLE
# =================================================
st.markdown("<h1 style='text-align:center;color:#0f6f61;'>🧞‍♂️ GITAM Genie</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>✨ Ask anything about campus ✨</p>", unsafe_allow_html=True)

# =================================================
# QUICK BUTTONS
# =================================================
col1, col2, col3, col4 = st.columns(4)

if col1.button("📚 Library"):
    st.session_state.messages.append({"role": "assistant", "content": get_response("library")})

if col2.button("🚌 Transport"):
    st.session_state.messages.append({"role": "assistant", "content": get_response("bus")})

if col3.button("🎓 Courses"):
    st.session_state.messages.append({"role": "assistant", "content": get_response("courses")})

if col4.button("🏠 Hostel"):
    st.session_state.messages.append({"role": "assistant", "content": get_response("hostel")})

st.markdown("---")

# =================================================
# CHAT
# =================================================
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

prompt = st.chat_input("Ask your question...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    reply = get_response(prompt)
    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.rerun()
