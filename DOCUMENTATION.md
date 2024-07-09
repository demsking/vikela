Vikela sets up a robust authentication system to secure backend services using
an authentication provider and various proxy middleware solutions such as
Traefik, Nginx, and others.

The authentication service ensures that all incoming requests to protected
services are authenticated before being forwarded. It verifies user credentials,
injects proxy headers upon successful authentication, and redirects unauthorized
users. This architecture enhances security and provides a scalable solution for
managing access to your applications.

**Key Features:**

- **Dedicated Authentication Service**: Handles user authentication and injects
  proxy headers upon successful login.
- **Proxy Middleware Integration**: Compatible with various proxy middleware
  solutions (e.g., Traefik, Nginx) to route requests through the authentication
  service.
- **Header Injection**: Automatically exposes `Remote-User`, `Remote-Groups`,
  `Remote-Name`, `Remote-Email` in headers, configurable with
  `authResponseHeaders`.
- **Docker-Compose Setup**: Provides an easy-to-deploy environment using Docker
  and Docker Compose.
- **TLS Support**: Ensures secure connections with TLS certificates managed by
  the proxy middleware.

**Meaning of Vikela**

**Vikela** means "project" or "guard" in Zulu, reflecting the core purpose of
the service: to guard and protect your applications by ensuring that only
authenticated users can access them.

## Backend Setup

Vikela uses CouchDB as its database backend, configured with a specific setup
enabling Proxy Authentication. This ensures secure access to the database and
helps maintain data integrity.

To enable Proxy Authentication on the CouchDB configuration, follow the
instructions provided in the CouchDB documentation at
https://docs.couchdb.org/en/latest/api/server/authn.html#api-auth-proxy.

### Generate Authentication Token

To generate the authentication token required for accessing CouchDB, you can
use the following command:

```sh
echo -n $COUCHDB_USER | openssl dgst -sha256 -hmac $COUCHDB_SECRET
```

This command uses OpenSSL to calculate the HMAC (Hash-based Message
Authentication Code) using SHA-256 hashing algorithm. It takes the CouchDB
user (`COUCHDB_USER`) as input and uses the CouchDB secret
(`COUCHDB_SECRET`) as the secret key. Replace `COUCHDB_USER` and
`COUCHDB_SECRET` with your actual database name and secret respectively.

## Deployment

