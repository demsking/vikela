# Vikela: Authentication Service with Proxy Middleware Integration

Vikela sets up a robust authentication system to secure backend services using
an authentication provider and various proxy middleware solutions such as
Traefik, Nginx, and others.

The authentication service ensures that all incoming
requests to protected services are authenticated before being forwarded. It
verifies user credentials, injects proxy headers upon successful authentication,
and redirects unauthorized users. This architecture enhances security and
provides a scalable solution for managing access to your applications.

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

## Table of Contents

- [How to Use](#how-to-use)
  * [Step 1: Configure the Proxy Middleware](#step-1-configure-the-proxy-middleware)
  * [Step 2: Running the Services](#step-2-running-the-services)
- [Contribute](#contribute)
- [Versioning](#versioning)
- [License](#license)

## How to Use

### Step 1: Configure the Proxy Middleware

**Using Traefik:**

1. **Docker-Compose Configuration**

   Create a `docker compose.yml`:

   ```yaml
   version: '3.8'

   services:
     traefik:
       image: traefik:v3.0
       depends_on:
         - vikela
       command:
         - "--api.insecure=true"
         - "--providers.docker=true"
         - "--entrypoints.web.address=:80"
       ports:
         - "80:80"
       volumes:
         - "/var/run/docker.sock:/var/run/docker.sock"
       networks:
         - cloud-public
       labels:
         - "traefik.enable=true"
         - "traefik.docker.network=cloud-public"
         - "traefik.http.routers.traefik.rule=Host(`traefik.${DOMAIN?Variable not set}`) && (PathPrefix(`/api`) || PathPrefix(`/dashboard`))"
         - "traefik.http.routers.traefik.service=api@internal"
         - "traefik.http.routers.traefik.tls=true"
         - "traefik.http.routers.traefik.tls.options=default"
         - "traefik.http.routers.traefik.middlewares=vikela"
         - "traefik.http.services.traefik.loadbalancer.server.port=8000"

     vikela:
       image: demsking/vikela
       networks:
         - cloud-public
       labels:
         - "traefik.enable=true"
         - "traefik.http.routers.vikela.service=vikela"
         - "traefik.http.routers.vikela.rule=Host(`vikela.example.com`)"
         - "traefik.http.routers.vikela.entryPoints=web"
         - "traefik.http.middlewares.vikela.forwardAuth.address=http://vikela:6303/api/verify?rd=https://vikela.example.com"
         - "traefik.http.middlewares.vikela.forwardAuth.trustForwardHeader=true"
         - "traefik.http.middlewares.vikela.forwardAuth.authResponseHeaders=Remote-User,Remote-Groups,Remote-Name,Remote-Email"
         - "traefik.http.services.vikela.loadbalancer.server.port=6303"

     whoami:
       image: traefik/whoami
       networks:
         - cloud-public
       labels:
         - "traefik.enable=true"
         - "traefik.http.routers.whoami.service=whoami"
         - "traefik.http.routers.whoami.rule=Host(`whoami.example.com`)"
         - "traefik.http.routers.whoami.entryPoints=web"
         - "traefik.http.routers.whoami.middlewares=vikela@docker"
         - "traefik.http.services.whoami.loadbalancer.server.port=80"

   networks:
     cloud-public:
   ```

**Using Nginx:**

1. **Nginx Configuration**

   Create an Nginx configuration file `nginx.conf`:

   ```nginx
   events {}

   http {
       server {
           listen 80;

           location /auth {
               proxy_pass http://vikela:6303/api/verify?rd=https://auth.example.com;
               proxy_set_header Host $host;
               proxy_set_header X-Real-IP $remote_addr;
               proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
               proxy_set_header X-Forwarded-Proto $scheme;
           }

           location / {
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

               proxy_pass http://backend_service:80;
           }
       }
   }
   ```

2. **Docker-Compose Configuration**

   Create a `compose.yaml` for Nginx:

   ```yaml
   version: '3.8'

   services:
     nginx:
       image: nginx:latest
       volumes:
         - ./nginx.conf:/etc/nginx/nginx.conf
       ports:
         - "80:80"
       networks:
         - cloud-public

     vikela:
       image: demsking/vikela
       networks:
         - cloud-public

     whoami:
       image: traefik/whoami
       networks:
         - cloud-public

   networks:
     cloud-public:
   ```

### Step 2: Running the Services

1. **Build and run the services**

   ```sh
   docker compose up -d
   ```

2. **Access your backend service through the proxy**

   - For Traefik: Visit `http://whoami.example.com`
   - For Nginx: Visit the domain or IP where Nginx is hosted

The proxy middleware will forward requests to the authentication service first.
If authenticated, it will inject proxy headers before forwarding the request to
the backend service. Adjust the configurations to fit your specific requirements
and environment.

## Contribute

Please follow [CONTRIBUTING.md](https://gitlab.com/demsking/vikela/blob/main/CONTRIBUTING.md).

## Versioning

Given a version number `MAJOR.MINOR.PATCH`, increment the:

- `MAJOR` version when you make incompatible API changes,
- `MINOR` version when you add functionality in a backwards-compatible manner,
  and
- `PATCH` version when you make backwards-compatible bug fixes.

Additional labels for pre-release and build metadata are available as extensions
to the `MAJOR.MINOR.PATCH` format.

See [SemVer.org](https://semver.org/) for more details.

## License

Licensed under the Apache License, Version 2.0 (the "License"); you may not use
this file except in compliance with the License.
You may obtain a copy of the License at [LICENSE](https://gitlab.com/demsking/vikela/blob/main/LICENSE).
