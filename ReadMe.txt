Setup of the AI Wrapper:
1. install dependencies
 <todo add dependecies and install instructions>
 -streamlit

 for linux:
    python3 -m venv myenv
    source myenv/bin/activate
    python3 -m pip --version
    python3 -m pip install --upgrade pip
    pip install ollama-api




2. In order to run parser the following have to be running:
- Ollama local instance needs to be running
- on command line/IDE run: python -m streamlit run /OmegaAI/main.py





Things to understand:
- measurements of context
- what makes the actual size of the ai model aka the big B
- can I setup ollama to reference a database and if so what database?
- how to make a searchable DB with some kind of process that can pull relevant info.

TODO of fun things to add:
- add history tracking so the ai can understand context
- add better parsing of files on local directory to add to context sent to api