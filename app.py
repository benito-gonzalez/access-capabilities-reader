import time
import logging
from src.scraper import retrieve_pdf_from_website
from src.pdf_to_file import generate_csv_from_file, generate_json_from_file
from src.index_generator import generate_indexes, load_indexes, get_assistant_agent
from src.conversation import show_chat
import streamlit as st

logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s',
                    level=logging.INFO)

if "messages" not in st.session_state:
    st.session_state.messages = []
if "user_text" not in st.session_state:
    st.session_state.user_text = ""
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


@st.cache_resource
def display_title():
    st.markdown(
        f"<h3 style='text-align: center;'>Bienvenido a tu asistente virtual de Capacidad de acceso para generación en nudos de la red de distribución</h3>",
        unsafe_allow_html=True)


def main():
    #start_time = time.time()
    #pdf_file_name = retrieve_pdf_from_website()
    #generate_csv_from_file(pdf_file_name)
    #generate_json_from_file("EDRD_Capacidad_de_Acceso_2024_03_01.pdf")
    #print("Time taken:", time.time() - start_time, "seconds")

    #generate_indexes()

    display_title()
    index = load_indexes()
    agent = get_assistant_agent(index)
    show_chat(agent)


if __name__ == "__main__":
    main()
