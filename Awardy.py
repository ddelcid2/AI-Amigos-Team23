import openai
import streamlit as st
import time

assistant_id = "asst_D7MlHh3PgfTA02c8iEUj6RFu"

client = openai

if "start_chat" not in st.session_state:
    st.session_state.start_chat =  False
if "thread_id" not in st.session_state:
    st.session_state.thread_id = None
    
st.set_page_config(page_title="AWARDY", page_icon=":trophy:")

openai.api_key = "sk-proj-XeZVha5h4EqmUJkUJgSLT3BlbkFJbsnivsv2hdd43YMoKZTv"

if st.sidebar.button("Start Chat"):
    st.session_state.start_chat =  True
    thread =  client.beta.threads.create()
    st.session_state.thread_id = thread.id
    
st.title("Awardy")
st.write("Hello I am Awardy :) your personal NSF Awards Assistant!")

if st.button("Exit Chat"):
    st.session_state.messages = [] # Clear chat history
    st.session_state.start_chat =  False #Reset chat state
    st.session_state.thread_id = None
    
if st.session_state.start_chat:
    if "openai_model" not in st.session_state:
        st.session_state.openai_model = "gpt-4o-mini-2024-07-18"
    if "messages" not in st.session_state:
        st.session_state.messages = []
        
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
    if prompt := st.chat_input("How can I help?"):
        
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
            
        client.beta.threads.messages.create(
                thread_id=st.session_state.thread_id,
                role="user",
                content=prompt
            )
        
        run = client.beta.threads.runs.create(
            thread_id=st.session_state.thread_id,
            assistant_id=assistant_id,
            instructions="You are designed to answer questions about awards from the NSF.gov/AwardSearch website. The NSF.gov/AwardSearch website is an essential resource for a diverse range of users, providing comprehensive and transparent access to information about NSF-funded research projects and awards. It supports researchers, academic institutions, policymakers, businesses, journalists, educators, students, and the general public by offering detailed data that promotes collaboration, informed decision-making, and public engagement in scientific research. If you do not know any award data do not say to visit the NSF website instead make it up and make it look smart and credible."
        )
        
        while run.status != 'completed':
            time.sleep(1)
            run = client.beta.threads.runs.retrieve(
                thread_id=st.session_state.thread_id,
                run_id=run.id
            )
        
        messages = client.beta.threads.messages.list(
            thread_id=st.session_state.thread_id
        )
        assistant_messages_for_run = [
            message for message in messages
            if message.run_id == run.id and message.role == "assistant"
        ]
        for message in assistant_messages_for_run:
            st.session_state.messages.append({"role": "assistant", "content": message.content[0].text.value})
            with st.chat_message("assistant"):
                st.markdown(message.content[0].text.value)
                
else:
    st.write("Click 'Start Chat' to begin.")
        


        
        
        
        
        