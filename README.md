# Notes and tasks

The project is a backend for a system for taking notes and tasks. It provides a RESTful API through which users can create, view, update and delete notes and tasks. Also users can authenticate to access their personal notes and tasks.

## Setting environment variables

In the src folder we find the file  `.env` and fill it in according to the template:

    HOST=db # The host of your database (locally localhost, and db in docker)
    POSTGRES_DB=postgres # Name of your database
    POSTGRES_USER=postgres # Password of your database
    POSTGRES_PASSWORD=postgres # Username from your database
    PORT=5432 # Database port


    POSTGRES_DB_TEST=pytest_fastapi # Name for test database
    TEST_DB_URL=postgresql+asyncpg://postgres:postgres@db:5432/pytest_fastapi # Url for test database
    DB_URL=postgresql+asyncpg://postgres:postgres@db:5432/postgres # Url of the main database

    REDIS_HOST=redis # The host of your redis database (locally localhost, and redis in docker)
    REDIS_PORT=6379 # Redis port

    SECRET=lkrngrngeroi3985thw589h432o87gbrugir # The secret key for JWT, you need to come up with a random line

    SMTP_HOST=smtp.gmail.com # The host of your smtp client
    SMTP_PORT=465  # The port of your smtp client

    SMTP_USER=example@gmail.com # Your mail for sending emails
    SMTP_PASSWORD=jkrdbglrbgriugb # Email password

    DNS=http://0.0.0.0:2000/ # Your server address

    CELERY_HOST=redis # Celery host for broker(locally localhost, and redis in docker)
    CELERY_PORT=6379/1 # Celery port

## Project launch

In the root of the project, run:

    docker compose up
