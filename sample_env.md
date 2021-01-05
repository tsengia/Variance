# Sample .env File

When setting up Variance, a `.env` file is needed in the toplevel directory.
This `.env` file is not distributed with Variance because it contains purely user configuration details.
Below are the contents of a sample `.env` file and an explanation of each item.

```
LANG=C.UTF-8
LC_ALL=C.UTF-8
PROD_DATABASE_URI=sqlite+pysqlite:///instance/prod-variance.sqlite
DEV_DATABASE_URI=sqlite+pysqlite:///instance/dev-variance.sqlite
UNIT_TEST_DATABASE_URI=sqlite+pysqlite:///:memory:
SESSION_COOKIE_NAME=[RANDOM STRING]
SECRET_KEY=[RANDOM STRING]
```

Be sure to generate your `SESSION_COOKIE_NAME` and `SECRET_KEY` in a secure manner.
The `SECRET_KEY` is used to sign the JSON Web Tokens used by clients of the API.
