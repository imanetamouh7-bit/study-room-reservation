from pathlib import Path

from dotenv import dotenv_values
from fastapi import Depends, FastAPI, Header, HTTPException

from app.database import get_connection
from datetime import date, time

from pydantic import BaseModel


PROJECT_ROOT = Path(__file__).resolve().parents[2]
ENV = dotenv_values(PROJECT_ROOT / ".env")


app = FastAPI(title="Study Room Reservation System")


def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != ENV["API_KEY"]:
        raise HTTPException(
            status_code=401,
            detail="Invalid API key",
        )


@app.get("/")
def root():
    connection = get_connection()
    connection.close()

    return {"message": "Study Room Reservation System API is running"}


@app.get("/rooms")
def get_rooms():
    connection = get_connection()

    cursor = connection.cursor()
    cursor.execute(
        """
        SELECT room_id, room_number, capacity
        FROM room
        ORDER BY room_id
        """
    )

    rooms = cursor.fetchall()

    cursor.close()
    connection.close()

    return [
        {
            "room_id": room[0],
            "room_number": room[1],
            "capacity": room[2],
        }
        for room in rooms
    ]
@app.get("/reservations")
def get_reservations():
    connection = get_connection()

    cursor = connection.cursor()
    cursor.execute(
        """
        SELECT
            r.reservation_id,
            r.date,
            r.start_time,
            r.end_time,
            s.name AS student_name,
            s.email AS student_email,
            ro.room_number,
            ro.capacity
        FROM reservation AS r
        JOIN student AS s
            ON r.student_id = s.student_id
        JOIN room AS ro
            ON r.room_id = ro.room_id
        ORDER BY r.date, r.start_time
        """
    )

    reservations = cursor.fetchall()

    cursor.close()
    connection.close()

    return [
        {
            "reservation_id": reservation[0],
            "date": reservation[1],
            "start_time": reservation[2],
            "end_time": reservation[3],
            "student_name": reservation[4],
            "student_email": reservation[5],
            "room_number": reservation[6],
            "capacity": reservation[7],
        }
        for reservation in reservations
    ]
class ReservationCreate(BaseModel):
    date: date
    start_time: time
    end_time: time
    student_id: int
    room_id: int
@app.post("/reservations", status_code=201)
def create_reservation(
    reservation: ReservationCreate,
    _: None = Depends(verify_api_key),
):  
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT reservation_id
        FROM reservation
        WHERE room_id = %s
          AND date = %s
          AND start_time < %s
          AND end_time > %s
        """,
        (
            reservation.room_id,
            reservation.date,
            reservation.end_time,
            reservation.start_time,
        ),
    )

    if cursor.fetchone() is not None:
        cursor.close()
        connection.close()

        raise HTTPException(
            status_code=409,
            detail="Room is already reserved for this time period",
        )

    cursor.execute(
        """
        INSERT INTO reservation
            (date, start_time, end_time, student_id, room_id)
        VALUES
            (%s, %s, %s, %s, %s)
        RETURNING reservation_id
        """,
        (
            reservation.date,
            reservation.start_time,
            reservation.end_time,
            reservation.student_id,
            reservation.room_id,
        ),
    )

    reservation_id = cursor.fetchone()[0]

    connection.commit()

    cursor.close()
    connection.close()

    return {
        "reservation_id": reservation_id,
        "message": "Reservation created successfully",
    }
    connection = get_connection()
    cursor = connection.cursor()

    # Prüfen, ob sich eine Reservierung für denselben Raum überschneidet
    cursor.execute(
        """
        SELECT reservation_id
        FROM reservation
        WHERE room_id = %s
          AND date = %s
          AND start_time < %s
          AND end_time > %s
        """,
        (
            reservation.room_id,
            reservation.date,
            reservation.end_time,
            reservation.start_time,
        ),
    )

    if cursor.fetchone() is not None:
        cursor.close()
        connection.close()

        raise HTTPException(
            status_code=409,
            detail="Room is already reserved for this time period",
        )

    cursor.execute(
        """
        INSERT INTO reservation
            (date, start_time, end_time, student_id, room_id)
        VALUES
            (%s, %s, %s, %s, %s)
        RETURNING reservation_id
        """,
        (
            reservation.date,
            reservation.start_time,
            reservation.end_time,
            reservation.student_id,
            reservation.room_id,
        ),
    )

    reservation_id = cursor.fetchone()[0]

    connection.commit()

    cursor.close()
    connection.close()

    return {
        "reservation_id": reservation_id,
        "message": "Reservation created successfully",
    }  
@app.get("/rooms/usage")
def get_room_usage():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            ro.room_id,
            ro.room_number,
            ro.capacity,
            COUNT(r.reservation_id) AS reservation_count
        FROM room AS ro
        LEFT JOIN reservation AS r
            ON ro.room_id = r.room_id
        GROUP BY
            ro.room_id,
            ro.room_number,
            ro.capacity
        ORDER BY ro.room_id
        """
    )

    usage = cursor.fetchall()

    cursor.close()
    connection.close()

    return [
        {
            "room_id": room[0],
            "room_number": room[1],
            "capacity": room[2],
            "reservation_count": room[3],
        }
        for room in usage
    ]  