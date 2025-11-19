import streamlit as st
import random
import time

st.write("오늘은 챗봇 만들기 할거야")
st.caption("단, 수업에서 다룬 내용만 대답 가능")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role":"assistant", "content": "안녕하세요! 챗봇입니다. 무엇을 도와드릴까요?"}]
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Hello?"):
    st.session_state.messages.append({"role":"user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        assistant_response = random.choice(
            ["안녕하세요!", "반가워요!", "무엇을 도와드릴까요?"]
        )
        for chunk in assistant_response.split():
            full_response += chunk + " "
            time.sleep(0.05)
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role":"assistant", "content": full_response})
