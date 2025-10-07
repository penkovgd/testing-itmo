from reception.domain.entity.reservation import Reservation
from reception.domain.entity.room import Room
from reception.domain.exception.reservation import ReservationStatusException
from reception.domain.value_object.guest import Guest
from shared_kernel.domain.value_object import RoomStatus, ReservationStatus

from datetime import datetime
import pytest


def test_make_reservation():
    # Arrange
    ROOM_NUMBER = "R101"
    ROOM_STATUS = RoomStatus.AVAILABLE
    DATE_IN = datetime(2025, 1, 20)
    DATE_OUT = datetime(2025, 1, 27)
    GUEST_MOBILE = "+82-10-1111-2222"
    GUEST_NAME = "John"

    room = Room(number=ROOM_NUMBER, room_status=ROOM_STATUS)
    guest = Guest(mobile=GUEST_MOBILE, name=GUEST_NAME)

    # Act
    reservation = Reservation.make(
        room=room, date_in=DATE_IN, date_out=DATE_OUT, guest=guest
    )

    # Assert
    assert (
        reservation.reservation_number is not None
        and reservation.reservation_status.in_progress
        and room.room_status.is_reserved
    )


def test_cancel_reservation(valid_reservation):
    # Arrange
    reservation = valid_reservation
    room = reservation.room

    # Act
    reservation.cancel()

    # Assert
    assert (
        reservation.reservation_status == ReservationStatus.CANCELLED
        and room.room_status.is_available
    )


@pytest.mark.parametrize(
    "reservation_status", [ReservationStatus.CANCELLED, ReservationStatus.COMPLETE]
)
def test_cancel_canceled_or_completed_reservation_throws_exception(
    reservation_status: ReservationStatus, valid_reservation
):
    # Arrange
    reservation = valid_reservation
    reservation.reservation_status = reservation_status

    # Act & Assert
    with pytest.raises(ReservationStatusException):
        reservation.cancel()
