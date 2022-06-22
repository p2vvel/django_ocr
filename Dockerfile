FROM python

WORKDIR /var/src/app

COPY requirements.txt .

RUN apt update && apt install -y tesseract-ocr tesseract-ocr-pol
RUN pip install -r requirements.txt

COPY ocr/ .

CMD bash -c "mkdir -p /static/static/ && mkdir -p /static/media/ && \
        python manage.py migrate && \
        python manage.py collectstatic --no-input && \
        python -m gunicorn --bind 0.0.0.0:8000 ocr.wsgi"
