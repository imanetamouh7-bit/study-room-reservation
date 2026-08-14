# Study Room Reservation System

A database-backed application for managing study rooms and reservations.

## Architecture

```text
Tkinter Frontend
       |
       | HTTP + X-API-Key
       v
FastAPI REST API
       |
       v
PostgreSQL