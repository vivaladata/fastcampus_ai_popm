import os
import json
import tensorflow as tf
import streamlit as st

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

@st.cache_resource
def load_trained_model():
    model_path = os.path.join(BASE_DIR, "models", "model3_ResNet.h5")
    if not os.path.exists(model_path):
        st.error(f"모델 파일을 찾을 수 없습니다: {model_path}")
        return None
    
    with st.spinner('모델을 로딩 중입니다...'):
        try:
            model = tf.keras.models.load_model(model_path)
            return model
        except Exception as e:
            st.error(f"모델 로딩 중 오류 발생: {str(e)}")
            return None

@st.cache_data 
def load_hospital_data(filepath=None):
    if filepath is None:
        filepath = os.path.join(BASE_DIR, "data", "hospitals.json")
    if not os.path.exists(filepath):
        st.error(f"데이터 파일을 찾을 수 없습니다: {filepath}")
        return []
    
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return json.load(file)
    except json.JSONDecodeError:
        st.error("병원 데이터 파일 형식이 올바르지 않습니다.")
        return []
    except Exception as e:
        st.error(f"데이터 로딩 중 오류 발생: {str(e)}")
        return []