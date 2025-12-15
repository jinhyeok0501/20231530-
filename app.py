import streamlit as st
import google.generativeai as genai
import os
import re # Add import for re module

# Function to get emoji based on positivity and empathy
def get_emoji(positivity, empathy):
    if positivity <= 50 and empathy <= 50:
        return "🧐"  # T + 부정 = 사려 깊음 / 분석적
    elif positivity > 50 and empathy <= 50:
        return "🤔"  # T + 긍정 = 낙관적 / 분석적
    elif positivity <= 50 and empathy > 50:
        return "😥"  # F + 부정 = 슬픔 / 공감
    else:
        return "🥰"  # F + 긍정 = 사랑스러움 / 공감

# Initialize session state for persistence
if "diary_content" not in st.session_state:
    st.session_state.diary_content = ""
if "robot_response" not in st.session_state:
    st.session_state.robot_response = ""
if "emotion_color" not in st.session_state:
    st.session_state.emotion_color = ""

st.set_page_config(layout="centered")

# --- 1. 설정 (사이드바) ---
with st.sidebar:
    st.title("⚙️ 설정")
    api_key = st.text_input("Gemini API 키 입력", type="password", help="Google Cloud에서 발급받은 Gemini API 키를 입력하세요.")

    st.subheader("🤖 로봇 성격 튜닝")
    positivity = st.slider("긍정 회로", 0, 100, 50, help="0=비관적/현실비판, 100=낙관적/희망회로")
    empathy = st.slider("공감 지수", 0, 100, 50, help="0=T(해결책/팩트), 100=F(공감/위로)")

    if api_key:
        genai.configure(api_key=api_key)
        st.success("API 키가 설정되었습니다!")
    else:
        st.warning("API 키를 입력해주세요.")
    

# --- 2. 메인 화면 (UI) ---
st.title("📖 마음을 읽는 일기 로봇, 에코")

# 상태 아이콘
st.markdown(f"<h1 style='text-align: center;'>{get_emoji(positivity, empathy)}</h1>", unsafe_allow_html=True)

st.subheader("오늘의 일기를 작성해주세요.")
st.session_state.diary_content = st.text_area("일기장", height=200, value=st.session_state.diary_content, key="diary_input")

if st.button("[일기 전달하기]"):
    if not api_key:
        st.error("API 키를 먼저 입력해주세요.")
    elif not st.session_state.diary_content:
        st.error("일기 내용을 입력해주세요.")
    else:
        # --- 3. AI 로직 (Gemini API - google.generativeai) ---
        # System Instruction (프롬프트)
        system_instruction = f"""
        너는 사용자의 일기를 읽고 답장해주는 로봇이야.
        너의 성격은 positivity({positivity})과 empathy({empathy}) 수치에 따라 결정돼.
        positivity: 0=비관적/현실비판, 100=낙관적/희망회로
        empathy: 0=T(해결책/팩트), 100=F(공감/위로)

        답변 형식: 반드시 아래 3가지 내용을 포함해서 자연스럽게 말해줘.
        1. 🔍 오늘의 핵심 사건: 일기에서 가장 중요한 사건 요약.
        2. 🎨 감정의 색깔: 이 일기의 감정을 대표하는 색상 이름과 Hex Code (예: 우울한 블루 #0000FF).
        3. 🤖 에코의 답장: 설정된 성격에 맞춰서, 일기 내용 중 구체적인 사건을 언급하며 조언하거나 위로해줘.
        """

        # 1. 모델을 가장 안정적인 'gemini-pro'로 변경
        model = genai.GenerativeModel("models/gemini-2.5-flash")
        chat = model.start_chat(history=[])
        
        # 2. 구버전에서도 잘 작동하도록 '성격(시스템 프롬프트)'을 내용과 합쳐서 보냄
        full_prompt = system_instruction + "\n\n[오늘의 일기]:\n" + st.session_state.diary_content
        
        response = chat.send_message(full_prompt)
        st.session_state.robot_response = response.text

        # Extract emotion color from the response using regex
        try:
            color_match = re.search(r'#(?:[0-9a-fA-F]{3}){1,2}', st.session_state.robot_response)
            if color_match:
                st.session_state.emotion_color = color_match.group(0)
            else:
                st.session_state.emotion_color = "#FFFFFF" # Default to white
        except Exception as e:
            st.error(f"감정 색깔 파싱 중 오류 발생: {e}")
            st.session_state.emotion_color = "#FFFFFF" # Default to white

        st.rerun()

# --- 4. 결과 화면 & 피드백 (로봇 과목 요소) ---
if st.session_state.robot_response:
    st.markdown(f"<div style='background-color:{st.session_state.emotion_color}; padding: 20px; border-radius: 10px;'>", unsafe_allow_html=True)
    st.write(st.session_state.robot_response)
    st.markdown("</div>", unsafe_allow_html=True)

    with st.expander("🛠️ AI 학습시키기 (피드백)"):
        st.subheader("로봇의 분석이 틀렸나요?")
        feedback_emotion = st.text_input("내가 느낀 진짜 감정", key="feedback_emotion")
        feedback_wish = st.text_area("로봇에게 바라는 점", key="feedback_wish")

        if st.button("[수정 데이터 전송]"):
            st.success("피드백 감사합니다! 에코가 더 똑똑해질 거예요! (데이터 수집 완료)")
