#
## Stage 1: Build environment
FROM python:3.11-alpine3.19 AS build-env

ENV PATH="/root/.local/bin:$PATH"
ENV POETRY_HOME='/usr/local'
ENV POETRY_VIRTUALENVS_CREATE=false

# Set the shell to /bin/ash and enable pipefail
SHELL ["/bin/ash", "-eo", "pipefail", "-c"]

# Install build dependencies
RUN apk update \
  && apk add --no-cache \
    curl=8.5.0-r0 \
    build-base=0.5-r3 \
    python3-dev=3.11.9-r0 \
    libffi-dev=3.4.4-r3 \
  && curl -sSL https://install.python-poetry.org | python3 -

WORKDIR /src
COPY poetry.lock pyproject.toml ./
RUN poetry install --no-root --no-interaction --no-ansi --only=main


#
## Stage 2: Runtime environment
FROM python:3.11-alpine3.19

# Create a non-root user and group
RUN addgroup -S olumulo && adduser -S olumulo -G olumulo

# Copy built Python dependencies from the build-env stage
COPY --from=build-env /usr/local/lib/python3.11/site-packages/ /usr/local/lib/python3.11/site-packages/
COPY --from=build-env /usr/local/bin/ /usr/local/bin/

# Binaries
COPY bin/* /opt/demanou/bin/
RUN chmod +x /opt/demanou/bin/*

# Copy application files
COPY pyproject.toml LICENSE DOCUMENTATION.md /opt/demanou/
COPY vikela/ /opt/demanou/vikela
COPY vikela_core/ /opt/demanou/vikela_core
COPY vikela_models/ /opt/demanou/vikela_models

USER olumulo

ENV PATH="/opt/demanou/bin:/usr/local/bin:$PATH"
ENV PYTHONPATH="/opt/demanou:/usr/local/lib/python3.11/site-packages"
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
