"""UI components for Streamlit"""
import streamlit as st
from ollama_api import get_available_models, ai_stream
from pdf_converter import read_pdf
import os
from gitingest import ingest
from user_talk import start_transcription, transcribe_audio
import time
import threading

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

            if ext == ".pdf":
                return read_pdf(uploaded_file)  # Use pdfplumber to read PDF files
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


def create_txt_file(document_text):
    """Create a .txt file from the extracted document text."""
    if document_text:
        with open("extracted_text.txt", "w", encoding="utf-8") as txt_file:
            txt_file.write(document_text)
        print("Text file created successfully.")
    else:
        print("No document text available to create a file.")

def process_repo_into_text(repo_path):
    """Process a repository into text using gitingest."""
    exclude = "extracted_text.txt repository_text.txt .git .github .vscode .idea .DS_Store *.pyc *.pyo __pycache__ *.log *.md *.yaml .continue"
    summary, tree, content = ingest(repo_path, exclude_patterns=exclude)
    with open("repository_text.txt", "w", encoding="utf-8") as txt_file:
        txt_file.write(summary + "\n\n" + tree + "\n\n" + content)
    return summary + "\n\n" + tree + "\n\n" + content


def create_sidebar():
     with st.sidebar:
        selected_model = setup_model_selection()
        directory_input = st.text_input("Enter repository root path", key="directory")

        repo_text = process_repo_into_text(directory_input) if directory_input else None
        document_text = file_upload()

        # Toggle button to start audio recording
        start_recording = st.toggle("Start Listening", key="start_listening")

        # Add a delay before sending the transcription
        delay_seconds = st.number_input("Delay before sending transcription (seconds)", min_value=1, max_value=10, value=3, step=1)

        # Use session state to track if recording is active
        if "is_recording" not in st.session_state:
            st.session_state["is_recording"] = False

        if start_recording and not st.session_state["is_recording"]:
            st.session_state["is_recording"] = True
            st.success("Listening started. Speak and then be silent for 3 seconds.")

        if not start_recording and st.session_state["is_recording"]:
            st.session_state["is_recording"] = False
            st.info("Listening stopped.")

        think = st.selectbox("Enable Think for AI Thinking models:", [True, False])
        stream = st.selectbox("AI response streamed:", [True, False])
        remember_history = st.selectbox("Remember Chat history:", [True, False])

        st.button("Print to console PDF text", on_click=lambda: print(document_text))
        st.button("Create txt file from PDF text", on_click=lambda: create_txt_file(document_text))

        return selected_model, document_text, think, stream, remember_history, repo_text, start_recording, delay_seconds

history = []

def setup_ui():
    """Initialize Streamlit UI elements."""
    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    st.title("AI Chatbot with Model Selection")
    selected_model, document_text, think, stream, remember_history, repo_text, start_recording, delay_seconds = create_sidebar()

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
                                repository=repo_text if repo_text else None,
                                ):
                ai_response += chunk
                response_container.markdown(ai_response)  # Stream response dynamically
                st.session_state["partial_response"] = ai_response  # Store progress

            st.session_state["messages"].append({"role": "assistant", "content": ai_response})
            history.append({"role": "assistant", "content": ai_response})
            # print(history)

    # Handle audio recording and transcription
    if start_recording and not st.session_state["is_recording"]:
        st.session_state["is_recording"] = True
        st.success("Listening started. Speak and then be silent for 3 seconds.")
    elif not start_recording and st.session_state["is_recording"]:
        st.session_state["is_recording"] = False
        st.info("Listening stopped.")

    if st.session_state["is_recording"]:
        # Start transcription in a background thread
        transcription_thread = threading.Thread(target=start_transcription)
        transcription_thread.start()
        transcription_thread.join()

        # Wait for the delay
        time.sleep(delay_seconds)

        # Send the transcribed text to the AI
        if "transcribed_text" in st.session_state:
            user_input = st.session_state["transcribed_text"]
            st.session_state["messages"].append({"role": "user", "content": f"{user_input} ( {selected_model})"})
            # Display user input in chat
            with st.chat_message("user"):
                st.markdown(f"{user_input} ({selected_model})")
            history.append({"role": "user", "content": user_input})

            # Stream AI response
            with st.chat_message("assistant"):
                response_container = st.empty()
                ai_response = ""
                for chunk in ai_stream(model=selected_model,
                                       prompt=user_input,
                                       files=document_text,
                                       think=think,
                                       stream=stream,
                                       messages=history if remember_history else None,
                                       repository=repo_text if repo_text else None,
                                       ):
                    ai_response += chunk
                    response_container.markdown(ai_response)  # Stream response dynamically
                    st.session_state["partial_response"] = ai_response  # Store progress

                st.session_state["messages"].append({"role": "assistant", "content": ai_response})
                history.append({"role": "assistant", "content": ai_response})
                # print(history)

