# Security Policy

## Supported Versions

| Version | Supported |
| ------- | --------- |
| 1.0.x   | ✅        |

## Reporting a Vulnerability

We take security seriously. If you discover a vulnerability, **please do not
open a public GitHub issue.**

Instead, email **aashish@marketdoctorsonline.com** with:

- A description of the vulnerability and its impact
- Steps to reproduce (proof-of-concept if possible)
- Any suggested remediation

You can expect an acknowledgement within **72 hours** and a status update within
**7 days**. Once a fix is released, we are happy to credit you (if you wish).

## Security Measures in This Project

CineBook applies defense-in-depth:

- **No raw SQL** — all database access goes through the SQLAlchemy ORM,
  eliminating SQL injection.
- **Password hashing** — passwords are stored as salted PBKDF2 hashes
  (Werkzeug), never in plaintext.
- **CSRF protection** — enabled globally via Flask-WTF on all state-changing
  forms.
- **Input validation** — every form field is validated server-side with WTForms.
- **Session hardening** — `HttpOnly`, `SameSite=Lax`, and `Secure` cookies in
  production.
- **Open-redirect protection** — the post-login `next` parameter is restricted
  to local URLs.
- **Secrets management** — all secrets are read from environment variables and
  never committed; production refuses to start with the default `SECRET_KEY`.
- **Authorization checks** — booking views are scoped to the current user
  (a user cannot read or cancel another user's bookings).

## Hardening Checklist for Deployments

- [ ] Set a strong, random `SECRET_KEY`.
- [ ] Set `FLASK_CONFIG=production` and `SESSION_COOKIE_SECURE=true`.
- [ ] Serve exclusively over HTTPS (TLS termination at proxy/load balancer).
- [ ] Use a managed database via `DATABASE_URL`, not the bundled SQLite file.
- [ ] Keep dependencies up to date (`pip list --outdated`).
