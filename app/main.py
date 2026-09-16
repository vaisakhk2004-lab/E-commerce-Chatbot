import streamlit as st
from pathlib import Path
from router import route
from FAQ import chain,load_data
from sql import sql_chain
faq_path=(Path(__file__).parent /'resources'/"faq_data.csv")
load_data(faq_path)
def ask(query):
    router=route(query).name
    if router=='faq':
        return chain(query)
    elif router == 'sql':
        return sql_chain(query)
    else:return f'router {router} not enabled'


st.title("🛍️ E-Commerce AI Assistant")
query=st.chat_input("Ask me !")

if 'messages' not in st.session_state:
    st.session_state['messages']=[]
for message in st.session_state.messages:
    with st.chat_message(message['role']):
         st.markdown(message['message'], unsafe_allow_html=True)
if query:
    with st.chat_message('user'):
        st.markdown(query)
    st.session_state.messages.append({'role':'User','message':query})
    response=ask(query)
    with st.chat_message('Assistant'):
        st.markdown(response)
    st.session_state.messages.append({'role': 'Assistant', 'message': response
                                      })