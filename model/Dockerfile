FROM python:3.12

COPY requirements.txt /requirements.txt

RUN python3 -m pip install -r /requirements.txt

COPY src/model.py /model.py
COPY model.pkl /model.pkl

CMD python3 /model.py >> /log.txt
