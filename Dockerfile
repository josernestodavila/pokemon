FROM python:3.11-slim as build
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    curl \
    libpq-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

ENV WORKDIR=/opt/app

WORKDIR ${WORKDIR}
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install -r requirements.txt

FROM python:3.11-slim 

RUN apt-get update \
    && apt-get install -y --no-install-recommends\
    curl \
    libpq-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

ENV WORKDIR=/opt/app
WORKDIR ${WORKDIR}

COPY --from=build /opt/venv /opt/venv
COPY . .

ENV PATH="/opt/venv/bin:$PATH"

HEALTHCHECK --interval=30s --timeout=5s CMD curl --silent --fail http://127.0.0.1:8000/health/ || exit 1

CMD ["python", "manage.py", "runserver" "0.0.0.0:8000"]

