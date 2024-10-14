import streamlit as st
from PIL import Image
from typing import Optional
from utils.image_processing import ImageProcessor
from utils.hospital_finder import generate_location_info, get_hospitals_info

class XRayUploader:
    def __init__(self, model=None):
        """XRayUploader 클래스 초기화"""
        self.image_processor = ImageProcessor(model=model)
        self.base_url = "http://localhost:8501"   # 권장하지 않으나, 테스트용으로 사용

    def show_xray_upload(self) -> None:
        """X-Ray 이미지 업로드 및 평가"""

        st.title("🔍 X-ray 진단서비스")

        # 로그인 확인
        if 'username' not in st.session_state:
            st.error("로그인이 필요합니다.")
            st.markdown(f"[로그인 페이지로 이동하기]({self.base_url}/)", unsafe_allow_html=True)  # URL 링크
            return

        st.subheader(f"{st.session_state.username}님! X-Ray 이미지를 업로드 해주세요")
        self.image_processor.display_usage_guide()  # 이용 가이드 표시

        # X-Ray 이미지 업로드 및 분석 진단 요청
        uploaded_file = st.file_uploader("", type=["png", "jpg", "jpeg"])

        if uploaded_file is None:
            st.error("유효한 이미지를 업로드 해주세요.")
            if 'diagnosis' in st.session_state:
                del st.session_state['diagnosis']
            return

        with st.spinner("AI 모델이 이미지를 분석하고 있습니다. 잠시만 기다려주세요..."):
            self.image_processor.process_uploaded_image(uploaded_file)

        # 진단이 완료된 경우 위치 정보 요청
        if 'diagnosis' in st.session_state:
            st.divider()
            st.markdown("<h5>🏥 가까운 병원을 찾아보시려면 선호하시는 지역을 입력해주세요!</h5>", unsafe_allow_html=True)
            user_location = st.text_input(" ", placeholder="예: 서울 강남구, 부산 해운대구, ...")

            if user_location:
                # 위치 정보 생성 및 병원 정보 얻기
                st.session_state.user_location = user_location
                with st.spinner("위치 정보를 생성하고 병원 정보를 불러오고 있습니다. 잠시만 기다려주세요..."):
                    location_info = generate_location_info(user_location)
                    if location_info is None:
                        st.error("위치 정보를 가져올 수 없습니다.")
                        return

                    # 위치 정보 출력 (디버깅용)
                    st.write(f"생성된 위치 정보: {location_info}")

                    hospitals = get_hospitals_info(location_info=location_info, symptom=st.session_state.diagnosis)
                    if not hospitals:
                        st.error("요청하신 지역 근처 병원 정보가 없습니다.")
                        return

                    # 병원 정보를 세션 상태에 저장
                    st.session_state.hospitals = hospitals

                st.session_state.page = "recommend_hospitals"
                st.rerun()

# 페이지 인스턴스 생성
if __name__ == "__main__":
    xray_uploader = XRayUploader()
    xray_uploader.show_xray_upload()
