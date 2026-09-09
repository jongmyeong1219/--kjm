import streamlit as st
import random

# 페이지 설정
st.set_page_config(
    page_title="가위바위보 게임",
    page_icon="✌️",
    layout="centered"
)

st.title("✌️✊🖐️ 가위바위보 게임")
st.write("아래 버튼 중 하나를 선택해서 컴퓨터와 대결해보세요!")

# 전적 관리를 위한 세션 상태(Session State) 초기화
if 'wins' not in st.session_state:
    st.session_state.wins = 0
if 'losses' not in st.session_state:
    st.session_state.losses = 0
if 'draws' not in st.session_state:
    st.session_state.draws = 0

# 가위바위보 옵션 정의
options = ["가위 ✌️", "바위 ✊", "보 🖐️"]

# 버튼 레이아웃 (3개의 열로 나누기)
col1, col2, col3 = st.columns(3)
user_choice = None

with col1:
    if st.button("가위 ✌️", use_container_width=True):
        user_choice = "가위 ✌️"
with col2:
    if st.button("바위 ✊", use_container_width=True):
        user_choice = "바위 ✊"
with col3:
    if st.button("보 🖐️", use_container_width=True):
        user_choice = "보 🖐️"

# 플레이어가 선택했을 때 게임 진행
if user_choice:
    computer_choice = random.choice(options)
    
    st.write("---")
    st.subheader("🎮 대결 결과")
    
    res_col1, res_col2 = st.columns(2)
    with res_col1:
        st.info(f"👤 **나의 선택:**\n### {user_choice}")
    with res_col2:
        st.warning(f"💻 **컴퓨터의 선택:**\n### {computer_choice}")
    
    # 승패 판정 로직
    if user_choice == computer_choice:
        st.info("🤝 **비겼습니다!**")
        st.session_state.draws += 1
    elif (
        (user_choice == "가위 ✌️" and computer_choice == "보 🖐️") or
        (user_choice == "바위 ✊" and computer_choice == "가위 ✌️") or
        (user_choice == "보 🖐️" and computer_choice == "바위 ✊")
    ):
        st.success("🎉 **이겼습니다! 축하합니다!**")
        st.session_state.wins += 1
    else:
        st.error("😭 **졌습니다... 다시 도전해보세요!**")
        st.session_state.losses += 1

# 전적 표시
st.write("---")
st.subheader("📊 현재 전적")
score_col1, score_col2, score_col3 = st.columns(3)

score_col1.metric("승리", f"{st.session_state.wins}회")
score_col2.metric("패배", f"{st.session_state.losses}회")
score_col3.metric("무승부", f"{st.session_state.draws}회")

# 전적 초기화 버튼
if st.button("전적 초기화 🔄"):
    st.session_state.wins = 0
    st.session_state.losses = 0
    st.session_state.draws = 0
    st.rerun()
