FROM python:3.13.7-slim

WORKDIR /code

# Копируем только файлы зависимостей сначала для лучшего кэширования
COPY pyproject.toml ./

# Устанавливаем зависимости одним слоем и очищаем кэш
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir "uv==0.6.12" && \
    uv pip compile pyproject.toml -o requirements.txt && \
    pip install --no-cache-dir -r requirements.txt

# Копируем остальной код
COPY . .

# Удаляем ненужные файлы для уменьшения размера
RUN find . -type f -name "*.pyc" -delete && \
    find . -type d -name "__pycache__" -delete && \
    rm -rf /root/.cache /tmp/*