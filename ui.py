import os

import streamlit as st
import requests
import pandas as pd
import altair as alt

# When deployed, set API_URL to the backend's public URL (e.g., Render service URL).
# Locally, it defaults to localhost:8000.
API = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(page_title="Adaptive Learning System", layout="centered")
st.title("📘 Adaptive Learning System")

# Custom CSS for better UI
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 10px 20px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 12px;
        transition: background-color 0.3s;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .stRadio > div {
        background-color: rgba(255, 255, 255, 0.1);
        padding: 10px;
        border-radius: 8px;
    }
    .stSubheader {
        color: #FFD700;
        font-weight: bold;
    }
    .stProgress > div > div > div {
        background-color: #FFD700;
    }
    .stSuccess {
        background-color: rgba(76, 175, 80, 0.2);
        color: #4CAF50;
        border: 1px solid #4CAF50;
        border-radius: 8px;
        padding: 10px;
    }
    .stError {
        background-color: rgba(244, 67, 54, 0.2);
        color: #F44336;
        border: 1px solid #F44336;
        border-radius: 8px;
        padding: 10px;
    }
    .stWarning {
        background-color: rgba(255, 152, 0, 0.2);
        color: #FF9800;
        border: 1px solid #FF9800;
        border-radius: 8px;
        padding: 10px;
    }
    .css-1d391kg {  /* Sidebar */
        background-color: rgba(0, 0, 0, 0.1);
    }
    .css-1lcbmhc {  /* Main content */
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        padding: 20px;
    }
    .sidebar-text {
        color: #FFD700;
        font-size: 18px;
        font-weight: bold;
    }
    .welcome-text {
        color: #FF69B4;
        font-size: 20px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# STEP 1: ENTER NAME
# -----------------------------
user = st.text_input("👤 Enter Your Name")

# Welcome message
if user:
    st.markdown(f'<p class="welcome-text">Welcome, {user}! Ready to learn? 🚀</p>', unsafe_allow_html=True)

# Initialize session state defaults (required before any use)
if "user_exists" not in st.session_state:
    st.session_state.user_exists = False
if "user_created" not in st.session_state:
    st.session_state.user_created = False
if "user_missing" not in st.session_state:
    st.session_state.user_missing = False
if "attempts" not in st.session_state:
    st.session_state.attempts = 1
if "count" not in st.session_state:
    st.session_state.count = 0
if "max_q" not in st.session_state:
    st.session_state.max_q = 10
if "q" not in st.session_state:
    st.session_state.q = None
if "ans" not in st.session_state:
    st.session_state.ans = ""

# Sidebar for additional info
with st.sidebar:
    st.markdown('<p class="sidebar-text">📊 User Dashboard</p>', unsafe_allow_html=True)
    if user:
        st.write(f"👤 **User:** {user}")
    if st.session_state.user_exists:
        st.write(f"📈 Questions Answered: {min(st.session_state.count, 10)}")
        st.write(f"🎯 Progress: {min(st.session_state.count, 10)}/10")
        st.write(f"🔄 Test Attempts: {st.session_state.attempts}")
        if st.session_state.count > 0:
            st.markdown("### 🏆 Achievements")
            if st.session_state.count >= 5 and st.session_state.count < 10:
                st.success("⭐ Halfway there!")
            if st.session_state.count >= 10:
                st.success("🎉 Test Completed!")
            st.info(f"Total Attempts: {st.session_state.attempts}")
    else:
        st.info("🔐 Please enter your name and check/create user to start.")

# -----------------------------
# STEP 2: CHECK USER
# -----------------------------
if user and st.button("🔍 Check User"):
    r = requests.get(f"{API}/check_user/{user}")
    data = r.json()
    if data.get("exists"):
        # Fetch session details to see if a previous test exists
        session_r = requests.get(f"{API}/session/{user}")
        session_data = session_r.json()
        answered = session_data.get("answered", 0)

        st.success(f"✅ Welcome back, {user}! You can start your test.")
        st.session_state.user_exists = True
        st.session_state.user_missing = False
        st.session_state.count = answered
        st.session_state.previous_test = session_data.get("has_previous", False)
        st.session_state.attempts = session_data.get("attempts", 1)
    else:
        st.warning("⚠️ User not found. Create a new user to start the test.")
        st.session_state.user_exists = False
        st.session_state.user_missing = True
        st.session_state.previous_test = False

# -----------------------------
# STEP 3: CREATE USER
# -----------------------------
if user and st.session_state.user_missing:
    if st.button("➕ Create User"):
        r = requests.post(f"{API}/create_user/{user}")
        st.success("🎉 User created successfully! You can now start your test.")
        st.session_state.user_exists = True
        st.session_state.user_created = True
        st.session_state.user_missing = False

    if st.button("🚀 Create & Start Test"):
        r = requests.post(f"{API}/create_user/{user}")
        st.success("🎉 User created and test started!")
        st.session_state.user_exists = True
        st.session_state.user_created = True
        st.session_state.user_missing = False
        st.session_state.count = 0
        st.session_state.q = None
        # Fetch first question right away
        r = requests.get(f"{API}/question/{user}")
        q = r.json()
        if "error" not in q:
            st.session_state.q = q

# -----------------------------
# STEP 4: REFRESH SESSION
# -----------------------------
if st.session_state.user_exists and st.button("🔄 Refresh Session"):
    r = requests.post(f"{API}/refresh/{user}")
    st.success("Session refreshed!")
    st.session_state.count = 0
    st.session_state.q = None

# If user has a previous full test, allow a retake
if st.session_state.user_exists and st.session_state.count >= st.session_state.max_q:
    st.info("You have completed a test. Retake to compare old and new results.")
    if st.button("🔁 Retake Test"):
        requests.post(f"{API}/refresh/{user}")
        st.session_state.count = 0
        st.session_state.q = None
        st.session_state.previous_test = False
        r = requests.get(f"{API}/question/{user}")
        q = r.json()
        if "error" not in q:
            st.session_state.q = q

# -----------------------------
# STEP 5: TEST FLOW
# -----------------------------
if st.session_state.user_exists:
    if st.session_state.count < 10:
        progress_value = st.session_state.count / 10
    else:
        progress_value = 1.0
    st.progress(progress_value)

    if st.session_state.count == 0 and st.button("🚀 Start Test"):
        r = requests.get(f"{API}/question/{user}")
        q = r.json()
        if "error" not in q:
            st.session_state.q = q
    elif st.session_state.count > 0 and st.session_state.count < st.session_state.max_q and st.session_state.q is None:
        if st.button("▶️ Continue Test"):
            r = requests.get(f"{API}/question/{user}")
            q = r.json()
            if "error" not in q:
                st.session_state.q = q

    if st.session_state.q:
        with st.form(key=f"question_form_{st.session_state.count}"):
            st.subheader(f"📝 Question {st.session_state.count+1} of 10")
            st.write(st.session_state.q["question"])
            
            options = st.session_state.q["options"]
            # Display options nicely
            for i, opt in enumerate(options):
                st.write(f"{chr(65+i)}. {opt}")
            
            ans = st.radio("Select your answer:", options, key="answer_radio")
            
            submitted = st.form_submit_button("✅ Submit Answer")
            
            if submitted:
                requests.post(f"{API}/answer", params={"user": user, "ans": ans})
                st.session_state.count += 1

                # Try to get next question
                r = requests.get(f"{API}/question/{user}")
                q = r.json()
                if "error" not in q:
                    st.session_state.q = q
                else:
                    st.session_state.q = None
                    st.success("🎯 You have answered all questions!")
                    
                    # Fetch study plan only after test completion
                    r = requests.get(f"{API}/plan/{user}")
                    data = r.json()
                    plan_text = data.get("plan")
                    weak_topics = data.get("weak_topics")
                    answers = data.get("answers", [])

                    if plan_text:
                        st.subheader("📖 Study Plan")
                        st.write(plan_text)
                        st.session_state.previous_test = True

                        # Compare with previous attempt if available
                        comparison = data.get("comparison", {})
                        if comparison:
                            st.subheader("🔍 Test Comparison")
                            st.write(f"• Previous correct: {comparison.get('prev_correct')} vs New correct: {comparison.get('new_correct')}")
                            st.write(f"• Previous ability: {comparison.get('prev_ability')} vs New ability: {comparison.get('new_ability')}")
                            st.write(f"• Previous weak topics: {', '.join(comparison.get('prev_weak_topics', []))}")
                            st.write(f"• New weak topics: {', '.join(comparison.get('new_weak_topics', []))}")

                        if weak_topics:
                            st.subheader("⚠️ Weak Topics")
                            st.write(", ".join(weak_topics))

                        if answers:
                            st.subheader("📊 Performance by Topic")
                            df = pd.DataFrame(answers)
                            chart = alt.Chart(df).mark_bar().encode(
                                x="topic",
                                y="count()",
                                color=alt.condition(
                                    alt.datum.correct, alt.value("green"), alt.value("red")
                                )
                            ).properties(width=600)
                            st.altair_chart(chart, use_container_width=True)
                    else:
                        st.error("Plan not generated")

# -----------------------------
# FLOWCHART REPRESENTATION
# -----------------------------
st.markdown("### 🔄 Learning Flow")
st.markdown("""
➡️ **Enter Name** → 🔍 **Check User** → ➕ **Create User (if needed)** → 🚀 **Start Test** → 📝 **Answer Questions** → 📖 **Study Plan**
""")

# -----------------------------
# OPTIONAL: VIEW PLAN LATER
# -----------------------------
if st.session_state.user_exists and st.session_state.count > 0:
    if st.session_state.previous_test and st.session_state.count == 0:
        st.info("You have a previous plan saved. Retake the test to generate a new plan.")
    elif st.button("📖 View Study Plan"):
        r = requests.get(f"{API}/plan/{user}")
        data = r.json()
        plan_text = data.get("plan")
        weak_topics = data.get("weak_topics")
        answers = data.get("answers", [])

        if plan_text:
            st.subheader("📖 Study Plan")
            st.write(plan_text)

            # Compare with previous attempt if available
            comparison = data.get("comparison", {})
            if comparison:
                st.subheader("🔍 Test Comparison")
                st.write(f"• Previous correct: {comparison.get('prev_correct')} vs New correct: {comparison.get('new_correct')}")
                st.write(f"• Previous ability: {comparison.get('prev_ability')} vs New ability: {comparison.get('new_ability')}")
                st.write(f"• Previous weak topics: {', '.join(comparison.get('prev_weak_topics', []))}")
                st.write(f"• New weak topics: {', '.join(comparison.get('new_weak_topics', []))}")

            if weak_topics:
                st.subheader("⚠️ Weak Topics")
                st.write(", ".join(weak_topics))

            if answers:
                st.subheader("📊 Performance by Topic")
                df = pd.DataFrame(answers)
                chart = alt.Chart(df).mark_bar().encode(
                    x="topic",
                    y="count()",
                    color=alt.condition(
                        alt.datum.correct, alt.value("green"), alt.value("red")
                    )
                ).properties(width=600)
                st.altair_chart(chart, use_container_width=True)
        else:
            st.error("Plan not generated")
