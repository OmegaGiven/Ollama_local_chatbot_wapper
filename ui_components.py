import streamlit as st
from ollama_api import get_available_models
import pdfplumber

def setup_ui():
    """Initialize Streamlit UI elements."""
    st.title("AI Chatbot with Model Selection")

def setup_model_selection():
    # Fetch available models
    if "models" not in st.session_state:
        st.session_state["models"] = get_available_models()

    # Model Selection Dropdown
    return st.selectbox("Choose AI Model", st.session_state["models"])

def file_upload():
    """Handle file upload and extraction."""
    uploaded_file = st.file_uploader("Upload documentation or code file", type=["txt", "md", "pdf", "py"], accept_multiple_files=False)
    if uploaded_file:
        print(uploaded_file.type)
        with pdfplumber.open(uploaded_file) as pdf:
            return "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
        # try:
        #     # Read the uploaded PDF file using the detected encoding
        #     document_text = result.decode(chardet.detect(result)["encoding"])
        #     print("document_text: ", document_text)
        # except UnicodeDecodeError as e:
        #     print(f"UnicodeDecodeError: {e}")
        #     return ""
        # else:
        #     return document_text
    else:
        return ""

def display_chat_history():
    """Render stored chat history."""
    if "messages" not in st.session_state:
        st.session_state["messages"] = []
    
    for message in st.session_state["messages"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

def user_input_handler():
    """Handles user input for chat."""
    return st.chat_input("Ask something about the uploaded document...")
