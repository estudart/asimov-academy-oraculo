import streamlit as st



class PageChat:
    def __init__(self):
        self.messages_list = [
            ("user", "Hello"),
            ("assistant", "How are you?"),
            ("user", "I'm fine!"),
        ]

    def start_page_chat(self):
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


if __name__ == '__main__':
    chat_instance = PageChat()
    chat_instance.start_page_chat()