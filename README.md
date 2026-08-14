# Study Room Reservation System

A database-backed application for managing study rooms and reservations at a university.

The system allows students to view available study rooms, create reservations and review existing reservations. It also provides room usage statistics.

The application was developed as a term project for the module **Introduction to Database Management Systems** at Technische Hochschule Georg Agricola (THGA Bochum).

---

## Table of Contents

- [Overview](#overview)
- [Application Domain](#application-domain)
- [Architecture](#architecture)
- [Technologies](#technologies)
- [Project Structure](#project-structure)
- [Database](#database)
- [Data Model](#data-model)
- [REST API](#rest-api)
- [API Authentication](#api-authentication)
- [Frontend](#frontend)
- [Frontend Functions](#frontend-functions)
- [Reservation Conflict Handling](#reservation-conflict-handling)
- [Docker Compose](#docker-compose)
- [Configuration](#configuration)
- [Running the Backend](#running-the-backend)
- [Running the Frontend](#running-the-frontend)
- [Windows Executable](#windows-executable)
- [Deployment on the Lecture Server](#deployment-on-the-lecture-server)
- [Security](#security)
- [Testing](#testing)
- [Current Project Status](#current-project-status)

---

## Overview

The Study Room Reservation System is a small database-backed application for managing study rooms and their reservations.

The system consists of three main layers:

1. **PostgreSQL** as the relational database management system
2. **FastAPI** as the REST API between the frontend and the database
3. **Python/Tkinter** as the desktop frontend

The frontend never accesses PostgreSQL directly. All communication with the database takes place through the FastAPI REST API.

The API is protected using an `X-API-Key`.

---

## Application Domain

The application is designed for universities where students need to reserve study rooms for individual or group work.

The system addresses the problem of manually managing room reservations, which can lead to double bookings and scheduling conflicts.

Typical use cases include:

- viewing available study rooms
- checking room capacity
- creating a reservation
- viewing existing reservations
- checking how often rooms are used

A typical scenario is a student reserving a study room for a few hours to prepare for an exam.

---

## Architecture

The overall architecture follows the structure required for the DBMS term project.

```text
                    HTTP + X-API-Key
┌──────────────────────────────┐
│      Tkinter Frontend        │
│      Desktop Application     │
└──────────────┬───────────────┘
               │
               │ REST API
               ▼
┌──────────────────────────────┐
│          FastAPI             │
│          API Layer           │
└──────────────┬───────────────┘
               │
               │ SQL
               ▼
┌──────────────────────────────┐
│        PostgreSQL            │
│       Database Layer         │
└──────────────────────────────┘
```

For the final deployment, PostgreSQL and FastAPI run as Docker containers on the lecture server. The frontend is installed separately as a Debian package (`.deb`).

The backend is therefore containerised, while the frontend is not.

---

## Technologies

The project uses the following technologies:

| Technology | Purpose |
|---|---|
| Python | Programming language |
| Tkinter | Desktop GUI |
| FastAPI | REST API |
| PostgreSQL 16 | Relational database |
| psycopg2 | PostgreSQL connection from Python |
| Docker | Containerisation |
| Docker Compose | Backend orchestration |
| uv | Python dependency and environment management |
| PyInstaller | Building the desktop application |
| fpm | Creating the Debian package |
| GitHub | Source-code repository |

---

## Project Structure

```text
study-room-reservation/
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   └── database.py
│   │
│   ├── Dockerfile
│   ├── pyproject.toml
│   ├── README.md
│   └── uv.lock
│
├── database/
│   ├── schema.sql
│   └── seed.sql
│
├── documentation/
│
├── frontend/
│   ├── main.py
│   ├── main.spec
│   └── study_room_icon.ico
│
├── docker-compose.yml
├── .env
├── .gitignore
└── README.md
```

The `.env` file is intentionally not committed to GitHub.

---

## Database

PostgreSQL is used as the relational database management system.

The database stores information about students, study rooms, reservations and equipment.

The database schema uses primary keys and foreign keys to maintain referential integrity.

The relational model was designed with normalisation in mind and follows the intended third-normal-form structure.

The SQL files for the database are located in:

```text
database/
├── schema.sql
└── seed.sql
```

### `schema.sql`

The schema file contains the table definitions and database constraints.

### `seed.sql`

The seed file contains initial data used for development and testing.

When the PostgreSQL container is initialised for the first time, the SQL initialisation files are executed automatically.

---

## Data Model

The planned data model contains the following main entities:

### Student

Stores information about students who create reservations.

Example attributes:

```text
student_id
name
email
```

### Room

Stores the available study rooms.

Example attributes:

```text
room_id
room_number
capacity
```

### Reservation

Represents a reservation of a study room.

Example attributes:

```text
reservation_id
date
start_time
end_time
student_id
room_id
```

The reservation references both the student and the reserved room.

### Equipment

Stores equipment that can be available in study rooms.

Example attributes:

```text
equipment_id
name
```

### Room Equipment

The relationship between rooms and equipment is modelled as an N:M relationship.

```text
room_equipment(
    room_id,
    equipment_id
)
```

This allows one room to contain multiple types of equipment and one type of equipment to be available in multiple rooms.

---

## REST API

The backend is implemented using FastAPI.

The frontend communicates with the backend through HTTP requests.

The main endpoints used by the application are:

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/rooms` | Returns available study rooms |
| GET | `/reservations` | Returns existing reservations |
| POST | `/reservations` | Creates a new reservation |
| GET | `/rooms/usage` | Returns room usage statistics |

### `GET /rooms`

Returns the available study rooms including information such as room number and capacity.

The frontend uses this endpoint when establishing the connection to the API.

### `GET /reservations`

Returns existing reservations.

The response contains information such as:

- reservation ID
- date
- start time
- end time
- student name
- room number

The query uses information from related database tables.

### `POST /reservations`

Creates a new reservation.

The request contains:

```text
date
start_time
end_time
student_id
room_id
```

The endpoint requires a valid `X-API-Key`.

### `GET /rooms/usage`

Returns usage statistics for the study rooms.

The endpoint uses an aggregation to determine the number of reservations associated with each room.

---

## API Authentication

Write operations are protected using an `X-API-Key`.

The API key is stored on the server as an environment variable and is not hard-coded into the source code.

The frontend asks the user for the API URL and API key when the application starts.

The key is sent in the HTTP header:

```text
X-API-Key: <API_KEY>
```

A request with an invalid or missing API key is rejected by the API.

The API key is stored in `.env` during deployment.

The `.env` file is excluded from version control through `.gitignore`.

---

## Frontend

The frontend is implemented in Python using Tkinter.

It is a desktop application and communicates exclusively with the FastAPI backend.

The frontend does not connect directly to PostgreSQL.

At startup, the application displays a connection screen where the user enters:

- API URL
- API key

Example:

```text
API URL:
http://127.0.0.1:8000

API Key:
************
```

After a successful connection, the application loads the available study rooms.

---

## Frontend Functions

### 1. API Connection

The connection screen allows the user to enter the API URL and API key.

The application sends a request to:

```text
GET /rooms
```

If the connection is successful, the application displays the number of available rooms.

If the connection fails, an appropriate error message is shown.

---

### 2. Available Study Rooms

The main screen displays the available study rooms in a table.

The table contains:

```text
Room
Capacity
```

Example:

```text
Room    Capacity
R101       4
R102       6
R201       8
R202      12
```

---

### 3. New Reservation

The user can create a new reservation.

The reservation form contains information such as:

- date
- start time
- end time
- student ID
- study room

The frontend sends the reservation to:

```text
POST /reservations
```

The request is authenticated using the `X-API-Key`.

If the reservation is created successfully, the application displays the generated reservation ID.

---

### 4. View Reservations

The application provides an overview of existing reservations.

The frontend requests:

```text
GET /reservations
```

The reservations are displayed in a table containing:

```text
ID
Date
Start
End
Student
Room
```

---

### 5. Room Usage

The application provides a room usage screen.

It requests:

```text
GET /rooms/usage
```

The result displays information such as:

```text
Room ID
Room
Capacity
Reservations
```

This makes it possible to see how frequently the individual rooms are reserved.

---

## Reservation Conflict Handling

The application prevents overlapping reservations for the same study room.

For example, if:

```text
Room: R101
Date: 2026-08-25
Time: 14:00 - 16:00
```

is already reserved, another reservation for the same room during an overlapping time period is rejected.

The API returns an HTTP `409 Conflict`.

Example error:

```text
Room is already reserved for this time period
```

This business rule prevents double bookings.

---

## Docker Compose

Docker Compose is used to orchestrate the backend.

The Compose configuration contains two services:

```text
postgres
api
```

### PostgreSQL container

The PostgreSQL service uses:

```text
postgres:16
```

The database credentials are provided through environment variables.

A named Docker volume is used so that database data persists when the container is restarted.

### FastAPI container

The API service is built from:

```text
backend/Dockerfile
```

The API runs on port:

```text
8000
```

The API container depends on PostgreSQL being healthy before the API starts.

The Docker Compose setup therefore provides the complete backend environment.

---

## Configuration

Configuration values are stored in a `.env` file in the project root.

The file contains sensitive values such as:

```text
POSTGRES_DB=...
POSTGRES_USER=...
POSTGRES_PASSWORD=...
API_KEY=...
```

The actual values are intentionally not included in this repository.

The `.env` file is excluded using `.gitignore`.

Do not commit real passwords or API keys to GitHub.

---

## Running the Backend

### Requirements

To run the backend locally, the following are required:

- Docker Desktop
- Docker Compose

### Start the backend

Open a terminal in the project root:

```bash
cd C:\study-room-reservation
```

Start the services:

```bash
docker compose up -d
```

Check the status:

```bash
docker compose ps
```

The expected services are:

```text
postgres
api
```

The PostgreSQL service should become healthy before the API is considered ready.

### API address

The local API is available at:

```text
http://127.0.0.1:8000
```

FastAPI also provides interactive API documentation at:

```text
http://127.0.0.1:8000/docs
```

### View API logs

```bash
docker compose logs api
```

### Stop the backend

```bash
docker compose down
```

### Important: database volume

The PostgreSQL data is stored in a Docker volume.

Using:

```bash
docker compose down
```

does not remove the database volume.

Using:

```bash
docker compose down -v
```

also removes the volume and therefore deletes the stored database data.

This should only be done intentionally.

---

## Running the Frontend

During development, the Python frontend can be started from the `frontend` directory.

For example:

```bash
cd frontend
```

The Windows development version can be executed using Python if Python is correctly installed.

The application starts with a connection screen where the API URL and API key can be entered.

The default local API URL is:

```text
http://127.0.0.1:8000
```

The backend must be running when the frontend communicates with the API.

---

## Windows Executable

A Windows executable was created using PyInstaller.

The executable is located in:

```text
frontend/dist/main.exe
```

The executable allows the frontend to be started without opening the Python source code directly.

The PyInstaller configuration is stored in:

```text
frontend/main.spec
```

The application icon is stored in:

```text
frontend/study_room_icon.ico
```

The Windows executable is intended for local Windows testing.

---

## Debian Package

The final project requires the frontend to be delivered as a Debian package.

The Windows `.exe` is therefore not the final deployment format.

The intended process is:

```text
frontend/main.py
        |
        v
PyInstaller on Linux
        |
        v
Linux application
        |
        v
fpm
        |
        v
.deb package
```

The final package will be installed on the lecture server using:

```bash
sudo dpkg -i <package-name>.deb
```

The Debian package is not yet included as a completed release in the current project state.

---

## Deployment on the Lecture Server

The final deployment follows the architecture specified for the term project.

The lecture server will run:

```text
Lecture Server
│
├── Docker Compose
│   ├── PostgreSQL
│   └── FastAPI
│
└── Debian Package
    └── Study Room Reservation Frontend
```

### Backend

The backend is started with:

```bash
docker compose up -d
```

This starts:

```text
PostgreSQL
FastAPI
```

### Frontend

The frontend is installed as a `.deb` package.

Example:

```bash
sudo dpkg -i study-room-reservation_0.1.0_amd64.deb
```

After installation, the frontend can be launched from the application launcher or the installed executable.

The frontend connects to the API using the configured API URL and `X-API-Key`.

---

## Security

Security is considered at several levels.

### API authentication

Write operations require a valid `X-API-Key`.

### Database credentials

Database credentials are stored in `.env` and are not committed to GitHub.

### Frontend/database separation

The frontend never connects directly to PostgreSQL.

The communication path is:

```text
Frontend
    |
    | HTTP + X-API-Key
    v
FastAPI
    |
    | Database connection
    v
PostgreSQL
```

This separation keeps database access inside the backend.

### HTTPS

For a publicly accessible deployment, HTTPS should be used so that API keys are not transmitted over an unencrypted connection.

---

## Error Handling

The frontend handles common API and connection errors.

Examples include:

### API unavailable

```text
Could not connect to the API.
Make sure the backend is running.
```

### Invalid API key

The API returns an HTTP error and the frontend informs the user that the connection or authentication failed.

### Reservation conflict

When a room is already reserved during the requested period, the API returns:

```text
HTTP 409
```

with a message indicating that the room is already reserved for the requested time period.

### Invalid input

The frontend checks required input fields and validates values such as the student ID before sending the request.

---

## Testing

The system is tested at several levels.

### Database tests

The database should be checked for:

- primary key constraints
- foreign key constraints
- NOT NULL constraints
- uniqueness constraints
- valid relationships

### API tests

The API should be tested for:

- successful GET requests
- successful reservation creation
- invalid API keys
- missing API keys
- invalid input
- reservation conflicts
- room usage aggregation

### Business rule test

A dedicated test checks that a study room cannot be reserved twice for overlapping time periods.

For example:

```text
Reservation 1:
R101
14:00 - 16:00

Reservation 2:
R101
15:00 - 17:00
```

The second reservation must be rejected.

---

## Git and GitHub

The source code is maintained in a Git repository.

The GitHub repository contains the project source code and configuration files.

Sensitive configuration values are excluded using `.gitignore`.

In particular:

```text
.env
```

is not committed to the repository.

The repository is intended to contain the reproducible source code and project structure required for the term project.

---

## Project Status

### Completed

- [x] Study Room Reservation System concept
- [x] PostgreSQL database
- [x] Database schema
- [x] Seed data
- [x] FastAPI REST API
- [x] API key protection
- [x] Docker Compose backend
- [x] Tkinter frontend
- [x] API connection screen
- [x] Study room overview
- [x] New reservation functionality
- [x] Reservation overview
- [x] Room usage statistics
- [x] Reservation conflict handling
- [x] Windows executable
- [x] Git repository
- [x] GitHub repository
- [x] README documentation

### Remaining

- [ ] Lecture server SSH access
- [ ] Linux frontend build
- [ ] Debian `.deb` package
- [ ] Installation and final test on the lecture server
- [ ] Final project documentation
- [ ] Final project video

---

## Author

**Imane Tamouh**

Technische Hochschule Georg Agricola (THGA Bochum)

Module: Introduction to Database Management Systems

Summer Term 2026