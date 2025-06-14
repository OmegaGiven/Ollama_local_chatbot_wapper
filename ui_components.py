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
        try:
            # Check the file extension
            ext = os.path.splitext(uploaded_file.name)[1].lower()
            content_type = {"application/pdf": ".pdf", "text/plain": ".txt"}.get(uploaded_file.type, None)

            if ext == ".pdf":
                with pdfplumber.open(uploaded_file) as pdf:
                    return "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
            elif uploaded_file.type == "text/plain":
                # For text files (txt, md, etc.) we can read directly
                content = uploaded_file.read().decode('utf-8')
                return content
            else:
                # Use the file object to read and decode with UTF-8, but note: what if it's a binary file? 
                # We are assuming that non-PDF allowed files are text-based.
                document_text = uploaded_file.read()   # This returns bytes
                decoded_bytes = document_text.decode('utf-8')
                return decoded_bytes
        except Exception as e:
            print(f"Error processing file: {e}")
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

def get_context_from_directory_and_subdirectories(path):
    """Collects text from all allowed files in the given path and its subdirectories."""
    texts = []
    for root, _, filenames in os.walk(path):
        for filename in filenames:
            file_path = os.path.join(root, filename)
            if is_allowed_file(file_path):  # We need a function to check by extension
                try:
                    text = read_file(file_path)   # This function should handle the reading and encoding properly
                    texts.append(text)
                except Exception as e:
                    pass

    return "\n\n".join(texts)