# Best Cars Dealership

## Project Name: Best Cars Dealership Platform

Full-stack web application built with **Django** (backend) and vanilla **HTML/JS** (frontend) that allows users to browse car dealerships, read and post reviews with sentiment analysis.

## Tech Stack
- **Backend**: Django 4.2 + SQLite
- **Frontend**: HTML5, Bootstrap 5, vanilla JavaScript
- **Deployment**: Render.com
- **CI/CD**: GitHub Actions

## Features
- Browse all car dealerships nationwide
- Filter dealerships by US state
- View dealer details and customer reviews
- Post reviews with automatic sentiment analysis (positive/negative/neutral)
- User authentication (Register, Login, Logout)
- Django Admin panel

## Team
- **Alex Johnson** — Full Stack Developer | alex.johnson@bestcars.com
- **Maria Garcia** — Backend Engineer | maria.garcia@bestcars.com
- **James Smith** — Frontend Developer | james.smith@bestcars.com

## Setup

```bash
cd server
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open http://127.0.0.1:8000

## API Endpoints

| Method | URL | Description |
|--------|-----|-------------|
| GET | /djangoapp/get_dealers | All dealers |
| GET | /djangoapp/get_dealers/Kansas | Dealers by state |
| GET | /djangoapp/dealer/1 | Dealer by ID |
| GET | /djangoapp/reviews/dealer/1 | Reviews for dealer |
| POST | /djangoapp/add_review | Add review |
| GET | /djangoapp/get_cars | All car makes & models |
| POST | /djangoapp/login | Login |
| GET | /djangoapp/logout | Logout |
| POST | /djangoapp/register | Register |
| GET | /djangoapp/analyze_review?text=... | Sentiment analysis |

## Deployment (Render)

1. Push to GitHub
2. New Web Service on render.com → connect repo
3. Build Command: `bash build.sh`
4. Start Command: `cd server && gunicorn djangoproj.wsgi`
5. Add env var: `SECRET_KEY=your-secret-key`

## Author : MASSOLOKONON Tadagbe Landry
## Licence MIT
