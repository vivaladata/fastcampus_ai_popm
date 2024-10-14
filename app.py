#app.py
import streamlit as st
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
st.set_page_config(page_title="X-pital: AI X-ray 진단 서비스", page_icon="🏥")

import pages.home as home
import pages.upload_xray as upload
import pages.recommend_hospitals as recommend
from utils.setup import load_trained_model, load_hospital_data


@st.cache_resource(show_spinner="모델과 데이터를 불러오는 중입니다...")
def load_resources():
    model = load_trained_model()
    hospital_data = load_hospital_data()
    if model is None or not hospital_data:
        st.error("리소스 로딩에 실패했습니다. 관리자에게 문의해주세요.")
        st.stop()
    return model, hospital_data

model, hospital_data = load_resources()

def load_page():
    page = st.session_state.get("page", "home")
    if page == "home":
        home.show_home()
    elif page == "upload_xray":
        uploader = upload.XRayUploader(model)
        uploader.show_xray_upload()
    elif page == "recommend_hospitals":
        recommend.show_hospital_recommendations()
    else:
        st.error("잘못된 페이지입니다. 홈으로 돌아갑니다.")
        st.session_state.page = "home"
        st.rerun()


# 사이드바 활용 시
# def create_sidebar():
#     """
#     사이드바 영역 : 라디오버튼/셀렉트박스 등으로 변경해도 무방 
#     """

#     st.sidebar.title("Customed navigation")
#     pages = {
#         "home": "홈 화면",
#         "upload_xray": "X-ray 업로드",
#         "recommend_hospitals": "병원 추천"
#     }

#     for page_name, page_title in pages.items():
#         if st.sidebar.button(page_title):
#             st.session_state.page = page_name # 버튼 클릭 시 session_state에 선택한 페이지 이름 저장        
#             st.rerun()


def main():
    if "page" not in st.session_state:
        st.session_state.page = "home"
    
    #create_sidebar()  #필요에 따라 별도의 커스텀 네비게이션을 생성할 수 있음
    load_page()

if __name__ == "__main__":
    main()
