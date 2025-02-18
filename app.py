import streamlit as st
from langchain_community.agent_toolkits import create_sql_agent
from langchain_openai import ChatOpenAI
from langchain_community.utilities import SQLDatabase
import os

os.environ["OPENAI_API_KEY"]=st.secrets["OPENAI_API_KEY"]

st.title("DataBaseGPT")

db = SQLDatabase.from_uri("sqlite:///Donation_Table.db")
# print(db.dialect)
# print(db.get_usable_table_names())

llm = ChatOpenAI(model="gpt-4", temperature=0)
agent_executor = create_sql_agent(llm, db=db, agent_type="openai-tools", verbose=True)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

query=st.chat_input("Ask questions about your data")

if query:
    try:
        response = agent_executor.invoke(query)
        st.session_state.chat_history.append({"Question": query, "Answer": response["output"]})
        for chat in st.session_state.chat_history:
            with st.chat_message("User"):
                st.write(chat["Question"])
            with st.chat_message("Assistant"):
                st.write(chat["Answer"])
    except Exception as e:
        st.error(f"Error:{e}")