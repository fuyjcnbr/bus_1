FROM python:3.12

COPY requirements.txt /requirements.txt

RUN python3 -m pip install -r /requirements.txt

COPY src/metric.py /metric.py


CMD python3 /metric.py >> /log.txt
