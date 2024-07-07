# Stage 1: Build environment
FROM python:3.11-alpine AS build-env

# Install build dependencies
RUN apk update \
    && apk add --no-cache \
        build-base \
        python3-dev \
        libffi-dev

COPY build/requirements.txt /opt/demanou/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /opt/demanou/requirements.txt

# Stage 2: Runtime environment
FROM python:3.11-alpine

# Create a non-root user and group
RUN addgroup -S olumulo && adduser -S olumulo -G olumulo

# Copy built Python dependencies from the build-env stage
COPY --from=build-env /usr/local/lib/python3.11/site-packages/ /usr/local/lib/python3.11/site-packages/
COPY --from=build-env /usr/lib/python3.11/site-packages/ /usr/lib/python3.11/site-packages/

# Binaries
COPY bin/* /opt/demanou/bin/
RUN chmod +x /opt/demanou/bin/*

# Copy application files
COPY pyproject.toml LICENSE DOCUMENTATION.md /opt/demanou/
COPY vikela/ /opt/demanou/vikela
COPY vikela_core/ /opt/demanou/vikela_core
COPY vikela_models/ /opt/demanou/vikela_models

USER olumulo

ENV PATH="/opt/demanou/bin"
ENV PYTHONPATH="/opt/demanou"
ENV PYTHONUNBUFFERED="1"
ENV PYTHONDONTWRITEBYTECODE="1"

ARG APP_NAME
ARG APP_VERSION

ENV TZ="Africa/Douala"
ENV ROOT_PATH="/api"
ENV CLIENT_USERAGENT="$APP_NAME/$APP_VERSION"
ENV COUCHDB_URL=
ENV COUCHDB_AUTH_ROLES="_admin"
ENV COUCHDB_AUTH_USERNAME=
ENV COUCHDB_AUTH_TOKEN=""
ENV DEFAULT_USER_GROUPS="user"
ENV COOKIE_SESSION_NAME="vikela-session"
ENV COOKIE_SESSION_MAX_AGE=""
ENV COOKIE_SESSION_EXPIRES=""
ENV COOKIE_SESSION_PATH="/"
ENV COOKIE_SESSION_DOMAIN=""
ENV COOKIE_SESSION_SECURE="false"
ENV COOKIE_SESSION_HTTPONLY="true"
ENV COOKIE_SESSION_SAMESITE="lax"
ENV JWT_SECRET_KEY=""
ENV JWT_ALGORITHM="HS256"
ENV JWT_ACCESS_TOKEN_EXPIRE_MINUTES="30"
ENV LOG_LEVEL="INFO"
ENV LOG_FILE=""

EXPOSE 6303

ENTRYPOINT ["/opt/demanou/bin/entrypoint.sh"]
