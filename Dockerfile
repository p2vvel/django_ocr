FROM python

WORKDIR /ocr

COPY ./ ./

RUN  pip install --no-cache-dir -r requirements.txt

RUN apt update && apt install -y tesseract-ocr tesseract-ocr-pol

ENV DEBUG=False

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "ocr.wsgi"]