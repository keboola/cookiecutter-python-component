FROM python:3.13-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# uncomment the following line should you have any troubles installing certain packages which require C/C++ extensions
# to be compiled during installation, eg. numpy, psycopg2, …
# RUN apt-get update && apt-get install -y build-essential

WORKDIR /code/

COPY pyproject.toml .
COPY uv.lock .

ENV UV_PROJECT_ENVIRONMENT="/usr/local/"
RUN uv sync --all-groups --frozen

COPY src/ src
COPY tests/ tests
COPY scripts/ scripts
COPY flake8.cfg .
COPY deploy.sh .

CMD ["python", "-u", "src/component.py"]
