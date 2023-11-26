# Dockerfile


# 사용할 베이스 이미지 설정
FROM postgres:13

# 초기화 스크립트를 복사


# 환경 변수 설정
ENV POSTGRES_DB manage_project
ENV POSTGRES_USER admin
ENV POSTGRES_PASSWORD admin

COPY ./scripts/ /docker-entrypoint-initdb.d/