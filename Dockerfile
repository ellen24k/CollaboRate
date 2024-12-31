# Python 3.12-slim 이미지를 기반으로 설정
# Python 3.12가 설치된 경량 리눅스 제공
FROM python:3.12-slim

# 컨테이너 내에서 작업할 디렉토리를 /app으로 설정 >> 작업 디렉토리 설정
WORKDIR /app

# 필요한 패키지 설치 및 캐시 정리
# apt-get을 사용하여 curl을 설치하고, 설치 후 불필요한 캐시 파일을 삭제
#RUN apt-get update && apt-get install -y \
#    curl \
#    && rm -rf /var/lib/apt/lists/*

# 의존성 파일 복사 및 설치
# 로컬 머신의 requirements.txt 파일을 컨테이너의 현재 디렉토리로 복사
# 그 다음, pip을 사용하여 requirements.txt에 명시된 Python 패키지들을 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 파일 복사
# 로컬 머신의 현재 디렉토리에 있는 모든 파일을 컨테이너의 작업 디렉토리로 복사.
COPY . .

# Streamlit 애플리케이션이 사용하는 포트 노출
# 컨테이너 외부에서 접근할 수 있도록 포트 8501을 열어줌.
EXPOSE 8501

# Streamlit 애플리케이션 실행 명령
# 컨테이너가 시작될 때 Streamlit 애플리케이션을 실행.
CMD ["streamlit", "run", "streamlit_app.py"]`
