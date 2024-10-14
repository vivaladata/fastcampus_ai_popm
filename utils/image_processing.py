# utils/image_processing.py

import streamlit as st
import numpy as np
from PIL import Image
from typing import Optional
import tensorflow as tf

class ImageProcessor:
    def __init__(self, model: Optional[tf.keras.Model] = None):
        """ImageProcessor 클래스 초기화"""
        if model is None:
            st.error("모델이 제공되지 않았습니다.")
            raise ValueError("모델이 필요합니다.")
        self.model = model

    @staticmethod
    def preprocess_image(_image: Image.Image) -> Optional[np.ndarray]:
        """이미지 전처리"""
        try:
            if _image.size[0] < 300 or _image.size[1] < 300:
                st.error("이미지 해상도가 너무 낮습니다. 최소 300x300 이상의 이미지를 업로드해주세요.")
                return None

            _image = _image.resize((224, 224)).convert('RGB')
            return np.expand_dims(np.array(_image) / 255.0, axis=0)
        except Exception as e:
            st.error(f"이미지 전처리 중 오류 발생: {str(e)}")
            return None

    def process_uploaded_image(self, uploaded_file: Optional[st.runtime.uploaded_file_manager.UploadedFile]) -> None:
        """업로드된 이미지 처리"""
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption=f'{st.session_state.username}님의 X-Ray 이미지', use_column_width=True)

            if st.button('진단 시작'):
                self.diagnose_image(image)

    def diagnose_image(self, image: Image.Image) -> None:
        """이미지 진단 및 결과 표시"""
        if self.model is None:
            st.error("진단모델 로딩 실패")
            return

        processed_image = self.preprocess_image(image)
        if processed_image is not None:
            prediction = self.model.predict(processed_image)
            self.display_diagnosis(prediction)
        else:
            st.error("이미지 전처리에 실패하였습니다.")

    def display_diagnosis(self, prediction: np.ndarray) -> None:
        """진단 결과 표시"""
        pneumonia_probability = float(prediction[0]) * 100  # 폐렴 확률을 백분율로 변환

        if pneumonia_probability > 60:
            st.session_state.diagnosis = "pneumonia"   # 세션 상태에 저장
            diagnosis_text = f"<h4><strong>X-pital 진단 결과: 폐렴 소견이 있습니다.</strong> (폐렴 확률: {pneumonia_probability:.2f}%)</h4>"
        else:
            diagnosis_text = f"<h4><strong>X-pital 진단 결과: 현재는 폐렴 소견이 없습니다만, 지속적으로 건강은 관리하세요!</strong> (폐렴 확률: {pneumonia_probability:.2f}%)</h4>"

        st.markdown(diagnosis_text, unsafe_allow_html=True)

    def display_usage_guide(self) -> None:
        """이용 가이드 표시"""
        st.markdown("### 📢 이용가이드")
        st.markdown("""
        1. 이미지는 정면이 잘 보이는 방향으로 올려주세요.
        2. "png", "jpg", "jpeg" 이미지만 넣어주세요.
        3. 해상도가 300x300 이상의 이미지를 넣어주세요.
        4. 진단 결과까지 최대 5분 소요될 수 있습니다.
        5. 의료법 및 개인정보보호법에 따라 본인 이외의 허위 정보를 올리지 마세요.
        """)

