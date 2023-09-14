FROM python:3.11.4

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

ENV FLASK_APP=main.py

ENV DATABASE_URI=sqlite:///db.sqlite

RUN flask db create_all

EXPOSE 8000

CMD ["flask", "run", "--host=0.0.0.0", "--port=8000"]
