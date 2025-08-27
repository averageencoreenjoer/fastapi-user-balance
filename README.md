# FastAPI User Balance Service

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Pytest](https://img.shields.io/badge/Pytest-0A9B71?style=for-the-badge&logo=pytest&logoColor=white)

A simple REST API built with FastAPI to manage a list of users and their balances. This project demonstrates basic API development principles, including data validation, in-memory data storage, and automated testing.

## Features

- **Create User**: `POST /users` - Create a new user with a unique email and an initial balance.
- **Get Users**: `GET /users` - Retrieve a list of all existing users.
- **Transfer Funds**: `POST /transfer` - Transfer a specified amount from one user to another, with validation for sufficient funds.

## Tech Stack

- **Framework**: FastAPI
- **Data Validation**: Pydantic
- **Testing**: Pytest & HTTPX
- **ASGI Server**: Uvicorn

## Getting Started

Follow these instructions to get a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3.8+

### Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/YOUR_USERNAME/fastapi-user-balance.git
    cd fastapi-user-balance
    ```

2.  **Create and activate a virtual environment:**
    - On macOS/Linux:
      ```bash
      python3 -m venv venv
      source venv/bin/activate
      ```
    - On Windows:
      ```bash
      python -m venv venv
      .\venv\Scripts\Activate
      ```

3.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### Running the Application

1.  **Start the development server:**
    ```bash
    uvicorn main:app --reload
    ```
    The API will be running at `http://127.0.0.1:8000`.

2.  **Access the interactive API documentation:**
    Open your browser and navigate to `http://127.0.0.1:8000/docs`. You will find a Swagger UI where you can interact with all the API endpoints.

### Running Tests

To ensure the application is working correctly, you can run the automated tests.

1.  **Execute the test suite:**
    ```bash
    pytest -v
    ```
    All tests should pass, confirming that the API endpoints and logic behave as expected.