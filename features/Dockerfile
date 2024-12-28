FROM python:3.12

COPY requirements.txt /requirements.txt

RUN python3 -m pip install -r /requirements.txt

COPY src/features.py /features.py

CMD python3 /features.py >> /log.txt
