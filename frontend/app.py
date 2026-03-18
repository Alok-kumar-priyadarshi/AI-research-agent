import streamlit as st
import requests
import uuid
import json
import os
from dotenv import load_dotenv

load_dotenv()

backend_research = os.getenv("backend_research")
backend_pdf = os.getenv("backend_pdf")


st.markdown("""
<style>
/* Fix bottom container */
div[data-testid="stHorizontalBlock"] {
    position: fixed;
    bottom: 20px;
    left: 10%;
    width: 80%;
    background-color: #0e1117;
    padding: 10px;
    border-radius: 10px;
    z-index: 1000;
}

/* Hide default file uploader box */
div[data-testid="stFileUploader"] {
    width: 125px;
}

/* Make it look like icon */
div[data-testid="stFileUploader"] > div {
    border: none;
    background: transparent;
}

/* Prevent content overlap */
.main {
    padding-bottom: 120px;
}
</style>
""", unsafe_allow_html=True)

#  backend URL
API_URL = backend_research

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
    st.header("⚙️ Settings")

    if st.button("Clear Chat"):
        st.session_state.messages = []

    st.divider()

    st.header("📂 Upload PDF")

    uploaded_file = st.file_uploader(
        "Upload your document",
        type=["pdf"]
    )

    if "pdf_uploaded" not in st.session_state:
        st.session_state.pdf_uploaded = False

    if uploaded_file and not st.session_state.pdf_uploaded:
        with st.spinner("Processing PDF..."):
            try:
                requests.post(
                    backend_pdf,
                    params={"session_id": st.session_state.session_id},
                    files={
                        "file": (
                            uploaded_file.name,
                            uploaded_file.getvalue(),
                            "application/pdf"
                        )
                    },
                    timeout=180
                )

                st.session_state.pdf_uploaded = True
                st.session_state.pdf_name = uploaded_file.name

                st.success("✅ PDF uploaded!")

            except Exception as e:
                st.error(f"Upload failed: {e}")

    if st.session_state.get("pdf_uploaded"):
        st.info(f"📄 Using: {st.session_state.pdf_name}")
    if st.button("Reset Document"):
        st.session_state.pdf_uploaded = False

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
                response = requests.post(API_URL, json=payload, timeout=180)
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
    
    

if "pdf_uploaded" not in st.session_state:
    st.session_state.pdf_uploaded = False

if uploaded_file and not st.session_state.pdf_uploaded:
    st.write("Uploading:", uploaded_file.name)

    try:
        requests.post(
            backend_pdf,
            params={"session_id": st.session_state.session_id},
            files={
                "file": (
                    uploaded_file.name,
                    uploaded_file.getvalue(),
                    "application/pdf"
                )
            },
            timeout=3600
        )

        st.session_state.pdf_uploaded = True
        st.session_state.pdf_name = uploaded_file.name

        st.success("✅ PDF uploaded!")

    except Exception as e:
        st.error(f"Upload failed: {e}")
        
        
        
