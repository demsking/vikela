# Vikela: Authentication Service with Proxy Middleware Integration

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

## Vikela Documentation

Open the documentation URL to access the API documentation. In your web browser,
navigate to [https://demsking.gitlab.io/vikela](https://demsking.gitlab.io/vikela).

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
