import streamlit as st
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq

from utils.config import secrets



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
    

    def add_user_message(self, memory: ConversationBufferMemory, message: str) -> None:
        memory.chat_memory.add_user_message(message)


    def add_ai_message(self, memory: ConversationBufferMemory, message: str) -> None:
        memory.chat_memory.add_ai_message(message)


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
            answer = chat.write_stream(st.session_state["llm"].stream(user_input))
            self.add_ai_message(stored_memory, answer)
            st.session_state["memory"] = memory


    def side_bar(self):
        tabs = st.tabs(["Upload Files", "Select Models"])
        
        with tabs[0]:
            file_type = st.selectbox(
                "Select the file type", 
                list(self.type_mapping_dict.keys())
            )
            self.generate_input_loader(self.type_mapping_dict[file_type])
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



    def run(self):
        self.chat()
        with st.sidebar:
            self.side_bar()


if __name__ == '__main__':
    chat_instance = PageChat()
    chat_instance.run()