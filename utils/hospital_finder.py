#utils/hospital_finder.py
import os
import json
import geopy.distance
from openai import OpenAI, OpenAIError
from dotenv import load_dotenv
from pydantic import BaseModel
import streamlit as st

# 환경 변수 로드 및 OpenAI 클라이언트 초기화
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# 위치 정보를 위한 데이터 모델 정의
class LocationInfo(BaseModel):
    location: str
    latitude: float
    longitude: float

# 병원 데이터 로드하는 함수 (JSON)
@st.cache_data
def load_hospital_data() -> list:
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    filepath = os.path.join(base_dir, 'data', 'hospitals.json')
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        st.error(f"병원 데이터 로드 실패: {e}")
        return []

# 거리 계산 함수
def calculate_distance(lat1, lon1, lat2, lon2) -> float:
    return geopy.distance.distance((lat1, lon1), (lat2, lon2)).km

# 1번 LLM : 위치 정보 생성 함수
def generate_location_info(location: str) -> LocationInfo:
    try:
        response = client.beta.chat.completions.parse(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Make location information in dictionary format including latitude and longitude for a given city."},
                {"role": "user", "content": f"The location: {location}"}
            ],
            temperature=0,
            response_format=LocationInfo,
        )
        return response.choices[0].message.parsed
    except (json.JSONDecodeError, OpenAIError) as e:
        st.error(f"OpenAI API 호출 중 오류: {e}")
        return None

# 2번 LLM : 적합한 병원 선정하는 함수
def get_hospitals_info(location_info: LocationInfo, symptom="폐렴") -> list:
    if client is None:
        st.error("OpenAI 클라이언트가 초기화되지 않았습니다.")
        return []

    try:
        latitude, longitude = location_info.latitude, location_info.longitude
        hospitals_json = load_hospital_data()

        if not hospitals_json:
            st.error("병원 데이터를 로드할 수 없습니다.")
            return []

        # 유효한 병원만 필터링 및 거리 계산
        valid_hospitals = []
        for hospital in hospitals_json:
            if 'latitude' in hospital and 'longitude' in hospital:
                # 위경도 기반으로 거리 계산
                hospital_latitude = hospital['latitude']
                hospital_longitude = hospital['longitude']
                distance = calculate_distance(latitude, longitude, hospital_latitude, hospital_longitude)

                # 거리 정보를 추가한 병원 데이터 복사본 생성
                hospital_dist = hospital.copy()  # 원본 데이터 수정 방지
                hospital_dist['distance'] = distance
                valid_hospitals.append(hospital_dist)

        if not valid_hospitals:
            st.error("유효한 병원이 없습니다.")
            return []

        # 거리 기준으로 병원 정렬 (상위 5개 선택)
        nearest_hospitals = sorted(
            valid_hospitals, key=lambda x: x['distance']
        )[:5]


        # OpenAI API 요청을 위한 메시지 구성
        hospital_info_prompt_system = (
            f"From the following list, select up to 3 hospitals that are most suitable for treating '{symptom}' based on their proximity. "
            "Return only a JSON list of dictionaries with their rank, id, and name with no markdown.\n"
        )

        # 병원 정보 문자열 생성 
        hospital_info_list = [
            f"Hospital ID: {hospital['id']}, Name: {hospital['name']}, "
            f"Latitude: {hospital['latitude']}, Longitude: {hospital['longitude']}, "
            f"Specialties: {', '.join(hospital.get('specialties', []))}, "
            f"Distance: {hospital['distance']:.2f} km"
            for hospital in nearest_hospitals
        ]

        hospital_info_prompt_user = "\n".join(hospital_info_list)

        # 응답 형식 예시 추가
        selection_format = (
            "Format: [{\"rank\": 1, \"id\": \"H000000\", \"name\": \"A병원\"}]"
        )

        # 최종 사용자 프롬프트 생성
        hospital_info_prompt_user += "\n\n" + selection_format

        messages = [
            {"role": "system", "content": hospital_info_prompt_system},
            {"role": "user", "content": hospital_info_prompt_user}
        ]

        # OpenAI API 호출
        hospital_response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0,
            max_tokens=100,
        )

        # 응답 처리 및 JSON으로 변환
        assistant_reply = hospital_response.choices[0].message.content.strip()
        try:
            selected_hospitals = json.loads(assistant_reply)
        except json.JSONDecodeError as e:
            st.error(f"OpenAI 응답을 처리하는 중 오류가 발생했습니다: {e}")
            return []

        # 선택된 병원 정보 가져오기
        final_hospitals = []
        for selected in selected_hospitals:
            hospital = next((h for h in nearest_hospitals if h['id'] == selected['id']), None)
            if hospital:
                hospital['rank'] = selected['rank']
                final_hospitals.append(hospital)

        return final_hospitals

    except (OpenAIError, Exception) as e:
        st.error(f"병원 정보를 처리하는 중 오류가 발생했습니다: {e}")
        return []


## [추가] 2번의 get_hospitals_info()을 LLM을 활용하지 않은 버전        
# def get_hospitals_info(location_info: LocationInfo, symptom="폐렴") -> list:
#     try:
#         latitude, longitude = location_info.latitude, location_info.longitude
#         hospitals_json = load_hospital_data()
#
#         if not hospitals_json:
#             st.error("병원 데이터를 로드할 수 없습니다.")
#             return []
#
#         # 유효한 병원만 필터링
#         valid_hospitals = []
#         for hospital in hospitals_json:
#             if 'latitude' in hospital and 'longitude' in hospital:
#                 distance = calculate_distance(latitude, longitude, hospital['latitude'], hospital['longitude'])
#                 hospital['distance'] = distance
#                 valid_hospitals.append(hospital)
#
#         # 가까운 병원 순으로 정렬
#         nearest_hospitals = sorted(valid_hospitals, key=lambda x: x['distance'])[:5]
#
#         return nearest_hospitals
#
#     except Exception as e:
#         st.error(f"병원 정보를 처리하는 중 오류가 발생했습니다: {e}")
#         return []


# 3번 LLM : 후속 메시지를 생성하는 함수
def generate_followup_message() -> str:
    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You're a kind Korean nurse."},
                {"role": "user", "content": "Briefly summarize three pieces of advice for pneumonia-suspected patients before going to the hospital in Korean."}
            ],
            temperature=0.8,
            max_tokens=300
        )
        return response.choices[0].message.content
    except OpenAIError as e:
        st.error(f"후속 메시지 생성 중 오류: {e}")
        return "후속 메시지 생성에 실패했습니다."
