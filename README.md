[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)

# Env It!

Envit is a Python library and command-line interface (CLI) tool for securely encrypting and decrypting environment variable files.

## Features

- Encrypt environment variable files before storing them in a Git repository
- Decrypt encrypted environment variable files for local usage
- Generate Secret keys for encryption and decryption

## Installation
```bash
pip install envit
```

## Usage

Create a `envs` directory in root of you project. put your environment `.env` files there.
here is directory structure:
```bash
sample-project
├── envs
│   ├── development.env
│   ├── staging.env
│   └── production.env
├── main.py
├── README.md
└── requirements.txt
```

> Note: Make sure your `.env` files included in `.gitignore`
>    ```gitignore
>    envs/*.env
>    ```

*for example your `production.env` looks like this:*
```text
# DATABASE
DB_HOST=database
DB_NAME=mydb
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=strongpassword
.
.
.
```

**Generate an encryption key**

```bash
ev keygen
```
This will output a randomly generated encryption key.

**Encrypt Environment Variables**

```bash
ev encrypt -e <environment> -k <encryption_key>
```
This will create a file named `<envrionment>.env.enc` in `envs` directory

**Decrypt Environment Variables**

```bash
ev decrypt -e <environment> -k <encryption_key>
```
This will create or overwrite existing `<environment>.env` file in `envs` directory

**Finally, your project structure looks like this:**
```bash
sample-project
├── envs
│   ├── development.env
│   ├── development.env.enc
│   ├── staging.env
│   ├── staging.env.enc
│   └── production.env
│   └── production.env.enc
├── main.py
├── README.md
└── requirements.txt
```

After all you can decrypt your credentials in desired environment with having corresponding secret key.

## Coding
Export `ENVIRONMENT` as an os environment variable like this:
```bash
export ENVIRONMENT=<environment>
```
Now you can easily get your environment variables. we used [python-decouple](https://pypi.org/project/python-decouple/) inside.

```python
from envit.core import config
from decouple import CSV

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=CSV())
DB_HOST = config('DB_HOST', default='localhost')
DB_PORT = config('DB_PORT', cast=int, default=5432)
...
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
