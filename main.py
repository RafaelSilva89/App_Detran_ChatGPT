# pip install streamlit streamlit-chat langchain python-dotenv
import streamlit as st
from streamlit_chat import message
from dotenv import load_dotenv
import os
from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    SystemMessage,
    HumanMessage,
    AIMessage
)

from htmlTemplates import css, bot_template, user_template


def init():
    # Load the OpenAI API key from the environment variable
    load_dotenv()

    # test that the API key exists
    if os.getenv("OPENAI_API_KEY") is None or os.getenv("OPENAI_API_KEY") == "":
        print("OPENAI_API_KEY is not set")
        exit(1)
    else:
        print("OPENAI_API_KEY is set")

st.set_page_config(page_title="Your own ChatGPT", page_icon=":earth_americas:")

def main():
    init()
    st.write(css, unsafe_allow_html=True)
    chat = ChatOpenAI(temperature=0)

    # initialize message history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            SystemMessage(content="You are a helpful assistant.")
        ]

    st.header("Your own ChatGPT :earth_americas:")

    # sidebar with user input
    #with st.sidebar:
    #user_input = st.text_input("Your message: ", key="user_input")
    user_input = st.chat_input("Your message: ", key="user_input")

    # handle user input
    if user_input:
        st.session_state.messages.append(HumanMessage(content=user_input))
        with st.spinner("Thinking..."):
            response = chat(st.session_state.messages)
        st.session_state.messages.append(AIMessage(content=response.content))

    # display message history
    messages = st.session_state.get('messages', [])
    for i, msg in enumerate(messages[1:]):
        if i % 2 == 0:
            #message(msg.content, is_user=True, key=str(i) + '_user')
            st.write(user_template.replace("{{MSG}}", msg.content),is_user=True, key=str(i) + '_user', unsafe_allow_html=True)
        else:
            #message(msg.content, is_user=False, key=str(i) + '_ai')
            st.write(bot_template.replace("{{MSG}}", msg.content), is_user=False, key=str(i) + '_ai' ,unsafe_allow_html=True)


if __name__ == '__main__':
    main()