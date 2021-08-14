# fetches Python image based on Slim
FROM python:3.8-slim

# setup working directory
WORKDIR /workdir

# copy folder into working directory
COPY src/ /workdir
RUN pip3 install -U pip
RUN pip3 install -r requirements.txt


CMD ["python", "/workdir/run.py"]
