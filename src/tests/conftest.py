from datetime import datetime, date, timedelta

import pytest

from reception.domain.entity.reservation import Reservation
from reception.domain.entity.room import Room
from reception.domain.service.check_in import CheckInService
from reception.domain.value_object.guest import Guest
from reception.domain.value_object.reservation import ReservationNumber
from shared_kernel.domain.value_object import ReservationStatus, RoomStatus


@pytest.fixture
def valid_reservation():
    ROOM_NUMBER = "R101"
    ROOM_STATUS = RoomStatus.RESERVED
    RESERVATION_STATUS = ReservationStatus.IN_PROGRESS
    DATE_IN, DATE_OUT = get_valid_dates()
    GUEST_MOBILE = "+82-10-1111-2222"
    GUEST_NAME = "John"

    room = Room(number=ROOM_NUMBER, room_status=ROOM_STATUS)

    reservation = Reservation(
        room=room,
        reservation_number=ReservationNumber.generate(),
        reservation_status=RESERVATION_STATUS,
        date_in=DATE_IN,
        date_out=DATE_OUT,
        guest=Guest(
            mobile=GUEST_MOBILE,
            name=GUEST_NAME,
        ),
    )

    return reservation


def get_valid_dates():
    current_time = datetime.utcnow()

    date_in = current_time - timedelta(hours=CheckInService._EARLY_CHECK_IN_OFFSET + 1)

    date_out = (
        current_time
        - timedelta(hours=CheckInService._LATE_CHECK_IN_OFFSET - 1)
        + timedelta(days=7)
    )

    return date_in, date_out
