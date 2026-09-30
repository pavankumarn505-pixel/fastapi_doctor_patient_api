# Doctor and Patient Management API

A simple REST API built using FastAPI to manage Doctors and Patients.

## Tech Stack

- Python 3.9+
- FastAPI
- Pydantic
- Uvicorn
- In-memory storage

## Features

### Doctor APIs

- `POST /doctors` - Create a doctor
- `GET /doctors` - Get all doctors
- `GET /doctors/{doctor_id}` - Get a doctor by ID

### Patient APIs

- `POST /patients` - Create a patient
- `GET /patients` - Get all patients

## Validation

- Doctor email must be valid.
- Patient age must be greater than 0.
- Pydantic models are used for request validation.
- `HTTPException` is used for proper error handling.
- Doctor `is_active` defaults to `true`.

## Project Structure

```text
fastapi_doctor_patient_api/
│
├── main.py
├── requirements.txt
└── README.md