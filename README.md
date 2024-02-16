

# Backend TikTok Clone - FastAPI

## Introduction

Welcome to the Backend TikTok Clone project, a cutting-edge application utilizing FastAPI, Alembic, SQLAlchemy, and AWS services including S3, SES, and SNS. This stack ensures scalability, efficiency, and security, leveraging OAuth 2.0 for authentication and AWS's robust cloud infrastructure.

## Features

- **FastAPI Framework:** For efficient and easy-to-write backend code.
- **Database Migrations with Alembic:** Ensures database versioning is seamless.
- **SQLAlchemy ORM:** For database interactions using Python objects.
- **AWS Integration:** Utilizing S3 for storage, SES for email, and SNS for notifications.
- **OAuth 2.0 Security:** To protect users' data with modern authentication standards.

## Getting Started

### Prerequisites

- Git
- Docker & Docker-Compose (for Docker deployment)
- Python 3.8 or newer

### Database Setup

#### Configuring Database Connection

1. Navigate to `alembic.ini` in the project directory.
2. Replace the placeholder values on line 61 with your database credentials:

    ```ini
    sqlalchemy.url = postgresql+psycopg2://DATABASE_USERNAME:password@DATABASE_SERVER:5432/DATABASE_NAME
    ```

#### Creating Tables

To set up your database tables for the first time, run:

```shell
alembic revision -m "create account table"
alembic revision --autogenerate -m "<description_of_changes>"
alembic upgrade head
```

### Updating Database Schema

To modify and update your database schema, edit the models in `app/core/db_model.py` and then apply the changes:

```shell
alembic revision --autogenerate -m "<description_of_changes>"
alembic upgrade head
```

## Deployment

### Local Deployment

To run the application locally:

```shell
git clone https://github.com/tanakon8529/backend-tiktok-clone-fastapi.git
cd backend-tiktok-clone-fastapi
pip install -r requirements.txt
python main.py
```

### Docker-Compose Deployment

#### Installation/Update

```shell
docker-compose build
docker-compose up -d
```

#### Stopping the Application

```shell
docker-compose down
```

#### Uninstallation

If you wish to remove the Docker stack:

```shell
docker stack rm <stack_name>
```
