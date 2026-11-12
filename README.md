# Backend Project

Simple Flask backend project for my Maestro course.

## Setup

First, create a virtual environment for the project:

```bash
python3 -m venv .venv
```

Activate the virtual environment:

```bash
source .venv/bin/activate
```

Then install the required packages:

```bash
pip install -r requirements.txt
```

This installs everything needed to run the project.

## Environment Variables

This project uses environment variables to store settings needed for the app to run.

Before running the app:

1. Copy `.env.example` and rename the copy to `.env`.
2. Open `.env` and fill in your own values.
3. Keep your `.env` file private and don't upload it to GitHub.

The app uses these environment variables:

| Variable | Purpose | Example |
|---|---|---|
| `SECRET_KEY` | Used for Flask security. | `replace-with-your-own-secret` |
| `DATABASE_URL` | Tells the app which database to use. | `sqlite:///dev.db` |

Example `.env` file:

```env
SECRET_KEY=replace-with-your-own-secret
DATABASE_URL=sqlite:///dev.db
```

Make sure to use your own secret key instead of the example value.

## Database Migrations

After setting up the project and installing the requirements, run this command to create the database tables:

```bash
flask --app "camp:create_app()" db upgrade
```

You should run this when setting up the project for the first time and whenever new migrations have been added.

The migration files are already included in the project, so you don't need to create new ones just to get the database set up.