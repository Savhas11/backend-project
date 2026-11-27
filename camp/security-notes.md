1. Password storage proof



Goal: Prove passwords are stored as one-way hashes, not plaintext.



Python shell check:

Python
from camp import create_app
from camp.extensions import db
from camp.models import User

app = create_app()
app.app_context().push()

user = User.query.first()
print("Email:", user.email)
print("Password hash:", user.password_hash)
Sample output (redacted):

Text
Email: updated1@example.com
Password hash: scrypt:32768:8:1$...$...
Conclusion: password_hash uses a one-way scrypt hash, plaintext password is never stored.

2. Login behavior: correct vs incorrect password



Goal: Prove correct password succeeds and incorrect password fails.



Correct password (redacted in this file):

Bash
curl -i -X POST http://127.0.0.1:5001/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "updated1@example.com",
    "password": "***REDACTED***"
  }'
Sample response:

Text
HTTP/1.1 200 OK
Content-Type: application/json
...

{"token":"<JWT_TOKEN_REDACTED>"}
Incorrect password (intentionally wrong):

Bash
curl -i -X POST http://127.0.0.1:5001/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "updated1@example.com",
    "password": "***wrong-pass**"
  }'
Sample response:

Text
HTTP/1.1 401 UNAUTHORIZED
Content-Type: application/json
...

{"error":"Invalid credentials"}
Conclusion: app issues JWT only for the correct password; incorrect passwords are rejected with 401.