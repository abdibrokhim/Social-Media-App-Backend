# Social Media App Service

## NOTE:
If it gives following error: `{"app": "SOCIAL_MEDIA_SERVICE", "event": "Exception on /api/posts/all [GET]", "exc_info": ["<class' RecursionError'>", "RecursionError('maximum recursion depth exceeded')", "<traceback object at 0x103e5de00>"], "level": "error", "timestamp": "2023-12-08 20:38:57"}`. Don't worry, it's because of the decorator `@jwt_required`. I will fix it later. If you want to test any of the API endpoints, just comment out the decorator.

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
# Gunicorn does not support windows consider using WSL 
# Windows
#.venv\Scripts\activate.bat
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
gunicorn --logger-class=config.logger.GunicornLogger service.wsgi:app --bind 0.0.0.0:9000 --workers=1
```

### Or run with bash script
    
```bash
bash run.sh
```

[<img src="https://run.pstmn.io/button.svg" alt="Run In Postman" style="width: 128px; height: 32px;">](https://app.getpostman.com/run-collection/21700421-95f6512d-c7d1-4b8c-9120-6feee078eb4d?action=collection%2Ffork&source=rip_markdown&collection-url=entityId%3D21700421-95f6512d-c7d1-4b8c-9120-6feee078eb4d%26entityType%3Dcollection%26workspaceId%3D457ca1df-a10f-43da-a319-d4f63f5bd818)


`I will leave/push database as it is, so you can test it with some data.`

**Important:** `Do not modify or modify and push the changes to another branch, if you are not sure what you did.`


### How to push to new branch

```bash
git checkout -b <branch-name>
git add .
git commit -m "your commit message"
git push origin <branch-name>
```