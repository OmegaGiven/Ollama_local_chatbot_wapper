import streamlit as st
from ollama_api import get_available_models, ai_stream
import pdfplumber
import os

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

def create_sidebar():
     with st.sidebar:
        # Top bar container with all persistent UI elements
        if 'models' not in st.session_state or 'directory' not in st.session_state:
            selected_model = setup_model_selection()
            directory_input = st.text_input("Enter directory path", key="directory")

            # Store the directory input value in session state to keep it across reruns
            if directory_input:
                st.session_state["directory"] = directory_input

        else:
            # If we're coming from a rerun, show all elements again
            selected_model = setup_model_selection()
            directory_input = st.text_input("Enter directory path", key="directory")

            if directory_input and 'directory' not in st.session_state or st.session_state['directory'] != directory_input:
                # Only update session state if the value changes (or is new)
                st.session_state["directory"] = directory_input
        document_text = file_upload()

        think = st.selectbox("Enable Think for AI Thinking models:", [True, False])
        stream = st.selectbox("AI response streamed:", [True, False])
        remember_history = st.selectbox("Remember Chat history:", [True, False])

        return selected_model, document_text, think, stream, remember_history

history = []

def setup_ui():
    """Initialize Streamlit UI elements."""
    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    st.title("AI Chatbot with Model Selection")
    selected_model, document_text, think, stream, remember_history = create_sidebar()

    # User input area in the right side
    display_chat_history()
    user_input = st.chat_input("Ask something about the uploaded document...")
    # Process user input and stream responses
    if user_input:
        st.session_state["messages"].append({"role": "user", "content": f"{user_input} ( {selected_model})"})
        # Display user input in chat
        with st.chat_message("user"):
            st.markdown( f"{user_input} ({selected_model})")
        history.append({"role": "user", "content": user_input})


        # Stream AI response
        with st.chat_message("assistant"):
            response_container = st.empty()
            ai_response = ""
            for chunk in ai_stream(model= selected_model,
                                prompt=user_input, 
                                files=document_text,
                                think=think,
                                stream=stream,
                                messages=history if remember_history else None,
                                ):
                ai_response += chunk
                response_container.markdown(ai_response)  # Stream response dynamically
                st.session_state["partial_response"] = ai_response  # Store progress

            st.session_state["messages"].append({"role": "assistant", "content": ai_response})
            history.append({"role": "assistant", "content": ai_response})
            # print(history)



