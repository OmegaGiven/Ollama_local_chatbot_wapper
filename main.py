import streamlit as st
from ui_components import setup_ui, file_upload, display_chat_history, user_input_handler, setup_model_selection
from ollama_api import ai_stream
import os
import pypdf


setup_ui()

# Set up UI components
display_chat_history()
user_input = user_input_handler()

document_text = file_upload()
selected_model = setup_model_selection()



# def get_context_from_directory(path):
#     """Makes List of files in path."""
#     try:
#         return [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) and os.path.join(path, f).endswith(".pdf")]
#     except Exception as e:
#         return [f"Error reading downloads folder: {e}"]

# files = get_context_from_directory("C:\\Users\\9ncjo\\Downloads")

# def extract_pdf_text(pdf_path):
#     """Extract and return text from a PDF file."""
#     text = ""
#     try:
#         with pypdf.PdfReader(pdf_path) as doc:
#             text = "\n".join([page.extract_text() for page in reader.pages])
#         return text
#     except Exception as e:
#         return f"Error extracting PDF: {e}"

# pdfs = []
# for f in files:
#     pdfs.append(extract_pdf_text(f))

# selected_file = st.selectbox("Select a file to analyze:", pdfs)

# if selected_file:
#     with open(os.path.join("C:\\Users\\9ncjo\\Downloads", selected_file), "r", encoding="utf-8") as f:
#         document_text = f.read()




# Process user input and stream responses
if user_input:
    st.session_state["messages"].append({"role": "user", "content": user_input})
    # Display user input in chat
    with st.chat_message("user"):
        st.markdown(user_input)
    # Stream AI response
    with st.chat_message("assistant"):
        response_container = st.empty()

        ai_response = ""
        for chunk in ai_stream(user_input, document_text, selected_model):
            ai_response += chunk
            response_container.markdown(ai_response)  # Stream response dynamically
            st.session_state["partial_response"] = ai_response  # Store progress
        
        
        st.session_state["messages"].append({"role": "assistant", "content": ai_response})





