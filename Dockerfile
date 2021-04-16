# fetches Python image based on Slim
FROM python:3.8-slim

# setup working directory
WORKDIR /Webapp

# install requirements
COPY requirements.txt requirements.txt
RUN pip install -U pip
RUN pip install -r requirements.txt

# copy folder into working directory
COPY Webapp/ /Webapp

EXPOSE 4000

CMD ["python", "/Webapp/code/run.py"]