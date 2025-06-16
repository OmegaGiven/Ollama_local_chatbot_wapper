Setup of the AI Wrapper:
1. install dependencies
 <todo add dependecies and install instructions>
 -streamlit

2. In order to run parser the following have to be running:
- Ollama local instance needs to be running
- on command line/IDE run: python -m streamlit run /OmegaAI/main.py


helpful documentation for ollama rest api calls:
https://www.postman.com/postman-student-programs/ollama-api/documentation/suc47x8/ollama-rest-api 


Things to understand:
- measurements of context
- can I setup ollama to reference a database and if so what database?
- how to make a searchable DB with some kind of process that can pull relevant info.

TODO of fun things to add:
- add history tracking so the ai can understand context
- add better parsing of files on local directory to add to context sent to api