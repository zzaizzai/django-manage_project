# # Dockerfile

# FROM python:3.9


# WORKDIR /app/src
# RUN pip install --upgrade pip && pip install -r requirements.txt


# # 컨테이너 실행 시 실행될 명령
# CMD ["python", "django/manage.py", "runserver", "0.0.0.0:8001"]



FROM python:3.9
ENV PYTHONUNBUFFERED=1
WORKDIR /django


COPY requirements.txt* /django/
# RUN pip install pipenv
# COPY Pipfile* /backend/
# RUN pipenv requirements > requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . /django/

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8001"]

EXPOSE 8001