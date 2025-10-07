from datetime import datetime, timedelta
import pytest

from reception.domain.exception.check_in import (
    CheckInAuthenticationException,
    CheckInDateException,
)
from reception.domain.service.check_in import CheckInService


def test_check_in(valid_reservation):
    # Arrange
    reservation = valid_reservation
    room = reservation.room
    service = CheckInService()

    # Act
    service.check_in(reservation=reservation, mobile=reservation.guest.mobile)

    # Assert
    assert room.room_status.is_occupied


@pytest.mark.parametrize(
    "date_in",
    [
        # Заехать нельзя в будущем
        datetime.utcnow() + timedelta(hours=1),
        # Заехать нельзя на _EARLY_CHECK_IN_OFFSET часов раньше чем
        datetime.utcnow() - timedelta(hours=CheckInService._EARLY_CHECK_IN_OFFSET - 1),
    ],
)
@pytest.mark.parametrize(
    "date_out",
    [
        # Не может быть такого, чтобы date_out > date_in
        datetime.utcnow() + timedelta(hours=1),
        # Въехать нельзя за _LATE_CHECK_IN_OFFSET до date_out
        datetime.utcnow() + timedelta(hours=CheckInService._LATE_CHECK_IN_OFFSET - 1),
    ],
)
def test_check_in_invalid_date_throws_exception(valid_reservation, date_in, date_out):
    # Arrange
    reservation = valid_reservation
    reservation.date_in = date_in
    reservation.date_out = date_out
    service = CheckInService()

    # Act & Assert
    with pytest.raises(CheckInDateException):
        service.check_in(reservation=reservation, mobile=reservation.guest.mobile)


def test_check_in_invalid_guest_throws_exception(valid_reservation):
    # Arrange
    reservation = valid_reservation
    mobile = "Invalid_mobile"
    service = CheckInService()

    # Act & Assert
    with pytest.raises(CheckInAuthenticationException):
        service.check_in(reservation=reservation, mobile=mobile)
