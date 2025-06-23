Setup of the AI Wrapper:
1. install dependencies for the AI wrapper
    you can just run to install the used python libraries ["streamlit", "pymupdf", "gitingest"]:
        python package_installer.py
    for linux if you want to make an venv for python:
        python3 -m venv myenv
        source myenv/bin/activate
        python3 -m pip --version
        python3 -m pip install --upgrade pip
        python3 -m pip install streamlit, pymupdf, gitingest
2. In order to run wrapper the following have to be running:
    Ollama local instance needs to be running
    on command line/IDE run: python -m streamlit run main.py

3. Input overview of streamlit app
Choose AI Model:
    This pulls from installed list of models that ollama has as of running the streamlit app
Enter repostiroy root path:
    Input a root path <C:projects/project_name/> that when you press the arrow or enter on the chatbot it will create a consolidated text file of the pathand subditectories using gitingest for it to be passed to ollamas models
Upload documentation or code file:
    uploads a pdf which is then parsed by pymupdf library to be passed into ollama models
Enable Think for AI Thinking models:
    Can be set to True for models like qwen deepseek etc
AI response streamed:
    Set to true if you want it to return word by word rather than all at once (token/s will be inaccurate if you are looking at that)
Remeber Chat history:
    When set to true it will take the context returned from previous responses and pass it in so it remebers chat history





helpful documentation for ollama rest api calls:
https://www.postman.com/postman-student-programs/ollama-api/documentation/suc47x8/ollama-rest-api 


Things that could be fun additions to this project in the future:
- measurements of context
- can I setup ollama to reference a database and if so what database?
- how to make a searchable DB with some kind of process that can pull relevant info.

