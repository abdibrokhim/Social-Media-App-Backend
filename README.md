# Social Media App Backend

## Title 

WeShot

## Description

Welcome to WeShot, the ultimate social media haven where your moments aren't just shared, they're celebrated. Inspired by the visual storytelling of Pinterest, the vibrant community of Instagram, and the personalized experience of Spotify, WeShot is where life's snapshots become part of a larger, more colorful tapestry.

Capture & Share: At the heart of WeShot is the simple yet powerful idea of capturing life as it happens. From the spontaneous to the spectacular, share your world, one moment at a time.

Explore & Discover: Dive into a sea of stories. With WeShot, every scroll is a journey through diverse experiences, emotions, and adventures. Discover content that resonates with your tastes, interests, and moods.

Personalized For You: Like Spotify's playlists tailored to your musical taste, WeShot curates a visual feed that evolves with your preferences. The more you explore, the more it becomes a reflection of you.

Powered by GPT4Vision: WeShot harnesses the cutting-edge capabilities of GPT4 Vision to elevate your storytelling. 

## Getting Started

### Dependencies

* Python
* Flask


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


**Note:** `I will leave/push database as it is, so you can test it with some data.`

### How to push commits to new branch

```bash
git checkout -b <branch-name>
git add .
git commit -m "your commit message"
git push origin <branch-name>
```