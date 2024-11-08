FROM python:3.11-slim
ENV PYTHONIOENCODING utf-8

# install gcc to be able to build packages - e.g. required by regex, dateparser, also required for pandas
RUN apt-get update && apt-get install -y build-essential
RUN pip install flake8

COPY requirements.txt /code/requirements.txt
RUN pip install -r /code/requirements.txt

COPY /src /code/src/
COPY /tests /code/tests/
COPY /scripts /code/scripts/
COPY flake8.cfg /code/flake8.cfg
COPY deploy.sh /code/deploy.sh

WORKDIR /code/

CMD ["python", "-u", "/code/src/component.py"]
