# Workout API

A headless REST API built with FastAPI and Domain-Driven Design (DDD), designed to manage workout routines and sessions. 

## Tech Stack
* Python 3.12
* FastAPI & Uvicorn
* Pydantic
* Pytest (81% Coverage)
* Docker

## Architecture
This project follows an Aggregate-Based Layered Architecture to strictly isolate Domain logic from Infrastructure concerns. 
* **Domain Layer:** Pure Python models protecting business invariants.
* **Service Layer:** Application use-cases and orchestration.
* **Infrastructure Layer:** FastAPI routers and Repository implementations.

## How to Run Locally (Docker)
1. Clone the repository.
2. Build the image: `docker build -t workout-api .`
3. Run the container: `docker run -p 8000:8000 workout-api`
4. Access the API documentation at `http://localhost:8000/docs`