Use the official Docker image [`demsking/vikela`](https://hub.docker.com/r/demsking/vikela)
to run Vikela:

```sh
docker run -d --env-file <path_to_env_file> -p 6303:6303 demsking/vikela
```

Replace `<path_to_env_file>` with the path to your environment variable file
containing the necessary configurations.

**Vikela API**

Open the documentation URL to access the API documentation. In your web browser,
navigate to [http://localhost:6303/docs](http://localhost:6303/docs).

### Configuration Variables

Below are the configuration variables used by the application, loaded from
environment variables:

| Variable Name                      | Description                                                                                | Default Value                 |
|------------------------------------|--------------------------------------------------------------------------------------------|-------------------------------|
| `TZ`                               | Time zone for the application.                                                             | `Africa/Douala`               |
| `WORKER`                           | Number of workers for the application.                                                     | `multiprocessing.cpu_count()` |
| `ROOT_PATH`                        | Root path for the API.                                                                     | `/api`                        |
| `CLIENT_USERAGENT`                 | User-agent string used for client requests.                                                | `vikela/{version}`            |
| `COUCHDB_URL`                      | URL for the CouchDB instance.                                                              |                               |
| `COUCHDB_AUTH_ROLES`               | Roles required for CouchDB authentication.                                                 | `_admin`                      |
| `COUCHDB_AUTH_USERNAME`            | Username for CouchDB authentication.                                                       |                               |
| `COUCHDB_AUTH_TOKEN`               | Authentication token for CouchDB.                                                          |                               |
| `DEFAULT_USER_GROUPS`              | Default groups assigned to users.                                                          | `user`                        |
| `COOKIE_SESSION_NAME`              | Name of the session cookie.                                                                | `vikela-session`              |
| `COOKIE_SESSION_MAX_AGE`           | Maximum age of the session cookie in seconds.                                              | `None`                        |
| `COOKIE_SESSION_EXPIRES`           | Expiry time of the session cookie in seconds.                                              | `None`                        |
| `COOKIE_SESSION_PATH`              | Path for which the session cookie is valid.                                                | `/`                           |
| `COOKIE_SESSION_DOMAIN`            | Domain for which the session cookie is valid.                                              |                               |
| `COOKIE_SESSION_SECURE`            | Flag indicating if the session cookie should only be sent over HTTPS.                      | `False`                       |
| `COOKIE_SESSION_HTTPONLY`          | Flag indicating if the session cookie should be accessible only through HTTP(S) requests.  | `True`                        |
| `COOKIE_SESSION_SAMESITE`          | SameSite attribute for the session cookie.                                                 | `lax`                         |
| `JWT_SECRET_KEY`                   | Secret key used for JWT token signing and verification.                                    |                               |
| `JWT_ALGORITHM`                    | Algorithm used for JWT signing.                                                            | `HS256`                       |
| `JWT_ACCESS_TOKEN_EXPIRE_MINUTES`  | Expiry duration for JWT access tokens in minutes.                                          | `30`                          |
| `LOG_LEVEL`                        | Logging level for the application.                                                         | `INFO`                        |
| `LOG_FILE`                         | File path for logging output.                                                              |                               |

### Step 1: Configure the Proxy Middleware

**Using Traefik:**

1. **Docker-Compose Configuration**

   Create a `compose.yaml` file:

   ```yaml
   ---
   services:
     traefik:
       image: traefik:v3.0
       depends_on:
         - vikela
       command:
         - "--api.insecure=true"
         - "--accesslog=true"
         - "--providers.docker=true"
         - "--providers.docker.network=cloud-public"
         - "--providers.docker.exposedByDefault=false"
         - "--entrypoints.web.address=:80"
       ports:
         - "80:80"
       volumes:
         - "/var/run/docker.sock:/var/run/docker.sock"

     vikela:
       image: demsking/vikela
       labels:
         - "traefik.enable=true"
         - "traefik.http.routers.vikela.service=vikela"
         - "traefik.http.routers.vikela.rule=Host(`auth.example.com`)"
         - "traefik.http.routers.vikela.entryPoints=web"
         - "traefik.http.middlewares.vikela.forwardAuth.address=http://vikela:6303/api/verify?rd=http://auth.example.com"
         - "traefik.http.middlewares.vikela.forwardAuth.trustForwardHeader=true"
         - "traefik.http.middlewares.vikela.forwardAuth.authResponseHeaders=Remote-User,Remote-Groups,Remote-Name,Remote-Email"
         - "traefik.http.services.vikela.loadbalancer.server.port=6303"

     couchdb:
       image: couchdb:3.3.3
       environment:
         COUCHDB_USER: ${COUCHDB_USER?Variable not set}
         COUCHDB_PASSWORD: ${COUCHDB_PASSWORD?Variable not set}
         COUCHDB_SECRET: ${COUCHDB_SECRET?Variable not set}

     public-service:
       image: traefik/whoami
       labels:
         - "traefik.enable=true"
         - "traefik.http.routers.public-whoami.service=public-whoami"
         - "traefik.http.routers.public-whoami.rule=PathPrefix(`/public`)"
         - "traefik.http.routers.public-whoami.entryPoints=web"
         - "traefik.http.services.public-whoami.loadbalancer.server.port=80"

     protected-service:
       image: traefik/whoami
       labels:
         - "traefik.enable=true"
         - "traefik.http.routers.protected-whoami.service=protected-whoami"
         - "traefik.http.routers.protected-whoami.rule=PathPrefix(`/protected`)"
         - "traefik.http.routers.protected-whoami.entryPoints=web"
         - "traefik.http.routers.protected-whoami.middlewares=vikela@docker"
         - "traefik.http.services.protected-whoami.loadbalancer.server.port=80"
   ```

**Using Nginx:**

1. **Nginx Configuration**

   Create an Nginx configuration file `nginx.conf`:

   ```nginx
   http {
       server {
           listen 80;

           location /auth {
               proxy_pass http://vikela:6303/api/verify?rd=https://auth.example.com;
               proxy_set_header Host $host;
               proxy_set_header X-Real-IP $remote_addr;

               # Add the following lines to set X-Forwarded-Proto,
               # X-Forwarded-Host, X-Forwarded-Method, and X-Forwarded-URI headers
               proxy_set_header X-Forwarded-Proto $scheme;
               proxy_set_header X-Forwarded-Host $host;
               proxy_set_header X-Forwarded-Method $request_method;
               proxy_set_header X-Forwarded-URI $request_uri;
           }

           location /public {
               auth_request /auth;

               proxy_pass http://public-service:80;
           }

           location /protected {
               auth_request /auth;

               # Pass the headers from the auth request to the backend service
               auth_request_set $user $upstream_http_x_remote_user;
               auth_request_set $email $upstream_http_x_remote_email;
               auth_request_set $groups $upstream_http_x_remote_groups;
               auth_request_set $name $upstream_http_x_remote_name;

               proxy_set_header X-Remote-User $user;
               proxy_set_header X-Remote-Email $email;
               proxy_set_header X-Remote-Groups $groups;
               proxy_set_header X-Remote-Name $name;

               proxy_pass http://protected-service:80;
           }
       }
   }
   ```

2. **Docker-Compose Configuration**

   Create a `compose.yaml` for Nginx:

   ```yaml
   ---
   services:
     nginx:
       image: nginx:latest
       volumes:
         - ./nginx.conf:/etc/nginx/nginx.conf
       ports:
         - "80:80"

     vikela:
       image: demsking/vikela

     couchdb:
       image: couchdb:3.3.3
       environment:
         COUCHDB_USER: ${COUCHDB_USER?Variable not set}
         COUCHDB_PASSWORD: ${COUCHDB_PASSWORD?Variable not set}
         COUCHDB_SECRET: ${COUCHDB_SECRET?Variable not set}

     public-service:
       image: traefik/whoami

     protected-service:
       image: traefik/whoami
   ```

### Step 2: Running the Services

1. **Build and run the services**

   ```sh
   docker compose up -d
   ```

2. **Access your backend service through the proxy**

   Visit `http://localhost/public` and then `http://localhost/protected`

The proxy middleware will forward requests to the authentication service first.
If authenticated, it will inject proxy headers before forwarding the request to
the backend service. Adjust the configurations to fit your specific requirements
and environment.

## Running Behind a TLS Termination Proxy

If you need to run Vikela behind a TLS termination proxy (such as Nginx or
Traefik), you must inform Vikela to trust the headers sent by the proxy that
indicate the application is running behind HTTPS. This is done by using the
`--proxy-headers` option:

```sh
docker run -d -p 6303:6303 demsking/vikela --proxy-headers
```

By adding the `--proxy-headers` option, Vikela will correctly interpret
the proxy headers indicating that it is operating behind an HTTPS proxy. This
ensures that the application behaves as expected in a secure environment.
