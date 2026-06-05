FROM python:3-slim

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/

RUN mkdir -p downloaded-scripts
VOLUME ["/usr/src/app/downloaded-scripts"]

CMD ["python", "src/main.py"]
