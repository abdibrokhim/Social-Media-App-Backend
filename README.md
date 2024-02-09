# WeShot Backend API

`Note:` Make sure you have already checked WeShot App [here](https://github.com/abdibrokhim/weshot). if you haven't, please check it first then come back here again.

## Getting Started

### Pre-requisites

* Python

## Installation

For detailed installation instructions, you can refer to the official documentation for each of the following tools:

* [Install Python](https://www.python.org/downloads/)

### Clone the repository

```bash
git clone https://github.com/abdibrokhim/Social-Media-App-Backend
```

### Go to the project directory
```
cd Social-Media-App-Backend
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

### Set environment variables

```bash
cp .env.example .env
```
`Note`: You need to set the environment variables in the `.env` file.

### Run the app

```bash
gunicorn --logger-class=config.logger.GunicornLogger service.wsgi:app --bind 0.0.0.0:9000 --workers=1
```

### Run with bash script
    
```bash
bash run.sh
```

### Postman Collection

You can test the API using the Postman collection below:

[<img src="https://run.pstmn.io/button.svg" alt="Run In Postman" style="width: 128px; height: 32px;">](https://app.getpostman.com/run-collection/21700421-95f6512d-c7d1-4b8c-9120-6feee078eb4d?action=collection%2Ffork&source=rip_markdown&collection-url=entityId%3D21700421-95f6512d-c7d1-4b8c-9120-6feee078eb4d%26entityType%3Dcollection%26workspaceId%3D457ca1df-a10f-43da-a319-d4f63f5bd818)


`Note:` I will leave database as it is, so you can test it with some data on it.

`Note:` After running the app if you see following message on you terminal:
```
{"app": "SOCIAL_MEDIA_SERVICE", "event": "Retrying in 1 second.", "level": "error", "timestamp": "2024-02-09 10:59:58"}
{"app": "SOCIAL_MEDIA_SERVICE", "event": "Can't connect to ('0.0.0.0', 9000)", "level": "error", "timestamp": "2024-02-09 10:59:59"}
```
please, just change the port number in the `run.sh` file to another port number, for example `8000`, and then run the app again it will work fine. Also, don't forget to change the port number in the `weshot` app in the `env.dart` file on [line 4](https://github.com/abdibrokhim/weshot/blob/54f538a7fee1d66fe10d7570ecddab3c53468767/lib/utils/env.dart#L4).
