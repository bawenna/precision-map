FROM python:3.8-slim-buster

WORKDIR /app
EXPOSE 5000
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY templates templates
COPY utils.py .
COPY app.py .
COPY sample.json .

# CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
CMD [ "waitress-serve", "--listen=*:5000" , "app:app"]