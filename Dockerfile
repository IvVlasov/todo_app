FROM python:3.12.4-slim

ADD . /opt/app/backend/

WORKDIR /opt/app/backend/


# Install python modules
RUN pip install --no-cache-dir -U pip setuptools && \
    pip install --no-cache .

EXPOSE 8000
ENTRYPOINT ["bash", "/opt/app/backend/scripts/entrypoint.sh"]
