"""
run program by:
python -m streamlit run /OmegaAI/main.py
"""
from package_installer import install_requirements
install_requirements()

import streamlit as st
from ui_components import setup_ui, file_upload, display_chat_history, user_input_handler, setup_model_selection
from ollama_api import ai_stream


setup_ui()

top_container = st.container()
with top_container:
    document_text = file_upload()
    selected_model = setup_model_selection()

# Set up UI components
display_chat_history()
user_input = user_input_handler()



# Process user input and stream responses
if user_input:
    st.session_state["messages"].append({"role": "user", "content": f"{user_input} ( {selected_model})"})
    # Display user input in chat
    with st.chat_message("user"):
        st.markdown( f"{user_input} ({selected_model})")
    # Stream AI response
    with st.chat_message("assistant"):
        response_container = st.empty()

        ai_response = ""
        for chunk in ai_stream(user_input, document_text, selected_model, None):
            ai_response += chunk
            response_container.markdown(ai_response)  # Stream response dynamically
            st.session_state["partial_response"] = ai_response  # Store progress
        
        
        st.session_state["messages"].append({"role": "assistant", "content": ai_response})
        




