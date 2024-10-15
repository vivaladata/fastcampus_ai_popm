# AI X-ray 진단 서비스 Mockup


## Overview
이 앱은 패스트캠퍼스 교육용으로 AI Product Owner(PO) 입문자를 위해 교육적인 목적으로 설계된 **Mockup**입니다.
AI 기반의 X-ray 진단 및 병원 추천 서비스로, Part3 실습 2에 해당하는 영역입니다. 실습 1이 선행되어야 진행 가능한 후속 실습입니다.
사용자가 자신의 X-ray 이미지를 업로드하면, AI 모델이 이를 분석하여 폐렴 가능성을 평가하고 결과를 제공하고, 이후 사용자의 선호지역 정보를 기반으로 인근 병원을 추천합니다.


## Main Features

### 1. 홈 화면 및 약식 로그인화면
- 사용자는 '홈' 페이지에서 제공된 로그인 옵션(Google, Apple, 카카오, 네이버)을 통해 로그인할 수 있습니다.
- 로그인 후 사용자에 한해서 X-ray 이미지를 업로드하여 AI 분석을 받을 수 있습니다.

### 2. X-ray 이미지 업로드 및 진단 
- 사용자가 X-ray 이미지를 업로드하면, AI 모델이 이를 분석하여 폐렴 여부를 판단합니다. 분석 결과가 폐렴일 경우, 사용자는 이어서 위치 정보를 입력하여 가까운 병원 추천을 받을 수 있습니다.
- 실습1에서 학습한 AI 모델은 사전에 **models** 디렉토리에 적재합니다.

### 3. 병원 추천 및 추가 메시지(Follow-up Messages) 생성
- 사용자가 입력한 위치 정보와 OpenAI API를 활용해 적절한 병원 목록을 제공합니다.
- 병원 정보는 JSON 데이터로 저장되어 있으며, 가까운 병원들을  중 추천합니다.


## 프로젝트 구조 (Project Structure)

  ```sh

  xray_handson/
  ├── app.py                  # 메인 Streamlit 앱 파일
  ├── data/
  │   └── hospitals.json      # 병원 데이터
  ├── models/
  │   └── model3_ResNet.h5    # 훈련된 AI 모델 (본인이 작업한 내용으로 변경 가능)
  ├── pages/
  │   ├── home.py                  # 홈 
  │   ├── recommend_hospitals.py   # 병원 추천 페이지
  │   ├── upload_xray.py           # X-ray 업로드 페이지
  ├── utils/
  │   ├── hospital_finder.py  # 병원 정보 처리 로직
  │   ├── image_processing.py # 이미지 처리 및 진단
  │   ├── html_helpers.py     
  │   └── setup.py            # 모델 및 병원 데이터 로드 설정
  └── requirements.txt        # 필수 Python 패키지 목록

  ```


## How to Run

### 요구사항 (Prerequisites)
- Python 3.9 이상
- 필요한 Python 패키지는 `requirements.txt` 파일에서 확인하고 설치할 수 있습니다.


### 앱 진입 시점 (Entry Point)
- `app.py` 파일을 통해 실행됩니다.


### 실행 코드 (Run Code)
1. **환경 설정**
    ```sh
    pip install -r requirements.txt
    ```

2. **앱 실행**
    ```sh
    streamlit run app.py
    ```
   **2-1. 이전의 Stremlit 캐시를 지우고 앱 실행 시**
    ```sh
    streamlit run app.py --server.port 8501 --server.address localhost --server.enableCORS false --global.developmentMode false
    ```

## 활용 라이브러리
- **OpenAI API**: 사용자의 입력에 따라 위치 정보 생성 및 후속 조언을 제공합니다.
- **Streamlit**: 웹 기반의 UI 구축을 위해 사용되었습니다.
- **TensorFlow**: X-ray 이미지를 분석하는 AI 모델을 제공합니다.
- **Pandas, Geopy**: 데이터 분석 및 거리 계산에 사용되었습니다.


## 본 파일 사용에 대한 주의사항
- 학습 과정에서 필요한 임의의 주석처리 및 임의의 코드들이 혼재되어 있습니다.
- 본 파일은 패스트캠퍼스 'AI 시대, PM/PO 를 위한 한 번에 끝내는 AI 서비스 기획 실무' Part 3 교육안입니다. 작성자와 협의되지 않은 무단배포 및 영업적 활용을 금합니다.
