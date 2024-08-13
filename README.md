# FastAPI Blog with SQLAlchemy

This repository contains a full-featured blogging application built with FastAPI, SQLAlchemy, and PostgreSQL. The application is designed to provide a foundation for a modern web application, including user authentication, CRUD operations for blog posts, and more.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [Running Tests](#running-tests)
- [Project Structure](#project-structure)
- [Environment Variables](#environment-variables)
- [License](#license)

## Features

- **User Authentication**: Secure user authentication with password hashing.
- **CRUD Operations**: Create, read, update, and delete posts and user profiles.
- **Dependency Injection**: Efficient dependency management using FastAPI's dependency injection system.
- **Asynchronous Support**: Leverages Python's `asyncio` for non-blocking I/O operations.
- **Database Integration**: Uses SQLAlchemy as the ORM and PostgreSQL as the database.
- **Testing**: Comprehensive test suite using `pytest`, including fixtures for setup and teardown.

## Installation

To get started with this project, follow the steps below:

### Prerequisites

- Python 3.9+
- PostgreSQL
- `virtualenv` (optional but recommended)

### Clone the Repository

```bash
git clone https://github.com/KiyoshiSama/fastapi-blog-sqlalchemy-v2.git
cd fastapi-blog-sqlalchemy-v2
```
### Create and Activate a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```
### Install Dependencies
```bash
pip install -r requirements.txt
```
### Running the Application
Before running the application, you need to set up the database and configure environment variables.

### Database Setup

1. Ensure PostgreSQL is running on your machine.
2. Create a new PostgreSQL database.

```bash
psql -U postgres
CREATE DATABASE fastapi_blog;
```
### Environment Variables
Create a ".env" file in the root directory of the project and add the following configuration. Adjust the values according to your setup:
```env
DATABASE_URL=postgresql+asyncpg://<username>:<password>@localhost:5432/fastapi_blog
SECRET_KEY=<your_secret_key>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```
### Run Database Migrations
```bash 
alembic upgrade head
```
### Run the Application
```bash
uvicorn app.main:app --reload
```
### Running Tests
This project uses "pytest" for testing. To run the tests, use the following command:
```bash
pytest
```
## Licence
This project is licensed under the MIT License. See the LICENSE file for more information.

