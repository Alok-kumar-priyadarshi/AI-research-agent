import streamlit as st
import requests
import uuid
import json

#  backend URL
API_URL = "http://127.0.0.1:8000/research"

st.set_page_config(page_title="AI Research Agent", layout="wide")

st.title("🤖 AI Research Assistant")

#  session id (per user)
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

#  chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

#  sidebar (extra control)
with st.sidebar:
    st.header("Settings")
    if st.button("Clear Chat"):
        st.session_state.messages = []

#  function to render structured response
def render_response(answer):
    try:
        parsed = json.loads(answer)

        st.subheader(parsed.get("title", "Report"))

        st.markdown("### 📌 Summary")
        st.write(parsed.get("summary", ""))

        st.markdown("### 🔑 Key Points")
        for point in parsed.get("key_points", []):
            st.markdown(f"- {point}")

        st.markdown("### 📊 Detailed Analysis")
        st.write(parsed.get("detailed_analysis", ""))

        st.markdown("### 🔗 Sources")
        for src in parsed.get("sources", []):
            st.markdown(f"[{src}]({src})")

    except Exception:
        # fallback if JSON parsing fails
        st.write(answer)

# 🔹 display chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        render_response(msg["content"])

# 🔹 user input
query = st.chat_input("Ask your research question...")

if query:
    # show user message
    st.session_state.messages.append({"role": "user", "content": query})

    with st.chat_message("user"):
        st.write(query)

    #  API call
    payload = {
        "query": query,
        "session_id": st.session_state.session_id
    }

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = requests.post(API_URL, json=payload, timeout=60)
                data = response.json()

                if "response" in data:
                    answer = data["response"]
                else:
                    answer = data.get("error", "Something went wrong")

            except Exception as e:
                answer = f"⚠️ Error: {str(e)}"

            #  render structured output
            render_response(answer)

    #  save AI response
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })