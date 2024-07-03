FROM python:3.11-alpine

# Create a non-root user and group
RUN addgroup -S olumulo && adduser -S olumulo -G olumulo

COPY build/requirements.txt /opt/demanou/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /opt/demanou/requirements.txt

# Binaries
COPY bin/* /opt/demanou/bin/
RUN chmod +x /opt/demanou/bin/*

# Copy application files
COPY pyproject.toml LICENSE OPENAPI-DESCRIPTION.md /opt/demanou/
COPY vikela/ /opt/demanou/vikela
COPY vikela_core/ /opt/demanou/vikela_core
COPY vikela_models/ /opt/demanou/vikela_models

USER olumulo

ENV PATH="/opt/demanou/bin:$PATH"
ENV PYTHONPATH="/opt/demanou:$PYTHONPATH"
ENV PYTHONUNBUFFERED="1"
ENV PYTHONDONTWRITEBYTECODE="1"

ENV TZ="Africa/Douala"

ENV LOG_LEVEL="info"
ENV LOG_FILE=

# URL for the CouchDB instance (to be set)
ENV COUCHDB_URL=

ENV VIKELA_API_KEY=
ENV VIKELA_SECRET_KEY=

# JWT signing algorithm
ENV JWT_ALGORITHM="HS256"

ENV JWT_SECRET_KEY=
ENV JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30

EXPOSE 6303

ENTRYPOINT ["/opt/demanou/bin/entrypoint.sh"]
