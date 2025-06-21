FROM python:3.12-slim

WORKDIR /app

COPY ./requirements.txt /app

RUN pip install -r requirements.txt

COPY src/ /app

EXPOSE 8501

CMD ["streamlit", "run", "app.py"]