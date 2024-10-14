import os
import dotenv
import json
from openai import OpenAI, OpenAIError

# 환경 변수 로드 및 OpenAI 클라이언트 초기화
dotenv.load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

def generate_followup_message():
    """조언 등 Followup Msg 추가"""
    try:
        # OpenAI API 호출
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You're a kind Korean nurse."},
                {"role": "user", "content": "Briefly but kindly summarize the three pieces of advice needed for patients \
                    suspected of having pneumonia before going to the hospital in Korean. Start with 'Advice'. Use bullet-style if you want."}
            ],
            temperature=0.8,
            max_tokens=300
        )

        # 메시지 추출
        followup_message = response.choices[0].message.content
        return followup_message

    except Exception as e:
        return f"오류 발생: {e}"




# 함수 호출 예제
result = generate_followup_message()
print(result)