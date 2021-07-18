FROM python:3.8-slim-buster

WORKDIR /app
EXPOSE 5000 8000
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY templates templates
COPY utils.py .
COPY app.py .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]