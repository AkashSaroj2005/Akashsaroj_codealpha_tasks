# MiniSocial — Mini Social Media App

A responsive mini social network built with **HTML, CSS, JavaScript, Django, and SQLite**.

## Features

- User sign up, log in, and log out
- User profile with bio and optional avatar URL
- Create text posts
- Comment on posts
- Like/unlike posts (one like per user per post)
- Follow/unfollow users
- Feed, following-only feed, explore people, and search for users/posts
- Django admin for database management
- Responsive layout for desktop and mobile
- CSRF protection on form submissions

## Project structure

```text
minisocial_project/
├── manage.py
├── requirements.txt
├── minisocial/          # Django settings and project URLs
├── social/              # Models, forms, views, routes, admin
├── templates/
│   ├── base.html
│   ├── registration/
│   └── social/
└── static/
    ├── css/styles.css
    └── js/app.js
```

## Run locally

Requires Python 3.10+.

### 1. Create and activate a virtual environment

**Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Create the database tables

```bash
python manage.py migrate
```

### 4. Create an admin account (optional)

```bash
python manage.py createsuperuser
```

### 5. Start the development server

```bash
python manage.py runserver
```

Open http://127.0.0.1:8000 in your browser. Admin is at http://127.0.0.1:8000/admin/.

## Database design

- `auth_user` — Django's built-in user table
- `social_profile` — one-to-one profile bio/avatar URL
- `social_post` — post body, author, creation time
- `social_comment` — comment, post, author, creation time
- `social_like` — user/post relationship with a unique constraint
- `social_follow` — follower/following relationship with unique constraint and self-follow prevention

## Important notes

- This is a learning/demo project. `DEBUG=True` and the development secret key are only for local development. Before deployment, set `DEBUG=False`, configure a secure secret key and `ALLOWED_HOSTS`, serve static files appropriately, and use HTTPS.
- Avatar images are optional external URLs; this project does not upload image files.
- The app currently uses standard Django form submissions, so like/follow/comment actions reload the page rather than using an API/AJAX.
- For production, add email verification, password reset, pagination, rate limiting, automated tests, moderation/reporting, and secure deployment configuration.
