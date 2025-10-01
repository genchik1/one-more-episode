FROM python:3.13.7-slim-bookworm

WORKDIR /code
COPY . /code/

RUN pip install --upgrade pip \
    && pip install "uv==0.6.12" \
    && uv pip compile pyproject.toml -o requirements.txt \
    && pip install -r requirements.txt \
    && rm -rf /root/.cache

