Vikela sets up a robust authentication system to secure backend services using
an authentication provider and various proxy middleware solutions such as
Traefik, Nginx, and others.

The authentication service ensures that all incoming
requests to protected services are authenticated before being forwarded. It
verifies user credentials, injects proxy headers upon successful authentication,
and redirects unauthorized users. This architecture enhances security and
provides a scalable solution for managing access to your applications.

## Configuration Variables

Below are the configuration variables used by the application, loaded from environment variables:

| Variable Name                      | Description                                                                                | Default Value                 |
|------------------------------------|--------------------------------------------------------------------------------------------|-------------------------------|
| `WORKER`                           | Number of workers for the application.                                                     | `multiprocessing.cpu_count()` |
| `ROOT_PATH`                        | Root path for the API.                                                                     | `/api`                        |
| `CLIENT_USERAGENT`                 | User-agent string used for client requests.                                                | `{APP_NAME}/{APP_VERSION}`    |
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
