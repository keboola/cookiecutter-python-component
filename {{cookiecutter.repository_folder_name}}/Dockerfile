FROM python:3.13-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# uncomment the following line should you have any troubles installing certain packages which require C/C++ extensions
# to be compiled during installation, eg. numpy, psycopg2, …
# RUN apt-get update && apt-get install -y build-essential

WORKDIR /code/

COPY pyproject.toml .

RUN uv pip install --system .

COPY src/ .
COPY tests/ .
COPY scripts/ .
COPY flake8.cfg .
COPY deploy.sh .

CMD ["python", "-u", "/code/src/component.py"]
