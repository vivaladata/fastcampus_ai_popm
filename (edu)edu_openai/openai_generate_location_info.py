import os
from dotenv import load_dotenv
import json
from openai import OpenAI, OpenAIError
from pydantic import BaseModel      # 데이터 구조와 유효성 검사를 위한 클래스

# 환경 변수 로드 & OpenAI 클라이언트 초기화
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# 위치 정보를 저장할 데이터 모델
class LocationInfo(BaseModel):
    location: str
    latitude: float
    longitude: float

# 위치 정보를 생성하는 함수
def generate_location_info(location: str) -> LocationInfo:
    try:
        # OpenAI API 호출 및 응답 처리
        response = client.beta.chat.completions.parse(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Make location information in dictionary format including latitude and longitude for a given city."},
                {"role": "user", "content": f"The location : {location}"}
            ],
            temperature=0,
            response_format=LocationInfo,
        )

        # 결과를 JSON 형식으로 변환
        result = response.choices[0].message.parsed
        result_json = result.json()
        print(result)
        print(result_json)  # JSON 

        return result

    except (json.JSONDecodeError, IndexError, OpenAIError) as e:
        # 오류 처리
        print(f"OpenAI API 호출 중 오류: {e}")
        return None
        

generate_location_info("서울")
