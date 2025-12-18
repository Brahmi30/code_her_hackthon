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
# LOGIN PAGE
# =================================================
if not st.session_state.logged_in:
    set_bg("splash_screen.png")

    st.markdown("""
    <style>

    header[data-testid="stHeader"] {
        background: transparent !important;
    }

    .block-container {
        padding-top: 0rem !important;
    }

    .login-wrapper {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
    }

    .login-box {
        background: rgba(0, 0, 0, 0.55);
        padding: 36px;
        border-radius: 22px;
        width: 420px;
        box-shadow: 0 12px 40px rgba(0,0,0,0.45);
        text-align: center;
    }

    .login-box h2 {
        color: #ffffff;
    }

    .login-box p {
        color: #e0fffa;
        margin-bottom: 18px;
    }

    /* Glass input boxes */
    .login-box input {
        background: rgba(255,255,255,0.28) !important;
        color: #000000 !important;
        backdrop-filter: blur(12px);
        border-radius: 14px !important;
        border: 1.5px solid rgba(255,255,255,0.7);
        height: 44px !important;
        font-size: 15px !important;
    }

    .login-box input::placeholder {
        color: #000000 !important;
        opacity: 0.75;
    }

    label {
        display: none !important;
    }

    .stButton > button {
        background: linear-gradient(135deg, #0f6f61, #20c997);
        color: white !important;
        border-radius: 26px;
        font-weight: bold;
        width: 100%;
        padding: 10px;
        margin-top: 10px;
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
                st.error("Please enter email and password")

    with col2:
        if st.button("Continue as Guest ✨"):
            st.session_state.logged_in = True
            st.session_state.user_type = "Guest"
            st.rerun()

    st.markdown("</div></div>", unsafe_allow_html=True)
    st.stop()

# =================================================
# LOAD KNOWLEDGE BASE
# =================================================
try:
    with open("knowledge.json", "r", encoding="utf-8") as f:
        knowledge = json.load(f)
except Exception as e:
    st.error(f"Error loading knowledge.json: {e}")
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
            return f"""{item["response"]}

🔗 Source: {item["source"]}"""
    return "🧞‍♂️ I couldn’t find that in my scrolls. Try Library, Transport, Courses, or Hostel."

# =================================================
# MAIN THEME
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

h1 {
    color: #0f6f61;
}

.magic-text {
    font-size: 18px;
    color: #0f6f61;
    animation: glow 2s infinite alternate;
}

@keyframes glow {
    from { text-shadow: 0 0 6px #7fffd4; }
    to { text-shadow: 0 0 14px #20c997; }
}

/* Chat bubbles */
div[data-testid="stChatMessage"][data-role="assistant"] {
    background: #ffffff !important;
    border-left: 6px solid #20c997;
    border-radius: 18px;
    padding: 14px;
    max-width: 75%;
}

div[data-testid="stChatMessage"][data-role="user"] {
    background: #dff3ef !important;
    border-right: 6px solid #0f6f61;
    border-radius: 18px;
    padding: 14px;
    margin-left: auto;
    max-width: 75%;
}

/* Force text black */
div[data-testid="stChatMessage"] * {
    color: #000000 !important;
}

/* Input */
div[data-testid="stChatInput"] textarea {
    background: white;
    color: black !important;
    border-radius: 22px;
    border: 2px solid #20c997;
}
div[data-testid="stChatInput"] textarea::placeholder {
    color: black !important;
    opacity: 0.6;
}

footer {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)

# =================================================
# SIDEBAR
# =================================================
with st.sidebar:
    st.markdown("## 🧞‍♂️ GITAM Genie")
    st.markdown("*Your magical university assistant* ✨")

    if st.session_state.user_type == "Guest":
        st.info("👤 Guest Mode")

    st.markdown("---")
    st.markdown("### 🚌 Bus Timings (Vizag)")
    st.write("Gajuwaka – **7:35 AM**")
    st.write("NAD X Roads – **7:55 AM**")
    st.write("RTC Complex – **8:00 AM**")

    if st.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.session_state.messages = []
        st.rerun()

# =================================================
# MAIN CHAT UI
# =================================================
st.markdown("""
<style>
.genie-text {
    font-size: 42px;
    font-weight: 800;
    color: #000000;
    text-align: center;
    text-shadow:
        0 0 6px #7fffd4,
        0 0 12px #20c997,
        0 0 20px #20c997;
    animation: glow 2s infinite alternate;
}

@keyframes glow {
    from {
        text-shadow:
            0 0 4px #7fffd4,
            0 0 8px #20c997;
    }
    to {
        text-shadow:
            0 0 10px #7fffd4,
            0 0 20px #20c997,
            0 0 30px #20c997;
    }
}
</style>

<div class="genie-text">
    🧞‍♂️ GITAM Genie
</div>
""", unsafe_allow_html=True)

st.markdown("<div class='magic-text'>✨ The Genie is awake. Ask your question… ✨</div>", unsafe_allow_html=True)

st.markdown("<h3 style='color:black;'>Quick Questions 👇</h3>", unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)

with c1:
    if st.button("📚 Library"):
        st.session_state.messages.append({"role": "assistant", "content": get_response("library")})
with c2:
    if st.button("🚌 Transport"):
        st.session_state.messages.append({"role": "assistant", "content": get_response("bus gajuwaka nad")})
with c3:
    if st.button("🎓 Courses"):
        st.session_state.messages.append({"role": "assistant", "content": get_response("courses")})
with c4:
    if st.button("🏠 Hostel"):
        st.session_state.messages.append({"role": "assistant", "content": get_response("hostel")})

st.markdown("---")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# =================================================
# CHAT INPUT (INSTANT RESPONSE)
# =================================================
prompt = st.chat_input("Ask the Genie anything about GITAM University")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    response = get_response(prompt)
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()
