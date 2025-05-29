import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq

from utils.config import secrets



class PageChat:
    def __init__(self):
        self.messages_list = [
            ("user", "Hello"),
            ("assistant", "How are you?"),
            ("user", "I'm fine!"),
        ]

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
                "llm": ChatOpenAI(api_key=secrets.get("OPENAI_API_KEY")),
                "models": [
                    "gpt-4o-mini",
                    "gpt-4o",
                    "o1-preview",
                    "o1-mini"
                ]
            },
            "Groq": {
                "llm": ChatGroq(api_key=secrets.get("GROQ_API_KEY")),
                "models": [
                    "llama-3.1-70b-versatile",
                    "gemma2-9b-it",
                    "mixtral-8x7b-32768"
                ]
            }
        }

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

        messages = st.session_state.get('messages', self.messages_list)
        for message in messages:
            chat = st.chat_message(message[0])
            chat.markdown(message[1])

        input_usuario = st.chat_input("Talk to the oracle")
        if input_usuario:
            messages.append(("user", input_usuario))
            st.session_state["messages"] = messages
            st.rerun()


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
            model = st.selectbox(
                "Select a model",
                self.models_data.get(provider)["models"]
            )


    def run(self):
        self.chat()
        with st.sidebar:
            self.side_bar()


if __name__ == '__main__':
    chat_instance = PageChat()
    chat_instance.run()