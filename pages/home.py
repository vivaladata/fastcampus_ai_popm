# pages/home.py
import streamlit as st
import time

def show_home():
    """홈 화면 표시 로그인"""

    col1, col2, col3 = st.columns([1,5,1])
    with col2:
        st.markdown("<h1 style='text-align: center; font-size: 3em;'>🥼X-pital</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; font-size: 2em;'>X-Ray AI진단서비스</p>", unsafe_allow_html=True)

    st.markdown("<br><br><br><br>", unsafe_allow_html=True)

    st.session_state.login_method = st.selectbox('로그인 방법 선택', ['Google', 'Apple', '카카오', '네이버'], key='login')

    if st.button('로그인'):
        st.session_state.username = '홍길동'  # 로그인 성공 가정
        st.success(f'{st.session_state.username}님, 안녕하세요? X-pital 진단을 위해 보유하신 촬영 이미지를 준비해주세요!')
        time.sleep(1)
        st.session_state.page = "upload_xray"
        st.rerun()