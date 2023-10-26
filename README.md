# Social Media App Service

## Installation

### Clone the repository

```bash
git clone https://github.com/abdibrokhim/Social-Media-App-Backend
```

### Create a virtual environment

```bash
python3 -m venv .venv
```

### Activate the virtual environment

```bash
# Linux
source .venv/bin/activate

# Windows
.venv\Scripts\activate.bat
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Copy file .env.example to .env

```bash
cp .env.example .env
```

### Run the app

```bash
gunicorn --logger-class=config.logger.GunicornLogger service.wsgi:app --bind 0.0.0.0:8000 --workers=1
```

`I will leave database as it is, so you can test it.`

**Important:** `Do not modify or modify and not push the code if you not sure what you are doing.`