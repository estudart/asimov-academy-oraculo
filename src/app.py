import tempfile

import streamlit as st
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate

from utils.config import secrets
from utils.loaders import *



class PageChat:
    def __init__(self):
        self.models_data = self.get_models()
    
        self.type_mapping_dict = {
            "Youtube": {
                "message": "Type the url of the video",
                "action": "text",
                "type": "url"
            },
            "WebSite": {
                "message": "Type the url of the website",
                "action": "text",
                "type": "url"
            },
            "PDF": {
                "message": "Updaload pdf file",
                "action": "upload",
                "type": [".pdf"]
            },
            ".csv": {
                "message": "Updaload csv file",
                "action": "upload",
                "type": [".csv"]
            },
            ".txt": {
                "message": "Updaload txt file",
                "action": "upload",
                "type": [".txt"]
            }
        }


    @staticmethod
    @st.cache_resource
    def get_models():
        return {
            "OpenAI": {
                "llm": ChatOpenAI(api_key="default"),
                "models": [
                    "gpt-4o-mini",
                    "gpt-4o",
                    "o1-preview",
                    "o1-mini"
                ]
            },
            "Groq": {
                "llm": ChatGroq(api_key="default"),
                "models": [
                    "llama-3.1-70b-versatile",
                    "gemma2-9b-it",
                    "mixtral-8x7b-32768"
                ]
            }
        }
    

    @staticmethod
    @st.cache_resource
    def get_memory():
        return ConversationBufferMemory()
    

    def set_model(self, provider: str, llm, model: str):
        llm.__init__(
            api_key=secrets.get(f"{provider.upper()}_API_KEY"),
            model=model
        )
        st.session_state["provider"] = provider
        st.session_state["llm"] = llm


    def load_files(self, file_type, file):
        if file_type == 'Site':
            documento = load_website(file)
        if file_type == 'Youtube':
            documento = load_youtube(file)
        if file_type == 'PDF':
            with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp:
                temp.write(file.read())
                nome_temp = temp.name
            documento = load_pdf(nome_temp)
        if file_type == '.csv':
            with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as temp:
                temp.write(file.read())
                nome_temp = temp.name
            documento = load_csv(nome_temp)
        if file_type == '.txt':
            with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as temp:
                temp.write(file.read())
                nome_temp = temp.name
            documento = load_txt(nome_temp)
        return documento
    

    def add_user_message(self, memory: ConversationBufferMemory, message: str) -> None:
        memory.chat_memory.add_user_message(message)


    def add_ai_message(self, memory: ConversationBufferMemory, message: str) -> None:
        memory.chat_memory.add_ai_message(message)

    
    def clean_memory(self, memory: ConversationBufferMemory) -> None:
        memory.chat_memory.clear()


    def generate_input_loader(self, data_set: dict) -> st:
        action = data_set.get("action")
        if action == "upload":
            file = st.file_uploader(
                data_set.get("message"), 
                type=data_set.get("type")
            )
        elif action == "text":
            file = st.text_input(
                data_set.get("message")
            )
        else:
            pass
        return file

    def conversation(self, file_type, document):
        system_message = '''Você é um assistente amigável chamado Oráculo.
        Você possui acesso às seguintes informações vindas 
        de um documento {}: 

        ####
        {}
        ####

        Utilize as informações fornecidas para basear as suas respostas.

        Sempre que houver $ na sua saída, substita por S.

        Se a informação do documento for algo como "Just a moment...Enable JavaScript and cookies to continue" 
        sugira ao usuário carregar novamente o Oráculo!'''.format(file_type, document)

        print(system_message)

        template = ChatPromptTemplate.from_messages([
            ('system', system_message),
            ('placeholder', '{chat_history}'),
            ('user', '{input}')
        ])
        chain = template | st.session_state["llm"]

        st.session_state['chain'] = chain

    def chat(self):
        st.header("🤖Welcome to the Oracle", divider=True)
        stored_memory = self.get_memory()
        memory = st.session_state.get('memory', stored_memory)
        for message in memory.buffer_as_messages:
            chat = st.chat_message(message.type)
            chat.markdown(message.content)

        user_input = st.chat_input("Talk to the oracle")
        if user_input:
            self.add_user_message(stored_memory, user_input)
            chat = st.chat_message("human")
            chat.markdown(user_input)

            chat = st.chat_message("ai")
            answer = chat.write_stream(st.session_state["chain"].stream({
                "input": user_input,
                "chat_history": stored_memory.buffer_as_messages
            }))
            self.add_ai_message(stored_memory, answer)
            st.session_state["memory"] = memory


    def side_bar(self):
        tabs = st.tabs(["Upload Files", "Select Models"])
        
        with tabs[0]:
            file_type = st.selectbox(
                "Select the file type", 
                list(self.type_mapping_dict.keys())
            )
            file = self.generate_input_loader(self.type_mapping_dict[file_type])
        with tabs[1]:
            provider = st.selectbox(
                "Select LLM provider",
                list(self.models_data.keys())
            )
            llm = self.models_data[provider]["llm"]
            model = st.selectbox(
                "Select a model",
                self.models_data.get(provider)["models"]
            )
            self.set_model(provider, llm, model)

        if st.button('Start Oracle', use_container_width=True):
            document = self.load_files(file_type, file)
            self.conversation(file_type, document)

        if st.button('Remove conversation history', use_container_width=True):
            self.clean_memory(self.get_memory())



    def run(self):
        self.chat()
        with st.sidebar:
            self.side_bar()


if __name__ == '__main__':
    chat_instance = PageChat()
    chat_instance.run()