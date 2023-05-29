# APIs Client Gateway

Welcome to our cutting-edge application powered by FastAPI, Alembic, SQLAlchemy, and integrated with various Amazon Web Services (AWS) such as S3, SES, and SNS. 

This robust stack enables us to build a highly scalable and efficient web service while leveraging the power of AWS's cloud infrastructure. With the added security and authentication benefits of OAuth 2.0, we ensure that our users' data remains protected throughout their interactions with our application. 

Whether you're new to this technology stack or an experienced developer, this guide will walk you through the seamless integration of these tools, allowing you to build a secure and feature-rich web application in no time.

## Alembic Create Table or Update database

### Settings connection

insert your database to /backend-tiktok-clone-fastapi/alembic.ini

    line 61 : sqlalchemy.url = postgresql+psycopg2://DATABASE_USERNAME:password@DATABASE_SERVER:5432/DATABASE_NAME

### Create table
First Times - Create Table Version !!

    alembic revision -m "create account table"

Generate script python auto upgrade by core.model

    alembic revision --autogenerate -m "comment here!!"

Upgrade script python from autogen to databases.

    alembic upgrade head

### Update table

Your can edit all table here /backend-tiktok-clone-fastapi/app/core/db_model.py

After, update table.....
Generate script python auto upgrade by core.model

    alembic revision --autogenerate -m "comment here!!"

Upgrade script python from autogen to databases.

    alembic upgrade head

## To deploy local

    $ git clone https://github.com/tanakon8529/backend-tiktok-clone-fastapi.git
    $ cd /backend-tiktok-clone-fastapi
    $ pip install -r requirements.txt
    $ python main.py

## To deploy with docker-compose

  

To install/update this application.

Run (if you see running and check error!!)

    docker-compose build

and (if you see running and check error!!)

    docker-compose up

Or >>build and up in one line<< (If you don't see running and check error.)

    Run docker-compose up --build -d

To stop-application.

    docker-compose down

To uninstall this application.

    docker stack rm <stack name>
