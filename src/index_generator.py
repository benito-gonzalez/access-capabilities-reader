import os
import logging
import chromadb
import streamlit as st
from src import constants
from llama_index.core import Settings
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext, Document
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.agent.openai import OpenAIAssistantAgent
from llama_index.core.tools import QueryEngineTool, ToolMetadata

os.environ['OPENAI_API_KEY'] = st.secrets["api_crendentials"]

Settings.llm = OpenAI("gpt-3.5-turbo", temperature=0, max_tokens=512)
Settings.embed_model = OpenAIEmbedding(model='text-embedding-3-small')


def generate_indexes() -> None:
    logging.info(f"Starting the document loading...")
    json_file = os.path.join(constants.DATA_PATH, "EDRD_Capacidad_de_Acceso_2024_03_01.json")

    if not os.path.exists(json_file):
        logging.info(f"There is no json file in the directory.")
    else:
        # load the documents in /pending directory
        documents = SimpleDirectoryReader(input_files=[json_file]).load_data()

        # initialize client, setting path to save data
        db = chromadb.PersistentClient(path=constants.DB_PATH)
        # create collection
        chroma_collection = db.get_or_create_collection("Collection")
        # assign chroma as the vector_store to the context
        vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
        storage_context = StorageContext.from_defaults(vector_store=vector_store)

        logging.info("Starting the indexing process...")
        VectorStoreIndex.from_documents(documents, storage_context=storage_context)


@st.cache_resource
def load_indexes() -> VectorStoreIndex:
    logging.info(f"Loading indexes...")

    # initialize client
    db = chromadb.PersistentClient(path=constants.DB_PATH)

    # get collection
    chroma_collection = db.get_or_create_collection("Collection")

    # assign chroma as the vector_store to the context
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    # load your index from stored vectors
    index = VectorStoreIndex.from_vector_store(vector_store, storage_context=storage_context)
    return index


def get_assistant_agent(index):
    acr_tool = QueryEngineTool(
        query_engine=index.as_query_engine(),
        metadata=ToolMetadata(
            name="edrd_03_01",
            description="Proporciona información detallada sobre la capacidad de acceso de cada subestacion"
        )
    )
    agent = OpenAIAssistantAgent.from_new(
        name="EDRD Analyst",
        instructions="Eres un asistente QA diseñado para analizar los datos sobre la capacidad de acceso proporcionado"
                     "en el contexto mediante un fichero json",
        tools=[acr_tool],
        openai_tools=[{"type": "code_interpreter"}],
        files=["data/EDRD_Capacidad_de_Acceso_2024_03_01.json"],
        #model="gpt-3.5-turbo",
        verbose=True,
    )
    return agent


if __name__ == "__main__":
    generate_indexes()
