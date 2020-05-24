FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

WORKDIR /app/

# Install Poetry
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

RUN apt-get install psql

# Copy poetry.lock* in case it doesn't exist in the repo
COPY ./pyproject.toml ./app/poetry.lock* /app/

RUN poetry install

COPY . /app
RUN pip install -e ./src

EXPOSE 8000
