import streamlit as st
import random
import time

st.write("함수 로봇을 만나러 오셨군요")
st.caption("한 번 들어왔으니 다시는 나가기 어려울 겁니다..")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role":"assistant", "content": "나는 미스터리 함수 로봇이다. 숫자를 입력하면 내가 그 숫자를 바꿀테니 함수를 맞혀라. 도전하겠느냐?"}]
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("도전하겠습니다"):
    st.session_state.messages.append({"role":"user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        assistant_response = random.choice(
            ["그래."]
        )
        for chunk in assistant_response.split():
            full_response += chunk + " "
            time.sleep(0.05)
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role":"assistant", "content": full_response})

        if prompt == "2x+1":
            response = "정답이다! 얼른 나가"
        else:
            try:
                x = float(prompt)
                y = 2 * x + 1
                response = f"결과는 {y} 이다. 규칙을 좀 알겠느냐?"
            except ValueError:
                response = "숫자를 입력하거나 함수를 맞혀라. (예: 1 또는 5x+2)"

        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

         
         
