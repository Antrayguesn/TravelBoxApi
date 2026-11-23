FROM python:3.12-alpine

RUN apk add --no-cache \
    build-base \
    libffi-dev \
    postgresql-dev

WORKDIR /app

COPY dist/travel_box_api-*.tar.gz /app/

RUN pip install --no-cache-dir travel_box_api-*.tar.gz \
    && pip install --no-cache-dir gunicorn

EXPOSE 5000

CMD ["gunicorn", "-w", "1", "-b", "0.0.0.0:5000", "--timeout", "600", "travel_box_api.__main__:app"]