FROM python:3.13.7

WORKDIR /code
COPY . /code/

ENV PIP_DEFAULT_TIMEOUT=100
ENV PIP_RETRIES=5

RUN pip install --upgrade pip \
    && pip install "uv==0.6.12" \
    && uv pip compile pyproject.toml -o requirements.txt \
    && pip install -r requirements.txt \
    && rm -rf /root/.cache

