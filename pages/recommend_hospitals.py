# pages/recommend_hospitals.py
import streamlit as st
from utils.hospital_finder import (
    get_hospitals_info,
    generate_followup_message,
    generate_location_info,
    LocationInfo
)
from utils.html_helpers import create_button_html # 버튼 생성 템플릿

def display_hospital_info(hospital: dict, index: int) -> None:
    """병원 정보를 화면에 표시"""
    st.markdown(f"### {index} : **{hospital['name']}**")

    cols = st.columns([3, 1, 1])
    with cols[0]:
        st.write(f"**주소**: {hospital['address']} ({hospital['distance']:.2f} km)")
    
    with cols[1]:
        if hospital.get('phone') and hospital['phone'] != '정보 없음':
            st.markdown(create_button_html(f"tel:{hospital['phone']}", "전화걸기", "#008CBA"), unsafe_allow_html=True)
    
    with cols[2]:
        if hospital.get('website') and hospital['website'] != '정보 없음':
            st.markdown(create_button_html(hospital['website'], "홈페이지", "#4CAF50"), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    with st.expander(f"▼ {hospital['name']}에 대한 더 많은 정보"):
        st.write(f"**진료과목**: {', '.join(hospital.get('specialties', []))}")
        st.write(f"**운영시간**: {hospital.get('hours', '정보 없음')}")
        st.write(f"**주말 운영시간**: {hospital.get('weekend_availability', '정보 없음')}")
        st.write(f"**전화번호**: {hospital.get('phone', '정보 없음')}")

    st.markdown("---")

def show_hospital_recommendations():
    """사용자의 진단 결과와 위치를 기반으로 병원 추천 리스트를 표시"""
    st.title("🏥 병원 추천 리스트")

    if 'diagnosis' not in st.session_state or 'user_location' not in st.session_state:
        st.error("진단 정보와 사용자 위치가 필요합니다. 진단 페이지로 돌아가 주세요.")
        return

    diagnosis = st.session_state.diagnosis
    user_location_str = st.session_state.user_location

    # 위치 정보 생성
    location_info = generate_location_info(user_location_str)
    if location_info is None:
        st.error("위치 정보를 가져올 수 없습니다.")
        return

    # 병원 정보 얻기
    hospitals = get_hospitals_info(location_info=location_info, symptom=diagnosis)
    if not hospitals:
        st.error("요청하신 지역 근처 병원정보가 없습니다.")
        return

    followup_message = generate_followup_message()
    
    # 병원 정보 표시 
    for i, hospital in enumerate(hospitals[:3], start=1):
        display_hospital_info(hospital, i)

    if followup_message: #text가 있으면 출력
        with st.container(border=True):
            st.subheader("📋 병원 방문 전까지 아래 내용을 참고하세요 !")
            st.write(followup_message)
                    


# 페이지 실행
if __name__ == "__main__":
    show_hospital_recommendations()