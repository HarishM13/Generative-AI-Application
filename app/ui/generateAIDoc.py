import streamlit as st
import requests

FASTAPI_URL = "http://localhost:8000"

st.set_page_config(page_title="GenAI Doc Assistant", layout="wide")
st.title(" Enterprise Generative AI Doc Assistant ")
st.markdown("Upload enterprise documents with appropriate format and ask questions.")

if "messages" not in st.session_state:
    st.session_state.messages = []


def validate_input(text: str) -> tuple[bool, str]:
    # Rule 1: Check if empty or just spaces
    if not text.strip():
        return False, "Input cannot be empty."
            
    # Rule 2: Profanity or blocked words check (example)
    blocked_words = ["spam", "hack", "malware","suicide","kill","murder","bomb"]
    if any(word in text.lower() for word in blocked_words):
        return False, "Your message contains prohibited words."

    return True, "Valid"



st.sidebar.header("📂 Upload Documents")
uploaded_file = st.sidebar.file_uploader("Upload File with TXT/PDF/CSV/XSLX format", 
    type=["txt", "pdf", "csv", "xlsx"]
)

if uploaded_file is not None:
    if st.sidebar.button("Upload"):
        with st.spinner("Uploading the document..."):
           
            try:
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                response = requests.post(f"{FASTAPI_URL}/upload", files=files)
                if response.status_code == 200:
                    st.success(
                        "Document uploaded "
                        "successfully!"
                    )
                    st.json(response.json())
                else:
                    st.error(response.json().get("error","Upload Failed"))
            except Exception as ex:
                st.error(
                    f"Error: {str(ex)}"
                )
st.subheader("💬 Ask Natural Language questions in uploaded document")
is_valid=False
error_message=""
user_query= st.chat_input("Ask Natural Language questions from uploaded document..")
if user_query:
    is_valid, error_message = validate_input(user_query)
    if error_message == "Valid" and is_valid:
          # Display user message in chat container
            with st.chat_message("user"):
                 st.markdown(user_query)
            st.session_state.messages.append({"role": "user", "content": user_query})
            with st.spinner("🤖 Agentic AI processing..."):
                payload = {"user_query": user_query}
                try:
                    res = requests.get(f"{FASTAPI_URL}/query", json=payload)
                    if res.status_code == 200:
                        result = res.json()
                        answer = result.get(
                        "final_verified_response")
                        st.session_state.messages.append({"role": "assistant", "content": answer})
                        st.info(answer)
                    else:
                        st.error("Error communicating with Backend Services.")
                except Exception as e:
                    st.error(f"Backend offline or connection refused: {e}")
    else:
        st.error(f"⚠️ Validation Error: {error_message}")