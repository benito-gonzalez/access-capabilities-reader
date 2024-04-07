import locale
from datetime import datetime
import streamlit as st
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.agent.openai import OpenAIAssistantAgent

locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

agent = OpenAIAssistantAgent.from_new(
    name="Math Tutor",
    instructions="You are a personal math tutor. Write and run code to answer math questions.",
    openai_tools=[{"type": "code_interpreter"}],
    instructions_prefix="Please address the user as Jane Doe. The user has a premium account.",
)


def get_current_date():
    return datetime.now().strftime("%d de %B de %Y")


def get_chat_engine(index, streaming=True):
    memory = ChatMemoryBuffer.from_defaults(token_limit=5000)
    return index.as_chat_engine(
        chat_mode="context",
        memory=memory,
        system_prompt=(
            f"Eres un experto en el análisis de datos semiestructurados en ficheros JSON. El usuario te hara preguntas"
            f"sobre esos datos que implicarán operaciones matemática como sumas y medias. "
            f"Deberás realizar los cálculos matemáticos sobre los datos elegidos por el usuario."
            f"Responder de manera consisa y clara. Tómate tu tiempo para pensar la respuesta."
            f"Contesta únicamente con información proporcionada en el contexto. No uses nunca información de"
            f" tu base de conocimiento."
        ),
        streaming=streaming
    )


def show_chat(agent):
    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("What is up?"):

        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            # chat_engine = get_chat_engine(index, streaming=True)
            if prompt:
                response = agent.chat(prompt, chat_history=st.session_state.chat_history)
                response_text = st.write(response.response)
                st.session_state.messages.append({"role": "assistant", "content": response_text})
