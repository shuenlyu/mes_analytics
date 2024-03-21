FROM python:3.9-slim-buster
LABEL maintainer="Shuen.Lyu <shuen.lyu@uct.com>"
ENV PYTHONUNBUFFERED=TRUE

COPY . /MES_Analytics
WORKDIR /MES_Analytics

RUN pip install -r requirements.txt
CMD [ "gunicorn", "--workers=5","--timeout=90", "--threads=2", "-b :8050", "main:server"]

