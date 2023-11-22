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

[<img src="https://run.pstmn.io/button.svg" alt="Run In Postman" style="width: 128px; height: 32px;">](https://app.getpostman.com/run-collection/21700421-95f6512d-c7d1-4b8c-9120-6feee078eb4d?action=collection%2Ffork&source=rip_markdown&collection-url=entityId%3D21700421-95f6512d-c7d1-4b8c-9120-6feee078eb4d%26entityType%3Dcollection%26workspaceId%3D457ca1df-a10f-43da-a319-d4f63f5bd818)


`I will leave/push database as it is, so you can test it.`

**Important:** `Do not modify or modify and push the changes to another branch, if you are not sure what you did.`


### How to push to new branch

```bash
git checkout -b <branch-name>
git add .
git commit -m "your commit message"
git push origin <branch-name>
```