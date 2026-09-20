
# REST API Development - Employee Management API

## Overview

This project is a RESTful API developed using FastAPI and SQLite.

The API provides CRUD operations for managing employee records.

## Technologies Used

- Python
- FastAPI
- SQLite
- SQLAlchemy
- Pydantic
- Uvicorn
- Requests
- Jupyter Notebook

## Features

- RESTful API
- CRUD operations
- SQLite database integration
- Input validation
- Error handling
- JSON responses
- Swagger API documentation
- ReDoc API documentation

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | / | API health check |
| POST | /employees | Create employee |
| GET | /employees | Get all employees |
| GET | /employees/{id} | Get employee by ID |
| PUT | /employees/{id} | Update employee |
| DELETE | /employees/{id} | Delete employee |

## Employee Data Model

| Field | Type | Description |
|-------|------|-------------|
| id | Integer | Unique employee ID |
| name | String | Employee name |
| email | String | Employee email |
| age | Integer | Employee age |
| department | String | Employee department |
| salary | Float | Employee salary |

## Validation

The API validates:

- Required fields
- Name length
- Email length
- Age between 18 and 65
- Positive salary
- Duplicate email addresses

## Error Handling

The API handles:

- Employee not found
- Duplicate email
- Invalid input
- Invalid data types
- Server errors

## Installation

Install the required packages:

    pip install -r requirements.txt

## Run the API

Run:

    uvicorn main:app --reload

The API will be available at:

    http://127.0.0.1:8000

## API Documentation

Swagger UI:

    http://127.0.0.1:8000/docs

ReDoc:

    http://127.0.0.1:8000/redoc

## Example POST Request

    {
        "name": "Rahul",
        "email": "rahul@example.com",
        "age": 22,
        "department": "IT",
        "salary": 45000
    }

## Example Response

    {
        "id": 1,
        "name": "Rahul",
        "email": "rahul@example.com",
        "age": 22,
        "department": "IT",
        "salary": 45000
    }

## Database

This project uses SQLite.

Database file:

    employees.db

## Author

Internship Task 3 - REST API Development
