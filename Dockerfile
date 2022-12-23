FROM python:3.8

WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY machine.py /app/machine.py
COPY main.py /app/main.py
COPY ./static /app/static
COPY env.py /app/env.py

ENV PATH=/home/app/.local/bin:$PATH
CMD cd /app
CMD [ "python3", "main.py" ]